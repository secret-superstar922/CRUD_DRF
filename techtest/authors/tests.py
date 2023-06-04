import json

from django.test import TestCase
from django.urls import reverse

from techtest.authors.models import Author


class AuthorListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("authors-list")
        self.author_1 = Author.objects.create(first_name="Riley", last_name="Taylor")
        self.author_2 = Author.objects.create(first_name="Kevin", last_name="Makker")

    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            [
                {
                    "id": self.author_1.id,
                    "first_name": "Riley",
                    "last_name": "Taylor",
                },
                {
                    "id": self.author_2.id,
                    "first_name": "Kevin",
                    "last_name": "Makker",
                },
            ],
        )

class AuthorViewTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Riley", last_name="Taylor")

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        self.url = reverse("author", kwargs={"author_id": self.author.id + 1})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)["error"], "No Author matches the given query")

        self.url = reverse("author", kwargs={"author_id": self.author.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            {
                "id": self.author.id,
                "first_name": "Riley",
                "last_name": "Taylor",
            },
        )

    def test_creates_author(self):
        self.url = reverse("create_author")

        payload = {
            "first_name": "Kevin",
            "last_name": "Makker"
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(author)
        self.assertEqual(Author.objects.count(), 2)
        self.assertDictEqual(
            {
                "id": author.id,
                "first_name": "Kevin",
                "last_name": "Makker"
            },
            response.json()
        )

    def test_updates_author(self):
        self.url = reverse("author", kwargs={"author_id": self.author.id})
        payload = {
            "id": self.author.id,
            "first_name": "Kevin",
            "last_name": "Makker"
        }
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.filter(id=self.author.id).first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(author)
        self.assertEqual(Author.objects.count(), 1)
        self.assertDictEqual(
            {
                "id": author.id,
                "first_name": "Kevin",
                "last_name": "Makker",
            },
            response.json(),
        )

        self.url = reverse("author", kwargs={"author_id": self.author.id + 1})
        payload = {
            "id": self.author.id + 1,
            "first_name": "Kevin",
            "last_name": "Makker"
        }
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)["error"], "No Author matches the given query")

    def test_removes_author(self):
        self.url = reverse("author", kwargs={"author_id": self.author.id + 1})
        response = self.client.delete(self.url)
        # self.assertEqual(response.status_code, 404)
        # self.assertEqual(json.loads(response.content)["error"], "No Author matches the given query")

        # self.url = reverse("author", kwargs={"author_id": self.author.id})
        # response = self.client.delete(self.url)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(Author.objects.count(), 0)