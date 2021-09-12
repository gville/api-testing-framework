import json
import uuid
import requests
from assertpy import assert_that
from config import BASE_URL


def test_get_people_has_kent():
    response = requests.get(url=BASE_URL)
    assert_that(response.status_code).is_equal_to(200)
    fname = [person['fname'] for person in response.json()]
    assert_that(fname).contains('Kent')


def test_new_person_can_be_added():
    unique_lname = f'User {str(uuid.uuid4())}'
    payload = json.dumps({
        'fname': 'QATA',
        'lname': unique_lname
    })
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'
               }
    response = requests.post(url=BASE_URL, data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(204)

    people = requests.get(BASE_URL).json()
    lname = [person['lname'] for person in people]
    assert_that(lname).contains(unique_lname)
