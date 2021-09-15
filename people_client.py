import json
import requests
import uuid

class PeopleClient:

    def __init__(self, url):
        self.base_url = url

    def get_people(self):
        response = requests.get(self.base_url)
        return response

    def get_person(self, person_id):
        response = requests.get(f'{self.base_url}/{person_id}')
        return response

    def create_person(self, payload):
        headers = {'Content-type': 'application/json',
                'Accept': 'application/json'
                }
        response = requests.post(self.base_url, data=payload, headers=headers)
        return response

    def generate_new_person_data(self):
        payload, unique_lname = self.__generate_payload_and_unique_lname()
        return payload, unique_lname

    def generate_existent_person_data(self):
        existent_person = {
            'fname': 'Kent',
            'lname': 'Brockman'
        }
        payload, _ = self.__generate_payload_and_unique_lname(existent_person)
        return payload

    def __generate_payload_and_unique_lname(self, dictionary=None):
        if dictionary is None:
            unique_lname = f'User {str(uuid.uuid4())}'
            person = open("tests/data/person.json", "r")
            person_dictionary = json.load(person)
            person_dictionary['lname'] = unique_lname
            payload = json.dumps(person_dictionary)
        else:
            unique_lname = dictionary['lname']
            payload = json.dumps(dictionary)
        return payload, unique_lname

    def delete_person(self, person_id):
        response = requests.delete(f'{self.base_url}/{person_id}')
        return response