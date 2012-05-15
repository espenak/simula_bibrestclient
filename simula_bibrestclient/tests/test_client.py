from unittest import TestCase

from simula_bibrestclient.client import urljoin


class TestClient(TestCase):
    def test_urljoin(self):
        self.assertEquals(urljoin('https://simula.no/publications/', '@@rest'),
                          'https://simula.no/publications/@@rest')
        self.assertEquals(urljoin('https://simula.no/publications', '@@rest'),
                          'https://simula.no/publications/@@rest')
        self.assertEquals(urljoin('https://simula.no/publications', 'hello', 'world', '@@rest'),
                          'https://simula.no/publications/hello/world/@@rest')
