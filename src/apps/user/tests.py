from rest_framework.reverse import reverse_lazy
from rest_framework import status

from django.contrib.auth.models import User

from apps.core.tests import LoggedUserAPITestCase


class UserAPITests(LoggedUserAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User(username='test', email='test@test.com')
        self.user.save()

    def tearDown(self) -> None:
        super().tearDown()
        self.user.delete()

    def get_users(self, **kwargs):
        url = reverse_lazy('user-list')
        return self.client.get(url, kwargs, format='json')

    def get_user(self, pk, **kwargs):
        url = reverse_lazy('user-detail', kwargs={'pk': pk})
        return self.client.get(url, kwargs, format='json')

    def test_get_users(self):
        response = self.get_users()
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_with_valid_pk(self):
        response = self.get_user(self.user.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_with_fake_pk(self):
        response = self.get_user(1444)  # fake pk
        assert response.status_code == status.HTTP_404_NOT_FOUND
