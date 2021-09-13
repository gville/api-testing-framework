import requests

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
