import io
import unittest
from unittest.mock import Mock, patch, call
import signal

with patch("ovh.Client"), patch("signal.signal") as signal_mock:
    import ip_listener

    assert signal_mock.mock_calls == [
        call(signal.SIGINT, ip_listener.timer_killer),
        call(signal.SIGTERM, ip_listener.timer_killer),
    ]


class TestGlobalVariables(unittest.TestCase):
    def test_ipify_url(self):
        self.assertEqual(ip_listener.IPIFY_URL, "https://api.ipify.org")

    def test_time(self):
        self.assertEqual(ip_listener.time, 30)


class TestIpListenerTimerKiller(unittest.TestCase):
    def test_timer_not_defined(self):
        ip_listener.current_timer = None  # type: ignore
        try:
            ip_listener.timer_killer()
        except:
            self.fail("Should not fail")

    def test_timer_defined(self):
        timer = Mock()
        ip_listener.current_timer = timer
        ip_listener.timer_killer()
        timer.cancel.assert_called()


class TestLaunchTimer(unittest.TestCase):
    def test_launch_timer(self):
        class TestTimer:
            def __init__(self, time: int, fn):
                assert time == 30
                assert fn == ip_listener.timer_fn

            def start(self):
                pass

        ip_listener.current_timer = None  # type: ignore
        with patch("ip_listener.Timer", TestTimer) as timer:
            timer.start = Mock()
            timer.start.return_value = "start"
            ip_listener.launch_timer()
            timer.start.assert_called()
        self.assertEqual("start", ip_listener.current_timer)


class TestGetIpIpify(unittest.TestCase):
    def test_ip_ipify(self):
        class RequestGetReturn:
            text = "text"

        with patch("requests.get", return_value=RequestGetReturn()) as requests_get:
            self.assertEqual("text", ip_listener.get_ip_ipify())
            requests_get.assert_called_with(ip_listener.IPIFY_URL)


@patch("sys.stdout", new_callable=io.StringIO)
@patch("ip_listener.update_all_sub_domain")
@patch("ip_listener.get_domain_ip")
@patch("ip_listener.get_ip_ipify")
class TestCheckIp(unittest.TestCase):
    def test_same_ip(self, ipify, domain_ip, update_all, stdout):
        ipify.return_value = "ip"
        domain_ip.return_value = "ip"
        ip_listener.check_ip()
        assert not update_all.called
        assert "Current IP: ip ?= Domain IP: ip" in stdout.getvalue()

    def test_different_ip(self, ipify, domain_ip, update_all, stdout):
        ipify.return_value = "new_ip"
        domain_ip.return_value = "ip"
        ip_listener.check_ip()
        update_all.assert_called_with("new_ip")
        assert "Current IP: new_ip ?= Domain IP: ip" in stdout.getvalue()
        assert "Old IP: ip => New IP: new_ip" in stdout.getvalue()
