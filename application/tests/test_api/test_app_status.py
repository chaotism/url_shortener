from urllib.parse import urljoin

from server.app import app
from httpx import URL
from starlette.testclient import TestClient


class TestSystemStatus:
    prefix = 'health/app_info'
    client = TestClient(app=app)
    client.base_url = URL(urljoin(str(client.base_url), prefix))

    def test_get_status(self):
        response = self.client.post('system-status/')
        assert 'ok' in response.text.lower()


class TestAppVersion:
    prefix = '/health/app_info'
    client = TestClient(app=app)
    client.base_url = URL(urljoin(str(client.base_url), prefix))

    def test_get_version(self):
        response = self.client.post('app-version/')
        assert '0.1' in response.text.lower()
