import os
import unittest
from unittest.mock import call, patch

environ = {
    "endpoint": "endpoint",
    "application_key": "application_key",
    "application_secret": "application_secret",
    "consumer_key": "consumer_key",
}

os.environ = {  # type: ignore
    **os.environ,
    **environ,
    "domain": "domain",
    "sub_domains": "domain1,domain2",
}


class MockClient:
    ovh_client_test = True

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get(self, url, fieldType=None, subDomain=None):
        pass

    def put(self, url, target):
        pass


with patch("ovh.Client", MockClient):
    from ip_changer import ovh_connector

    ovh_connector.__init__()
    assert ovh_connector._domain == "domain"
    assert ovh_connector._client.ovh_client_test
    for key, value in environ.items():
        assert ovh_connector._client.kwargs[key] == value
    assert ovh_connector.domains == ["domain1", "domain2"]


@patch("ip_changer.ovh_connector._client.get")
class TestGetDomainIp(unittest.TestCase):
    def test_get_domain_ip(self, client):
        client.return_value = {0: "first", "target": "target"}
        record_ip = ovh_connector.get_domain_ip()
        for mock_call in (
            call("/domain/zone/domain/record", fieldType="A", subDomain="domain1"),
            call("/domain/zone/domain/record/first"),
        ):
            assert mock_call in client.mock_calls
        self.assertEqual("target", record_ip)


@patch("ip_changer.ovh_connector._client.put")
@patch("ip_changer.ovh_connector._client.get")
class TestUpdateDomain(unittest.TestCase):
    def test_update_domain(self, client_get, client_put):
        client_get.return_value = ["record1"]
        ovh_connector.update_domain("subDomain", "current_ip")
        client_put.assert_called_with(
            "/domain/zone/domain/record/record1", target="current_ip"
        )


@patch("ip_changer.ovh_connector.update_domain")
class TestUpdateAllSubDomain(unittest.TestCase):
    def test_update_all_sub_domain(self, update):
        ovh_connector.update_all_sub_domain("current_ip")
        assert update.mock_calls == [
            call("domain1", "current_ip"),
            call("domain2", "current_ip"),
        ]
