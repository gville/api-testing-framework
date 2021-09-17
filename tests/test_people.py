from assertpy.assertpy import soft_assertions
from models.person import Person
from people_client import PeopleClient
from assertpy import assert_that
from config import BASE_URL
from cerberus import Validator
from utils import data_reader


class TestPeopleApi:

    def setup_class(self):
        self.client = PeopleClient(url=BASE_URL)

    def test_get_people_has_kent(self):
        response = self.client.get_people()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).extracting('fname').contains('Kent')

    def test_new_person_can_be_added(self):
        payload, unique_lname = self.client.generate_new_person_data()
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        people = self.client.get_people().json()
        lname = [person['lname'] for person in people]
        assert_that(lname).contains(unique_lname)

    def test_existent_person_can_not_be_added(self):
        payload, _ = self.client.generate_new_person_data()
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(409)

    def test_get_person_by_id(self):
        response = self.client.get_person(1)
        assert_that(response.status_code).is_equal_to(200)
        person = Person(**response.json())
        assert_that(person.fname).is_equal_to('Doug')
        assert_that(person.lname).is_equal_to('Farrell')
    
    def test_created_person_can_be_deleted(self):
        payload, unique_lname = self.client.generate_new_person_data()
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        people = self.client.get_people().json()
        new_person = [person for person in people if person['lname'] == unique_lname][0]
        
        response = self.client.delete_person(new_person['person_id'])
        assert_that(response.status_code).is_equal_to(200)

    def test_person_schema(self):
        schema = data_reader.read_json_from_file("person_schema.json")
        response = self.client.get_person(1)
        validator = Validator(schema, required_all=True)
        is_valid = validator.validate(response.json())
        assert_that(is_valid, description=validator.errors).is_true()

    def test_people_schema(self):
        schema = data_reader.read_json_from_file("person_schema.json")
        response = self.client.get_people()
        validator = Validator(schema, required_all=True)
        with soft_assertions():
            for person in response.json():
                is_valid = validator.validate(person)
                assert_that(is_valid, description=validator.errors).is_true()
