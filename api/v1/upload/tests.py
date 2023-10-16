import base64

from django.core.files.uploadedfile import SimpleUploadedFile

from api.tests import BaseAPITestCase
from api.v1.upload import urls
from upload.models import Upload


class Create64ClipBoardTestCase(BaseAPITestCase):
    url_name = urls.CREATE_64

    def setUp(self) -> None:
        super().setUp()
        self.content = b"content"

    def test_unauthorized_success(self):
        """Should create an upload even if request is not authorized"""
        base64_content = f"data:text/plain;base64,{base64.b64encode(self.content).decode()}"

        response = self.client.post(
            self.get_url(),
            {
                "name": "test_name.txt",
                "content": base64_content,
            }
        )
        data = response.json()
        upload = Upload.objects.get(id=data.get("id"))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(upload.user, None)
        self.assertTrue(upload.file.size)
        self.assertEqual(upload.file.read(), self.content)

    def test_authorized_success(self):
        """Should create an upload when user is authorized"""
        base64_content = f"data:text/plain;base64,{base64.b64encode(self.content).decode()}"

        response = self.client.post(
            self.get_url(),
            {
                "name": "test_name.txt",
                "content": base64_content,
            },
            headers=self.auth_headers
        )
        data = response.json()
        upload = Upload.objects.get(id=data.get("id"))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(upload.user, self.user)
        self.assertTrue(upload.file.size)
        self.assertEqual(upload.file.read(), self.content)

    def test_bad_data(self):
        """Should return bad response if bad data is provided"""
        base64_content = f"bad data"

        response = self.client.post(
            self.get_url(),
            {
                "name": "test_name.txt",
                "content": base64_content,
            }
        )
        self.assertEqual(response.status_code, 400)

class CreateUploadTestCase(BaseAPITestCase):
    url_name = urls.CREATE

    def setUp(self) -> None:
        super().setUp()
        self.file = SimpleUploadedFile(
            "file.txt",
            b"content"
        )

    def test_unauthorized_success(self):
        """Should create an upload even if request is not authorized"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test name",
                "file": self.file,
            }
        )
        data = response.json()
        upload = Upload.objects.get(id=data.get("id"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(upload.user, None)
        self.assertTrue(upload.file.size)

    def test_authorized_success(self):
        """Should create an upload when user is authorized"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test name",
                "file": self.file,
            },
            headers=self.auth_headers
        )
        data = response.json()
        upload = Upload.objects.get(id=data.get("id"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(upload.user, self.user)
        self.assertTrue(upload.file.size)

    def test_no_file(self):
        """Should return 400 if no file provided"""
        response = self.client.post(
            self.get_url(),
            {
                "name": "test name",
            },
        )
        self.assertEqual(response.status_code, 400)


class RetrieveUpload(BaseAPITestCase):
    url_name = urls.RETRIEVE

    def setUp(self) -> None:
        super().setUp()
        self.upload = Upload.objects.create(
            name="test name",
            media_type=Upload.MediaTypes.DOCUMENT,
            file=SimpleUploadedFile(
                "file.txt",
                b"content"
            ),
            user=self.user
        )
        self.another_clipboard = Upload.objects.create(
            name="another test name",
            media_type=Upload.MediaTypes.DOCUMENT,
            file=SimpleUploadedFile(
                "another_file.txt",
                b"another content"
            ),
            user=self.another_user
        )

    def test_authorized(self):
        """Should return upload if request is authorized and valid id is provided"""
        response = self.client.get(
            self.get_url(id=self.upload.id),
            headers=self.auth_headers
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["id"], str(self.upload.id))

    def test_unauthorized(self):
        """Should return 401 if no credentials are provided"""
        response = self.client.get(
            self.get_url(id=self.upload.id),
        )
        self.assertEqual(response.status_code, 401)

    def test_not_found(self):
        """Should return 404 if non existent id is provided"""
        non_existent_id = 200
        response = self.client.get(
            self.get_url(id=non_existent_id),
            headers=self.auth_headers
        )
        self.assertFalse(Upload.objects.filter(id=non_existent_id).exists())
        self.assertEqual(response.status_code, 404)

    def test_clipboard_of_another_not_found(self):
        """Should return 404 if id of another user is prvided """
        response = self.client.get(
            self.get_url(id=self.another_clipboard.id),
            headers=self.auth_headers
        )
        self.assertNotEqual(self.user, self.another_clipboard.user)
        self.assertTrue(Upload.objects.filter(id=self.upload.id).exists())
        self.assertEqual(response.status_code, 404)


class ListUploadCase(BaseAPITestCase):
    url_name = urls.LIST

    def setUp(self) -> None:
        super().setUp()
        self.n = 10
        self.generate_uploads(self.n)

    def generate_uploads(self, n):
        for i in range(n):
            Upload.objects.create(
                name="test name",
                file=SimpleUploadedFile(
                    "file.txt",
                    b"content"
                ),
                user=self.user if n % 2 == 0 else self.another_user,
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
        self.assertEqual(len(results), Upload.objects.filter(user=self.user).count())
