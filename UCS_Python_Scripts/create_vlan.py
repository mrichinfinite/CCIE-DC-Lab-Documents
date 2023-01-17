# Create, query and remove VLAN in UCSM

# Imports
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
import creds

# Login to UCSM
handle = UcsHandle(creds.ucsm_vip, creds.username, creds.password)
handle.login()

# Query FabricLanCloud class ID
lan_cloud = handle.query_classid('FabricLanCloud')

# Print the first object of FabricLanCloud
print(lan_cloud[0])

# Create new VLAN object with the name my_vlan_10 and ID 10
my_vlan_10 = FabricVlan(parent_mo_or_dn= lan_cloud[0], name="my_vlan_10", id="10")

# Push the object to UCSM
handle.add_mo(my_vlan_10)

# Commit the change
handle.commit()

# Query UCSM and confirm that the VLAN has been created
print(handle.query_dn("fabric/lan/net-my_vlan_10"))

# Remove the newly created VLAN and commit the change
handle.remove_mo(my_vlan_10)
handle.commit()

# Query for my_vlan_10 to make sure it has been removed successfully; None will be returned
print(handle.query_dn("fabric/lan/net-my_vlan_10"))

# Logout of UCSM
handle.logout()
