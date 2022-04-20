from rest_framework import status
from rest_framework.reverse import reverse_lazy

from apps.core.tests import UserAPITestCase


class AuthAPITest(UserAPITestCase):
    token_obtain_pair_view = 'token-obtain-pair'
    token_verify_view = 'token-verify'
    token_refresh_view = 'token-refresh'

    def obtain_token(self, username, password):
        url = reverse_lazy(self.token_obtain_pair_view)
        data = {
            "username": username,
            "password": password
        }
        return self.client.post(url, data, format='json')

    def verify_token(self, token):
        url = reverse_lazy(self.token_verify_view)
        data = {
            "token": token
        }
        return self.client.post(url, data, format='json')

    def refresh_token(self, refresh):
        url = reverse_lazy(self.token_refresh_view)
        data = {
            "refresh": refresh
        }
        return self.client.post(url, data, format='json')

    def test_obtain_token_with_valid_credentials(self):
        response = self.obtain_token(self.current_user.username,
                                     self.current_user_password)
        assert response.status_code == status.HTTP_200_OK
        assert 'refresh' in response.data
        assert 'access' in response.data
        return response

    def test_obtain_token_with_fake_credentials(self):
        response = self.obtain_token('fake', 'fake')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data

    def test_refresh_token_with_valid_token(self):
        response_token = self.obtain_token(self.current_user.username,
                                           self.current_user_password)
        assert response_token.status_code == status.HTTP_200_OK
        response = self.refresh_token(response_token.data['refresh'])
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_refresh_token_with_fake_token(self):
        response = self.refresh_token('fake refresh token')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data
        assert 'code' in response.data
        assert response.data['code'] == 'token_not_valid'

    def test_verify_token_with_valid_token(self):
        response_token = self.obtain_token(self.current_user.username,
                                           self.current_user_password)
        assert response_token.status_code == status.HTTP_200_OK
        response = self.verify_token(response_token.data['access'])
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_verify_token_with_fake_token(self):
        response = self.verify_token('fake access token')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data
        assert 'code' in response.data
        assert response.data['code'] == 'token_not_valid'
