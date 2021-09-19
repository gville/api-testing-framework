import json
import requests
import uuid

from utils import data_reader

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
        payload, fname, lname = self.__generate_payload_and_names()
        return payload, fname, lname

    def __generate_payload_and_names(self):
        person_json = data_reader.read_file('person.json')
        person_dict = json.load(person_json)
        unique_lname = f'User {str(uuid.uuid4())}'
        person_dict['lname'] = unique_lname
        payload = json.dumps(person_dict)
        return payload, person_dict['fname'], unique_lname

    def update_person(self, person_id, payload):
        headers = {'Content-type': 'application/json',
                'Accept': 'application/json'
                }
        response = requests.put(f'{self.base_url}/{person_id}', data=payload, headers=headers)
        return response

    def delete_person(self, person_id):
        response = requests.delete(f'{self.base_url}/{person_id}')
        return response