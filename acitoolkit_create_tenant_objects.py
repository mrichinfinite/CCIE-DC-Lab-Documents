# Imports
from creds import *
from acitoolkit.acitoolkit import *
import json

# Create session with APIC
session = Session(URL, USERNAME, PASSWORD)
session.login()

# Create Tenant and VRF
tenant_name = "Test"
tenant = Tenant(tenant_name)
vrf = Context("Test-VRF", tenant)

# Create Bridge Domain and associate VRF to it
bridge_domain = BridgeDomain("Test-BD", tenant)
bridge_domain.add_context(vrf)

# Create subnet
subnet = Subnet("Test-Subnet", bridge_domain)
subnet.set_addr("192.168.10.1/24")

# Create ICMP filter and filter entry
filter_icmp = Filter("icmp", tenant)
filter_entry_icmp = FilterEntry("icmp", filter_icmp, etherT="ip", prot="icmp")

# Create HTTP filter and filter entry
filter_http = Filter("http", tenant)
filter_entry_tcp80 = FilterEntry("tcp-80", filter_http, etherT="ip", prot="tcp", dFromPort="http", dToPort="http")

# Create ICMP contract and associate to ICMP filter
contract_icmp = Contract("icmp", tenant)
contract_subject_icmp = ContractSubject("icmp", contract_icmp)
contract_subject_icmp.add_filter(filter_icmp)

# Create HTTP contract and associate to HTTP filter
contract_http = Contract("http", tenant)
contract_subject_http = ContractSubject("http", contract_http)
contract_subject_http.add_filter(filter_http)

# Create Application Profile
app_profile = AppProfile("Test-App", tenant)

# Create Test 1 EPG and associate to bridge domain and contracts
epg_test_1 = EPG("Test-1", app_profile)
epg_test_1.add_bd(bridge_domain)
epg_test_1.provide(contract_http)
epg_test_1.consume(contract_icmp)

# Create Test 2 EPG and associate to bridge domain and contracts
epg_test_2 = EPG("Test-2", app_profile)
epg_test_2.add_bd(bridge_domain)
epg_test_2.provide(contract_icmp)
epg_test_2.consume(contract_http)

# Collect list of tenants
tenant_list = Tenant.get(session)

# Print list of tenants
tenant_list
for tn in tenant_list:
    print(tn.name)

# Print URL and configuration data
print("\n{}\n\n{}".format(tenant.get_url(), tenant.get_json()))

# Print configuration data as JSON
print(json.dumps(tenant.get_json(), sort_keys=True, indent=2, separators=(',',':')))

# Push configuration to APIC
resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())

# Test configuration request
if resp.ok:
     print("\n{}: {}\n\n{} is ready for use".format(resp.status_code, resp.reason, tenant.name))
else:
     print("\n{}: {}\n\n{} was not created!\n\n Error: {}".format(resp.status_code, resp.reason, subnet.name, resp.content))

# Re-check tenant list
new_tenant_list = Tenant.get(session)
for tn in new_tenant_list:
    print(tn.name)

# Check app list in new tenant
app_list = AppProfile.get(session, tenant)
for app in app_list:
    print(app.name)

# Check EPG list in new app
epg_list = EPG.get(session, app_profile, tenant)
for epg in epg_list:
    print(epg.name)

# exit
exit()