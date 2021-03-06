from assertpy.assertpy import soft_assertions
from models.person import Person
from models.error import Error
from people_client import PeopleClient
from assertpy import assert_that
from config import BASE_URL
from cerberus import Validator
from utils import data_reader


class TestPeopleApi:

    def setup_class(self):
        self.client = PeopleClient(url=BASE_URL)

    def test_get_people_has_specific_person(self):
        specific_person = 'Kent'
        response = self.client.get_people()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).extracting('fname').contains(specific_person)

    def test_new_person_can_be_added(self):
        payload, _, unique_lname = self.client.generate_new_person_data()
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        people = self.client.get_people().json()
        assert_that(people).extracting('lname').contains(unique_lname)

    def test_existent_person_can_not_be_added(self):
        payload, fname, lname = self.client.generate_new_person_data()
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        response = self.client.create_person(payload)
        error = Error(**response.json())
        assert_that(response.status_code).is_equal_to(409)
        assert_that(error.status).is_equal_to(409)
        error_msg = f"Person with {fname} {lname} already exists"
        assert_that(error.detail).is_equal_to(error_msg)

    def test_get_person_by_id(self):
        person_id = 1
        response = self.client.get_person(person_id)
        
        assert_that(response.status_code).is_equal_to(200)
        person = Person(**response.json())
        assert_that(person.fname).is_equal_to('Doug')
        assert_that(person.lname).is_equal_to('Farrell')
        assert_that(person.person_id).is_equal_to(person_id)
    
    def test_created_person_can_be_deleted(self):
        payload, _, lname = self.client.generate_new_person_data()
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        people = self.client.get_people().json()
        new_person = [person for person in people if person['lname'] == lname][0]
        
        response = self.client.delete_person(new_person['person_id'])
        assert_that(response.status_code).is_equal_to(200)

    def test_unexistent_person_can_not_be_deleted(self):
        unexistent_person_id = 0
        response = self.client.delete_person(unexistent_person_id)
        
        assert_that(response.status_code).is_equal_to(404)
        error = Error(**response.json())
        assert_that(error.status).is_equal_to(404)
        assert_that(error.detail).is_equal_to(f'Person not found for id {unexistent_person_id}')

    def test_created_person_can_be_updated(self):
        payload, _, lname = self.client.generate_new_person_data()
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        people = self.client.get_people().json()
        new_person = [person for person in people if person['lname'] == lname][0]
        
        updated_payload, _, _ = self.client.generate_new_person_data()

        response = self.client.update_person(new_person['person_id'], updated_payload)
        assert_that(response.status_code).is_equal_to(200)

    def test_person_schema(self):
        schema = data_reader.read_json_from_file("person_schema.json")
        validator = Validator(schema, required_all=True)
        
        response = self.client.get_person(1)
        
        is_valid = validator.validate(response.json())
        assert_that(is_valid, description=validator.errors).is_true()

    def test_people_schema(self):
        schema = data_reader.read_json_from_file("person_schema.json")
        validator = Validator(schema, required_all=True)
        
        response = self.client.get_people()
        
        with soft_assertions():
            for person in response.json():
                is_valid = validator.validate(person)
                assert_that(is_valid, description=validator.errors).is_true()

    def test_error_schema(self):
        schema = data_reader.read_json_from_file('error_schema.json')
        validator = Validator(schema)
        
        unexistent_person_id = 0
        response = self.client.delete_person(unexistent_person_id)
        
        is_valid = validator.validate(response.json())
        assert_that(is_valid, description=validator.errors).is_true()
