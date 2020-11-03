import os
from typing import List, Optional

import ovh  # type: ignore

_domain: str
_client: ovh.Client
domains: List[str]


def __init__():
    global _domain, _client, domains

    print(os.environ)
    _domain = os.environ.get("domain", "")
    _client = ovh.Client(
        endpoint=os.environ.get("endpoint"),
        application_key=os.environ.get("application_key"),
        application_secret=os.environ.get("application_secret"),
        consumer_key=os.environ.get("consumer_key"),
    )
    domains = os.environ.get("sub_domains", "").split(",")


def get_domain_ip() -> Optional[str]:
    records = _client.get(
        f"/domain/zone/{_domain}/record", fieldType="A", subDomain=domains[0]
    )
    record = _client.get(f"/domain/zone/{_domain}/record/{records[0]}")
    record_ip: str = record["target"]
    return record_ip


def update_domain(sub_domain: str, current_ip: str):
    records = _client.get(
        f"/domain/zone/{_domain}/record", fieldType="A", subDomain=sub_domain
    )
    _client.put(f"/domain/zone/{_domain}/record/{records[0]}", target=current_ip)


def update_all_sub_domain(current_ip: str):
    for d in domains:
        update_domain(d, current_ip)


if __name__ == "__main__":
    print(get_domain_ip())
