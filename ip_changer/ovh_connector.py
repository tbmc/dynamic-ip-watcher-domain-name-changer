import os
import ovh  # type: ignore
from typing import Optional, List

__domain: str
__client: ovh.Client
domains: List[str]


def __init__():
    global __domain, __client, domains
    __domain = os.environ.get("domain", "")
    __client = ovh.Client(
        endpoint=os.environ.get("endpoint"),
        application_key=os.environ.get("application_key"),
        application_secret=os.environ.get("application_secret"),
        consumer_key=os.environ.get("consumer_key"),
    )
    domains = os.environ.get("sub_domains", "").split(",")


def get_domain_ip() -> Optional[str]:
    records = __client.get(
        f"/domain/zone/{__domain}/record", fieldType="A", subDomain=domains[0]
    )
    record = __client.get(f"/domain/zone/{__domain}/record/{records[0]}")
    record_ip: str = record["target"]
    return record_ip


def update_domain(sub_domain: str, current_ip: str):
    records = __client.get(
        f"/domain/zone/{__domain}/record", fieldType="A", subDomain=sub_domain
    )
    __client.put(f"/domain/zone/{__domain}/record/{records[0]}", target=current_ip)


def update_all_sub_domain(current_ip: str):
    for d in domains:
        update_domain(d, current_ip)


if __name__ == "__main__":
    print(get_domain_ip())