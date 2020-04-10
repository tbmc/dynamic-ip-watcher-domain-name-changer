import os
import signal
from threading import Timer
import requests

from ovh_connector import get_domain_ip, update_all_sub_domain

IPIFY_URL = "https://api.ipify.org"

time = int(os.environ.get("timer", 30))
current_timer: Timer


def timer_killer():
    if current_timer is not None:
        current_timer.cancel()


signal.signal(signal.SIGINT, timer_killer)  # type: ignore
signal.signal(signal.SIGTERM, timer_killer)  # type: ignore


def launch_timer():
    global current_timer
    current_timer = Timer(time, timer_fn)
    current_timer.start()


def timer_fn():
    try:
        launch_timer()
        check_ip()
    except:
        pass


def get_ip_ipify() -> str:
    return requests.get(IPIFY_URL).text


def check_ip():
    current_ip = get_ip_ipify()
    domain_ip = get_domain_ip()
    print(f"Current IP: {current_ip} ?= Domain IP: {domain_ip}")
    if current_ip != domain_ip:
        print(f"Old IP: {domain_ip} => New IP: {current_ip}")
        update_all_sub_domain(current_ip)


if __name__ == "__main__":
    launch_timer()
    check_ip()
