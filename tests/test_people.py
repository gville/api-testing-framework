import json
from people_client import PeopleClient
import uuid
from assertpy import assert_that
from config import BASE_URL

class TestPeopleApi:

    def setup_class(self):
        self.client = PeopleClient(url=BASE_URL)

    def test_get_people_has_kent(self):
        response = self.client.get_people()
        assert_that(response.status_code).is_equal_to(200)
        fname = [person['fname'] for person in response.json()]
        assert_that(fname).contains('Kent')


    def test_new_person_can_be_added(self):
        unique_lname = f'User {str(uuid.uuid4())}'
        payload = json.dumps({
            'fname': 'QATA',
            'lname': unique_lname
        })
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

        people = self.client.get_people().json()
        lname = [person['lname'] for person in people]
        assert_that(lname).contains(unique_lname)

    def test_existent_person_can_not_be_added(self):
        payload = json.dumps({
            'fname': 'Kent',
            'lname': 'Brockman'
        })
        response = self.client.create_person(payload)
        assert_that(response.status_code).is_equal_to(409)

    def test_get_person_by_id(self):
        response = self.client.get_person(1)
        assert_that(response.status_code).is_equal_to(200)
        person = response.json()
        assert_that(person.get('fname')).is_equal_to('Doug')
        assert_that(person.get('lname')).is_equal_to('Farrell')
