#! /usr/bin/env python

import requests
import json

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

# Edit these values
url = 'https://<ip-address-or-hostname>/ins'
username = '<username>'
password = '<password>'

headers = {'content-type': 'application/json'}
payload = {
    'ins_api': {
        'version': '1.0',
        'type': 'cli_show',
        'chunk': '0',
        'sid': '1',
        'input': 'show vlan brief',
        'output_format': 'json',
    }
}
response = requests.post(
    url,
    data=json.dumps(payload),
    headers=headers,
    auth=(username, password),
    verify=False,
).json()

vlan_list = response['ins_api']['outputs']['output']['body'][
    'TABLE_vlanbriefxbrief'
]['ROW_vlanbriefxbrief']

for vlan in vlan_list:
    print('{}'.format(vlan['vlanshowbr-vlanname']))
