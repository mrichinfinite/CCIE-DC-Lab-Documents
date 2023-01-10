# Import modules
from cisco import *
from cisco.vrf import *
from cisco.interface import *
from cli import *

# Create VRF and add membership to interface Ethernet1/35
vrf_context = VRF('my-vrf')
vrf_context.create()
vrf_context.add_interface('Ethernet1/35')

# Return newly created VRF ID
print(vrf_context.get_vrf_id_by_name('my-vrf'))

# Add IP address to interface Ethernet1/35 and enable the interface
int_135 = Interface('Ethernet1/35')
int_135.set_ipaddress(ip_address='192.168.100.1', mask=24)
int_135.set_state(s='no shut')

# Add interface Ethernet1/36 to port-channel100 and configure LACP active, then enable the interface
cli('conf t ; int eth1/36 ; channel-group 100 mode active ; no shut')
