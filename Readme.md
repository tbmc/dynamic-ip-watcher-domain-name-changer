[![pipeline status](https://gitlab.com/tbmc/dynamic-ip-watcher-domain-name-changer-clone/badges/master/pipeline.svg)](https://gitlab.com/tbmc/dynamic-ip-watcher-domain-name-changer-clone/-/commits/master)


# Generate OVH credential for API

[Link](https://api.ovh.com/createToken/index.cgi?GET=%2F*&PUT=%2F*&POST=%2F*&DELETE=%2F)


# Environment variables

- domain: domain name in ovh (i.e. google.fr)
- sub_domains (i.e. "test,ping," if there is an ending coma, it will update domain without sub_domain).
  The first sub domain will be used to check the current IP.
- timer: default to 30 (in seconds)

## OVH

- endpoint
- application_key
- application_secret
- consumer_key

