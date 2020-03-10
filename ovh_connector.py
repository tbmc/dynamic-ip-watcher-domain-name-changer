import os
import ovh

__domain = os.environ.get("domain", "")
__client = ovh.Client(
    endpoint=os.environ.get("endpoint"),
    application_key=os.environ.get("application_key"),
    application_secret=os.environ.get("application_secret"),
    consumer_key=os.environ.get("consumer_key"),
)


def get_domain_ip() -> str:
    records = __client.get(f"/domain/zone/{__domain}/record", fieldType="A", subDomain="")
    record = __client.get(f"/domain/zone/{__domain}/record/{records[0]}")
    record_ip = record["target"]
    return record_ip


def update_domain(sub_domain: str, current_ip: str):
    records = __client.get(f"/domain/zone/{__domain}/record", fieldType="A", subDomain=sub_domain)
    __client.put(f"/domain/zone/{__domain}/record/{records[0]}", target=current_ip)


def update_all_sub_domain(current_ip: str):
    domains = os.environ.get("sub_domains", "").split(",")
    for d in domains:
        update_domain(d, current_ip)


if __name__ == '__main__':
    print(get_domain_ip())

