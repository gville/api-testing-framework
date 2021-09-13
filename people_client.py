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

    def generate_payload_and_unique_lname(self, dictionary=None):
        if dictionary is None:
            unique_lname = f'User {str(uuid.uuid4())}'
            payload = json.dumps({
                'fname': 'QATA',
                'lname': unique_lname
            })
        else:
            unique_lname = dictionary['lname']
            payload = json.dumps(dictionary)
        return payload, unique_lname

    def delete_person(self, person_id):
        response = requests.delete(f'{self.base_url}/{person_id}')
        return response