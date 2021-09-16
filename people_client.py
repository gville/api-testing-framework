import json
import requests
import uuid

from utils.data_reader import read_file

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

    def __generate_payload_and_unique_lname(self):
        unique_lname = f'User {str(uuid.uuid4())}'
        person = read_file('person.json')
        person_dictionary = json.load(person)
        person_dictionary['lname'] = unique_lname
        payload = json.dumps(person_dictionary)
        return payload, unique_lname

    def delete_person(self, person_id):
        response = requests.delete(f'{self.base_url}/{person_id}')
        return response