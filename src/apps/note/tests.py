from rest_framework.reverse import reverse_lazy
from rest_framework import status

from apps.note.models import Note, Tag
from apps.core.tests import LoggedUserAPITestCase


class NoteAPITests(LoggedUserAPITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.tag = Tag(name='new tag')
        self.tag.save()
        self.note = Note(title='admin',
                         body='admin@gmail.com',
                         author=self.current_user)
        self.note.save()
        self.note.tags.add(self.tag)
        self.note.save()

    def tearDown(self) -> None:
        super().tearDown()
        self.tag.delete()
        self.note.delete()

    def get_notes(self, **kwargs):
        url = reverse_lazy('note-list')
        return self.client.get(url, kwargs, format='json')

    def get_note(self, pk, **kwargs):
        url = reverse_lazy('note-detail', kwargs={'pk': pk})
        return self.client.get(url, kwargs, format='json')

    def new_note(self, title, body, tags):
        url = reverse_lazy('note-list')
        data = {
            "title": title,
            "body": body,
            "tags": tags
        }
        response = self.client.post(url, data, format='json')
        return response

    def delete_note(self):
        url = reverse_lazy('note-detail', kwargs={'pk': self.note.pk})
        response = self.client.delete(url, format='json')
        return response

    def update_put_note(self, title, body, tags):
        url = reverse_lazy('note-detail', kwargs={'pk': self.note.pk})
        data = {
            "title": title,
            "body": body,
            "tags": tags
        }
        response = self.client.put(url, data, format='json')
        return response

    def update_patch_note(self, title, body, tags):
        url = reverse_lazy('note-detail', kwargs={'pk': self.note.pk})
        data = {
            "title": title,
            "body": body,
            "tags": tags
        }
        response = self.client.patch(url, data, format='json')
        return response

    def test_new_note_with_valid_data(self):
        response = self.new_note('note title',
                                 'note body',
                                 ["tag: 1", "tag: 2"])
        assert response.status_code == status.HTTP_201_CREATED

    def test_put_note_with_valid_data(self):
        response = self.update_put_note('note title',
                                        'note body',
                                        ["tag: 7", "tag: 6"])
        assert response.status_code == status.HTTP_200_OK

    def test_patch_note_with_valid_data(self):
        response = self.update_patch_note('note title',
                                          'note body',
                                          ["tag: 3", "tag: 4"])
        assert response.status_code == status.HTTP_200_OK

    def test_delete_note_with_valid_data(self):
        response = self.delete_note()
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_notes(self):
        response = self.get_notes()
        assert response.status_code == status.HTTP_200_OK

    def test_get_note_with_valid_pk(self):
        response = self.get_note(self.note.pk)
        assert response.status_code == status.HTTP_200_OK

    def test_get_note_with_fake_pk(self):
        response = self.get_note(1444)  # fake pk
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_new_note_with_valid_data_and_anonymous_user(self):
        self.client.logout()
        response = self.new_note('note title',
                                 'note body',
                                 ["tag: 1", "tag: 2"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_note_with_valid_and_anonymous_user(self):
        self.client.logout()
        response = self.update_put_note('note title',
                                        'note body',
                                        ["tag: 7", "tag: 6"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_note_with_valid_data_and_anonymous_user(self):
        self.client.logout()
        response = self.update_put_note('note title',
                                        'note body',
                                        ["tag: 7", "tag: 6"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_note_with_valid_and_anonymous_user(self):
        self.client.logout()
        response = self.delete_note()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
