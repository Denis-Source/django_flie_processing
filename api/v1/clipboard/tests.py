from django.core.files.uploadedfile import SimpleUploadedFile

from api.tests import BaseAPITestCase
from api.v1.clipboard import urls
from clipboard.models import ClipBoard


class CreateClipBoardTestCase(BaseAPITestCase):
    url_name = urls.CREATE

    def setUp(self) -> None:
        super().setUp()
        self.file = SimpleUploadedFile(
            "file.txt",
            b"content"
        )

    def test_unauthorized(self):
        """Should create a clipboard even if request is not authorized"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test name",
                "file": self.file,
                "auto_delete": False,

            }
        )
        data = response.json()
        clipboard = ClipBoard.objects.get(id=data.get("id"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(clipboard.user, None)
        self.assertTrue(clipboard.file.size)

    def test_authorized(self):
        """Should create a clipboard when user is authorized"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test name",
                "file": self.file,
                "auto_delete": False,
            },
            headers=self.auth_headers
        )
        data = response.json()
        clipboard = ClipBoard.objects.get(id=data.get("id"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(clipboard.user, self.user)
        self.assertTrue(clipboard.file.size)

    def test_no_file(self):
        """Should return 400 if no file provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test name",
                "auto_delete": False,
            },
        )
        self.assertEqual(response.status_code, 400)


class RetrieveClipBoardTask(BaseAPITestCase):
    url_name = urls.RETRIEVE

    def setUp(self) -> None:
        super().setUp()
        self.clipboard = ClipBoard.objects.create(
            name="test name",
            media_type=ClipBoard.MediaTypes.DOCUMENT,
            file=SimpleUploadedFile(
                "file.txt",
                b"content"
            ),
            user=self.user,
            auto_delete=True
        )
        self.another_clipboard = ClipBoard.objects.create(
            name="another test name",
            media_type=ClipBoard.MediaTypes.DOCUMENT,
            file=SimpleUploadedFile(
                "another_file.txt",
                b"another content"
            ),
            user=self.another_user,
            auto_delete=True
        )

    def test_authorized(self):
        """Should return clipboard if request is authorized and valid id is provided"""
        response = self.client.get(
            self.get_url(id=self.clipboard.id),
            headers=self.auth_headers
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["id"], self.clipboard.id)

    def test_unauthorized(self):
        """Should return 401 if no credentials are provided"""
        response = self.client.get(
            self.get_url(id=self.clipboard.id),
        )
        self.assertEqual(response.status_code, 401)

    def test_not_found(self):
        """Should return 404 if non existent id is provided"""
        non_existent_id = 200
        response = self.client.get(
            self.get_url(id=non_existent_id),
            headers=self.auth_headers
        )
        self.assertFalse(ClipBoard.objects.filter(id=non_existent_id).exists())
        self.assertEqual(response.status_code, 404)

    def test_clipboard_of_another_not_found(self):
        """Should return 404 if id of another user is prvided """
        response = self.client.get(
            self.get_url(id=self.another_clipboard.id),
            headers=self.auth_headers
        )
        self.assertNotEqual(self.user, self.another_clipboard.user)
        self.assertTrue(ClipBoard.objects.filter(id=self.clipboard.id).exists())
        self.assertEqual(response.status_code, 404)


class ListClipBoardTestCase(BaseAPITestCase):
    url_name = urls.LIST

    def setUp(self) -> None:
        super().setUp()
        self.n = 10
        self.generate_clipboards(self.n)

    def generate_clipboards(self, n):
        for i in range(n):
            ClipBoard.objects.create(
                name="test name",
                file=SimpleUploadedFile(
                    "file.txt",
                    b"content"
                ),
                user=self.user if n % 2 == 0 else self.another_user,
                auto_delete=True
            )

    def test_unauthorized(self):
        """Should return 400 if request is not authorized"""
        response = self.client.get(
            self.get_url(),
        )
        self.assertEqual(response.status_code, 401)

    def test_authorized(self):
        """Should return a list of clipboards if request is authorized"""
        response = self.client.get(
            self.get_url(),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        results = response.json().get("results")
        self.assertTrue(results)
        self.assertEqual(len(results), ClipBoard.objects.filter(user=self.user).count())
