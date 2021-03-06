import requests
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class UserListTestCase(APITestCase):

    def test_user_list(self):
        url = 'http://127.0.0.1:8000/api/v1/user/list/'
        response = self.client.get(url, format='json')
        print('------test_user_list------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateUserTestCase(APITestCase):

    # def test_create_user_success(self):
    #     url = 'http://127.0.0.1:8000/api/v1/user/'
    #     data = {
    #         "city_id":"8961d794-f03e-49b2-a694-7f3aec447b41",
    #         "user_type_id":"46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
    #         "user_subtype_id":"c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
    #         "form_factor_id":"1735f7cc-8029-4754-855a-67532ecc0257",
    #         "department_id":"ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
    #         "status_id":"ec3afefb-aebe-4c02-8ad0-889c3cab341f",
    #         "first_name":"arpita",
    #         "middle_name":"ghansham",
    #         "last_name":"badwaik",
    #         "phone_mobile":"8483003577",
    #         "phone_landline":"8483003504",
    #         "password":"badwaik20",
    #         "email": "admin@duv.com"
    #     }
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
    #     headers = {'token': token}
    #     response = requests.post(url, data=data, headers=headers)
    #     print('------test_create_user_success-------', response.status_code)
    #     # response = self.client.post(url, data, format='json', **{'token': token})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/user/'
        data = {
            "city_id": "8961d794-f03e-49b2-a694-7f3aec447b41",
            "user_type_id": "46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
            "user_subtype_id": "c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "status_id": "ec3afefb-aebe-4c02-8ad0-889c3cab341f",
            "first_name": "arpita",
            "middle_name": "ghansham",
            "last_name": "badwaik",
            "phone_mobile": "8483003577",
            "phone_landline": "8483003504",
            "password": "badwaik20",
            "email": "admin@du.com"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_user_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/'
        data = {
            "city_id":"8961d794-f03e-49b2-a694-7f3aec447b42",
            "user_type_id":"46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
            "user_subtype_id":"c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
            "form_factor_id":"1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id":"ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "status_id":"ec3afefb-aebe-4c02-8ad0-889c3cab341f",
            "first_name":"arpita",
            "middle_name":"ghansham",
            "last_name":"badwaik",
            "phone_mobile":"8483003577",
            "phone_landline":"8483003504",
            "password":"badwaik20",
            "email": "admin@dua.com"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/'
        data = {
            "city_id": "8961d794-f03e-49b2-a694-7f3aec447b41",
            "user_type_id": "46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
            "user_subtype_id": "c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "status_id": "ec3afefb-aebe-4c02-8ad0-889c3cab341f",
            "first_name": "arpita",
            "middle_name": "ghansham",
            "last_name": "badwaik",
            "phone_mobile": "8483003577",
            "phone_landline": "8483003504",
            "password": "badwaik20",
            "email": "admin@dua.com"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserTestCase(APITestCase):

    def test_get_user_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/5e1c8a66-74b7-46ba-966a-878de96ab7a5'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/5e1c8a66-74b7-46ba-966a-878de96ab7aa'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_not_authenticated(self):
        url = 'http://127.0.0.1:8000/api/v1/user/5e1c8a66-74b7-46ba-966a-878de96ab7aa'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJN'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_not_authenticated-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateUserTestCase(APITestCase):

    def test_update_user_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279'
        data = {
            "city_id":"8961d794-f03e-49b2-a694-7f3aec447b41",
            "user_type_id":"46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
            "user_subtype_id":"c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
            "form_factor_id":"1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id":"ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "status_id":"ec3afefb-aebe-4c02-8ad0-889c3cab341f",
            "first_name":"twinkle",
            "middle_name":"ghansham",
            "last_name":"badwaik",
            "phone_mobile":"8483003504",
            "phone_landline":"8483003504",
            "password":"admin"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_user_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e270'
        data = {
            "city_id": "8961d794-f03e-49b2-a694-7f3aec447b41",
            "user_type_id": "46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
            "user_subtype_id": "c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "status_id": "ec3afefb-aebe-4c02-8ad0-889c3cab341f",
            "first_name": "twinkle",
            "middle_name": "ghansham",
            "last_name": "badwaik",
            "phone_mobile": "8483003504",
            "phone_landline": "8483003504",
            "password": "admin"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_user_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279'
        data = {
            "city_id": "8961d794-f03e-49b2-a694-7f3aec447b41",
            "user_type_id": "46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
            "user_subtype_id": "c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "status_id": "ec3afefb-aebe-4c02-8ad0-889c3cab341f",
            "first_name": "twinkle",
            "middle_name": "ghansham",
            "last_name": "badwaik",
            "phone_mobile": "8483003504",
            "phone_landline": "8483003504",
            "password": "admin"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_user_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLoginTestCase(APITestCase):

    def test_login_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/login/'
        data = {'email': 'admin@du.com', 'password': 'badwaik20'}
        response = self.client.post(url, data, format='json')
        print('------test_login_success------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_not_authorized(self):
        url = 'http://127.0.0.1:8000/api/v1/user/login/'
        data = {'email': 'admin@du.com', 'password': 'badwaik201'}
        response = self.client.post(url, data, format='json')
        print('------test_login_not_authorized------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_bad_request(self):
        url = 'http://127.0.0.1:8000/api/v1/user/login/'
        data = {'email': 'admin@du.com'}
        response = self.client.post(url, data, format='json')
        print('-----test_login_bad_request-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogoutTestCase(APITestCase):

    # def test_logout_success(self):
    #     url = 'http://127.0.0.1:8000/api/v1/user/logout/'
    #     data = {'id_string' : '10e94252-7991-4f72-b73f-84295969e279'}
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjhERjQxRCJ9.AhcENQ_yUZ7z4vuWwDFnwmcqpRr_nAqxsmmoi5l4pok'
    #     headers = {'token': token}
    #     response = requests.post(url, data, headers=headers)
    #     print('-----test_logout_success-------', response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_not_authorized(self):
        url = 'http://127.0.0.1:8000/api/v1/user/logout/'
        data = {'id_string': '265ab340-b9c4-4ea9-ac1d-2857a20bc291'}
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data, headers=headers)
        print('------test_logout_not_authorized------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_bad_request(self):
        url = 'http://127.0.0.1:8000/api/v1/user/logout/'
        data = {'id_string': '265ab340-b9c4-4ea9-ac1d-2857a20bc291'}
        headers = {}
        response = requests.post(url, data, headers=headers)
        print('-----test_logout_bad_request-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RoleListTestCase(APITestCase):

    def test_role_list(self):
        url = 'http://127.0.0.1:8000/api/v1/role/list/'
        response = self.client.get(url, format='json')
        print('------test_role_list------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateRoleTestCase(APITestCase):

    # def test_create_role_success(self):
    #     url = 'http://127.0.0.1:8000/api/v1/role/'
    #     data = {
    #         "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
    #         "type_id": "8b8e41f9-21b6-4af8-8a63-d0596bf36199",
    #         "sub_type_id": "a246c566-86f5-4699-bfb5-5b903c5fc601",
    #         "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
    #         "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
    #         "role": "role23"
    #     }
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
    #     headers = {'token': token}
    #     response = requests.post(url, data=data, headers=headers)
    #     print('------test_create_role_success-------', response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_role_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/role/'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "type_id": "8b8e41f9-21b6-4af8-8a63-d0596bf36199",
            "sub_type_id": "a246c566-86f5-4699-bfb5-5b903c5fc601",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "role": "role23"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_role_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_role_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/role/'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf47",
            "type_id": "8b8e41f9-21b6-4af8-8a63-d0596bf36199",
            "sub_type_id": "a246c566-86f5-4699-bfb5-5b903c5fc601",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "role": "role23"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_role_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_role_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/role/'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "type_id": "8b8e41f9-21b6-4af8-8a63-d0596bf36199",
            "sub_type_id": "a246c566-86f5-4699-bfb5-5b903c5fc601",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "role": "role23"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_role_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetRoleTestCase(APITestCase):

    def test_get_role_success(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_role_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_role_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df01'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_role_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_role_not_authenticated(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_role_not_authenticated-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateRoleTestCase(APITestCase):

    def test_update_role_success(self):
        url = 'http://127.0.0.1:8000/api/v1/role/0952eb82-cb2b-405c-a7a9-39f1ac39bf77'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "type_id": "8b8e41f9-21b6-4af8-8a63-d0596bf36199",
            "sub_type_id": "a246c566-86f5-4699-bfb5-5b903c5fc601",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "role": "role1234"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_role_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/role/0952eb82-cb2b-405c-a7a9-39f1ac39bf70'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "type_id": "8b8e41f9-21b6-4af8-8a63-d0596bf36199",
            "sub_type_id": "a246c566-86f5-4699-bfb5-5b903c5fc601",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "role": "role23"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_role_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_role_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/role/0952eb82-cb2b-405c-a7a9-39f1ac39bf77'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "type_id": "8b8e41f9-21b6-4af8-8a63-d0596bf36199",
            "sub_type_id": "a246c566-86f5-4699-bfb5-5b903c5fc601",
            "form_factor_id": "1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id": "ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "role": "role23"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_role_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivilegeListTestCase(APITestCase):

    def test_privilege_list(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/list/'
        response = self.client.get(url, format='json')
        print('------test_privilege_list------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreatePrivilegeTestCase(APITestCase):

    # def test_create_privilege_success(self):
    #     url = 'http://127.0.0.1:8000/api/v1/privilege/'
    #     data = {
    #         "name": "delete"
    #     }
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
    #     headers = {'token': token}
    #     response = requests.post(url, data=data, headers=headers)
    #     print('------test_create_privilege_success-------', response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_privilege_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/'
        data = {
             "name": "delete"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_privilege_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_privilege_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/'
        data = {
             "name":"delete"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_privilege_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetPrivilegeTestCase(APITestCase):

    def test_get_privilege_success(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/180205c7-9e2e-481b-9131-d22291cf7d8e'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_privilege_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_privilege_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/180205c7-9e2e-481b-9131-d22291cf7d8g'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_privilege_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_privilege_not_authenticated(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/180205c7-9e2e-481b-9131-d22291cf7d8e'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_privilege_not_authenticated-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdatePrivilegeTestCase(APITestCase):

    # def test_update_privilege_success(self):
    #     url = 'http://127.0.0.1:8000/api/v1/privilege/180205c7-9e2e-481b-9131-d22291cf7d8e'
    #     data = {
    #         "name": "new"
    #     }
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
    #     headers = {'token': token}
    #     response = requests.put(url, data=data, headers=headers)
    #     print('------test_update_privilege_success-------', response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_privilege_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/180205c7-9e2e-481b-9131-d22291cf7d8y'
        data = {
            "name": "new-delete"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_privilege_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_privilege_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/privilege/180205c7-9e2e-481b-9131-d22291cf7d8e'
        data = {
            "name": "new-delete"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_privilege_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetRolePrivilegeTestCase(APITestCase):

    def test_get_role_privilege_success(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d/privileges'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_role_privilege_success------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_role_privilege_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0v/privileges'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_role_privilege_not_found------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_role_privilege_not_authorized(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d/privileges'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_role_privilege_not_authorized------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateRolePrivilegeTestCase(APITestCase):

    def test_create_role_privilege_success(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d/privileges/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "data":[
                {
                    "module_id":"91727a81-d17c-45b0-a8f5-98a462fe7454",
                    "sub_module":[
                        {
                            "sub_module_id":"b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id":"94e65da1-2f9a-422f-a032-d3e192761352"
                        },
                        {
                            "sub_module_id":"b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id":"9ebfefbc-fd45-4c48-ac4a-ca7b1274f4c9"
                        }
                    ]
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_role_privilege_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_role_privilege_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d/privileges/'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "data": [
                {
                    "module_id": "91727a81-d17c-45b0-a8f5-98a462fe7454",
                    "sub_module": [
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "94e65da1-2f9a-422f-a032-d3e192761352"
                        },
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "9ebfefbc-fd45-4c48-ac4a-ca7b1274f4c9"
                        }
                    ]
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_role_privilege_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_role_privilege_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0i/privileges/'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "data": [
                {
                    "module_id": "91727a81-d17c-45b0-a8f5-98a462fe7454",
                    "sub_module": [
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "94e65da1-2f9a-422f-a032-d3e192761352"
                        },
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "9ebfefbc-fd45-4c48-ac4a-ca7b1274f4c9"
                        }
                    ]
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_role_privilege_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_role_privilege_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d/privileges/'
        data = {
            "utility_id": "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "data": [
                {
                    "module_id": "91727a81-d17c-45b0-a8f5-98a462fe7454",
                    "sub_module": [
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "94e65da1-2f9a-422f-a032-d3e192761352"
                        },
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "9ebfefbc-fd45-4c48-ac4a-ca7b1274f4c9"
                        }
                    ]
                }
            ]
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_role_privilege_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteRolePrivilegeTestCase(APITestCase):

    # def test_delete_role_privilege_success(self):
    #     url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d/privileges/'
    #     data = {
    #         "module":[
    #             {
    #                 "module_id":"91727a81-d17c-45b0-a8f5-98a462fe7454",
    #                 "sub_module":[
    #                     {
    #                         "sub_module_id":"b8ba583e-2dc2-4638-ac39-ae6603bad141",
    #                         "privilege_id":"94e65da1-2f9a-422f-a032-d3e192761352"
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
    #     headers = {'token': token}
    #     response = requests.delete(url, data=data, headers=headers)
    #     print('------test_delete_role_privilege_success-------', response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_role_privilege_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0r/privileges/'
        data = {
            "module": [
                {
                    "module_id": "91727a81-d17c-45b0-a8f5-98a462fe7454",
                    "sub_module": [
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "94e65da1-2f9a-422f-a032-d3e192761352"
                        }
                    ]
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.delete(url, data=data, headers=headers)
        print('------test_delete_role_privilege_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_role_privilege_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/role/9d6c3775-b645-436b-9417-0b1d66d9df0d/privileges/'
        data = {
            "module": [
                {
                    "module_id": "91727a81-d17c-45b0-a8f5-98a462fe7454",
                    "sub_module": [
                        {
                            "sub_module_id": "b8ba583e-2dc2-4638-ac39-ae6603bad141",
                            "privilege_id": "94e65da1-2f9a-422f-a032-d3e192761352"
                        }
                    ]
                }
            ]
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.delete(url, data=data, headers=headers)
        print('------test_delete_role_privilege_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserRoleTestCase(APITestCase):

    def test_create_user_role_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        data = {
            "utility_id" : "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "roles" : [
                {
                    "role_id_string":"9d6c3775-b645-436b-9417-0b1d66d9df0d"
                },
                {
                    "role_id_string":"c616155b-7dd9-4ef2-9b38-0eaafc74abae"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_role_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_role_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        data = {
            "utility_id" : "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "roles" : [
                {
                    "role_id_string":"9d6c3775-b645-436b-9417-0b1d66d9df0d"
                },
                {
                    "role_id_string":"c616155b-7dd9-4ef2-9b38-0eaafc74abae"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_role_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_user_role_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e270/role/'
        data = {
            "utility_id" : "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "roles" : [
                {
                    "role_id_string":"9d6c3775-b645-436b-9417-0b1d66d9df0d"
                },
                {
                    "role_id_string":"c616155b-7dd9-4ef2-9b38-0eaafc74abae"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_role_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_role_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        data = {
            "utility_id" : "8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "roles" : [
                {
                    "role_id_string":"9d6c3775-b645-436b-9417-0b1d66d9df0d"
                },
                {
                    "role_id_string":"c616155b-7dd9-4ef2-9b38-0eaafc74abae"
                }
            ]
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_privilege_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserRoleTestCase(APITestCase):

    def test_get_user_role_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_role_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_role_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e270/role/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_role_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_role_not_authenticated(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_role_not_authenticated-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteUserRoleTestCase(APITestCase):

    def test_delete_user_role_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        data = {
            "roles" : [
                {
                    "role_id_string":"9d6c3775-b645-436b-9417-0b1d66d9df0d"
                },
                {
                    "role_id_string":"c616155b-7dd9-4ef2-9b38-0eaafc74abae"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.delete(url, data=data, headers=headers)
        print('------test_delete_user_role_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_role_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        data = {
            "roles" : [
                {
                    "role_id_string":"9d6c3775-b645-436b-9417-0b1d66d9df0d"
                },
                {
                    "role_id_string":"c616155b-7dd9-4ef2-9b38-0eaafc74abae"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.delete(url, data=data, headers=headers)
        print('------test_delete_user_role_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_role_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/role/'
        data = {
            "roles": [
                {
                    "role_id_string": "9d6c3775-b645-436b-9417-0b1d66d9df0d"
                },
                {
                    "role_id_string": "c616155b-7dd9-4ef2-9b38-0eaafc74abae"
                }
            ]
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.delete(url, data=data, headers=headers)
        print('------test_delete_user_role_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserSkillTestCase(APITestCase):

    def test_get_user_skill_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/skill/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_skill_success------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_skill_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c0/skill/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_skill_not_found------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_skill_not_authorized(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/skill/'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_skill_not_authorized------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserSkillTestCase(APITestCase):

    def test_create_user_skill_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/skill/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "skills" : [
                {
                    "skill_id_string":"e3612d18-c2cd-4f2a-8c40-dd779f092cd0"
                },
                {
                    "skill_id_string":"86a86afa-c85a-4531-89e1-555358f09767"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_skill_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_skill_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/skill/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "skills" : [
                {
                    "skill_id_string":"e3612d18-c2cd-4f2a-8c40-dd779f092cd0"
                },
                {
                    "skill_id_string":"86a86afa-c85a-4531-89e1-555358f09767"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_skill_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_user_skill_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/skill/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "skills" : [
                {
                    "skill_id_string":"e3612d18-c2cd-4f2a-8c40-dd779f092cd0"
                },
                {
                    "skill_id_string":"86a86afa-c85a-4531-89e1-555358f09767"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_skill_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_skill_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/skill/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "skills" : [
                {
                    "skill_id_string":"e3612d18-c2cd-4f2a-8c40-dd779f092cd0"
                },
                {
                    "skill_id_string":"86a86afa-c85a-4531-89e1-555358f09767"
                }
            ]
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_skill_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserAreaTestCase(APITestCase):

    def test_get_user_area_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/area/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_area_success------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_area_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e270/area/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_area_not_found------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_area_not_authorized(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/area/'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_area_not_authorized------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserAreaTestCase(APITestCase):

    def test_create_user_area_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/area/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "areas" : [
                {
                    "area_id_string":"b7795190-e27d-4522-8fa9-23343c376eed"
                },
                {
                    "area_id_string":"93f22191-f68e-4767-a1b1-0d21747e01b4"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_area_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_area_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/area/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "areas" : [
                {
                    "area_id_string":"b7795190-e27d-4522-8fa9-23343c376eed"
                },
                {
                    "area_id_string":"93f22191-f68e-4767-a1b1-0d21747e01b4"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_area_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_user_area_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e270/area/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "areas" : [
                {
                    "area_id_string":"b7795190-e27d-4522-8fa9-23343c376eed"
                },
                {
                    "area_id_string":"93f22191-f68e-4767-a1b1-0d21747e01b4"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_area_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_area_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/area/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "areas" : [
                {
                    "area_id_string":"b7795190-e27d-4522-8fa9-23343c376eed"
                },
                {
                    "area_id_string":"93f22191-f68e-4767-a1b1-0d21747e01b4"
                }
            ]
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_area_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserUtilityTestCase(APITestCase):

    def test_get_user_utility_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/utility/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_utility_success------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_utility_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9co/utility/'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_utility_not_found------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_utility_not_authorized(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/utility/'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_utility_not_authorized------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserUtilityTestCase(APITestCase):

    def test_create_user_utility_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/utility/'
        data = {
            "utilities" : [
                {
                    "utility_id_string":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f"
                },
                {
                    "utility_id_string":"78de46e9-0a05-4fbc-a4e1-12041d7b580a"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_utility_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_utility_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/utility/'
        data = {
            "utilities" : [
                {
                    "utility_id_string":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f"
                },
                {
                    "utility_id_string":"78de46e9-0a05-4fbc-a4e1-12041d7b580a"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_utility_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_user_utility_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c0/utility/'
        data = {
            "utilities" : [
                {
                    "utility_id_string":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f"
                },
                {
                    "utility_id_string":"78de46e9-0a05-4fbc-a4e1-12041d7b580a"
                }
            ]
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_utility_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_utility_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/3004e182-7dee-4565-afe5-7cd38be6a9c5/utility/'
        data = {
            "utilities" : [
                {
                    "utility_id_string":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f"
                },
                {
                    "utility_id_string":"78de46e9-0a05-4fbc-a4e1-12041d7b580a"
                }
            ]
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_utility_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserBankTestCase(APITestCase):

    def test_get_user_bank_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/bank'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_bank_success------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_bank_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e270/bank'
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_bank_not_found------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_bank_not_authorized(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/bank'
        token = 'abcd'
        headers = {'token': token}
        response = requests.get(url, headers=headers)
        print('------test_get_user_bank_not_authorized------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateUserBankTestCase(APITestCase):

    def test_create_user_bank_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/bank/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "bank_id":"70a52737-6a73-4f53-9c7b-d01c28a9346b"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_bank_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_bank_conflict(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/bank/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "bank_id":"70a52737-6a73-4f53-9c7b-d01c28a9346b"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_bank_conflict-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_user_bank_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e27a/bank/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "bank_id":"70a52737-6a73-4f53-9c7b-d01c28a9346b"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_bank_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_bank_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/bank/'
        data = {
            "utility_id":"8d2b7039-84fe-44cb-8b4e-cf0c011dbf4f",
            "bank_id":"70a52737-6a73-4f53-9c7b-d01c28a9346b"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.post(url, data=data, headers=headers)
        print('------test_create_user_bank_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateUserBankTestCase(APITestCase):

    def test_update_user_bank_success(self):
        url = 'http://127.0.0.1:8000/api/v1/user/10e94252-7991-4f72-b73f-84295969e279/bank/'
        data = {
            "bank_id":"ba0ac53f-a2f6-4e97-86be-2d21507ab09c"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_user_bank_success-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_bank_not_found(self):
        url = 'http://127.0.0.1:8000/api/v1/user/e4d4c8da-31b0-458f-8bdd-7f04bb259c45/bank/'
        data = {
            "bank_id":"ba0ac53f-a2f6-4e97-86be-2d21507ab09c"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjY3NzEyQSJ9.YQ_tNdxIKZEaYtKn6l_Na6wZd2WgkzRqjAu_GZBDEJM'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_user_bank_not_found-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_bank_not_authenticate(self):
        url = 'http://127.0.0.1:8000/api/v1/user/e4d4c8da-31b0-458f-8bdd-7f04bb259c45/bank/'
        data = {
            "bank_id":"ba0ac53f-a2f6-4e97-86be-2d21507ab09c"
        }
        token = 'abcd'
        headers = {'token': token}
        response = requests.put(url, data=data, headers=headers)
        print('------test_update_user_bank_not_authenticate-------', response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)