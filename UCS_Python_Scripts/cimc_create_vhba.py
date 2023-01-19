# Create, query and remove vHBA in CIMC

# Imports
from imcsdk.mometa.adaptor.AdaptorHostFcIf import AdaptorHostFcIf
from imcsdk.imchandle import ImcHandle
import imc_creds

# Login to CIMC
handle = ImcHandle(imc_creds.cimc_ip, imc_creds.username, imc_creds.password)
handle.login()

# Query AdaptorHostFcIf class ID
fc_adaptor = handle.query_classid('AdaptorHostFcIf')

# Print the first object of AdaptorHostFcIf
print(fc_adaptor[0])

# Declare vHBA
vhba = AdaptorHostFcIf(parent_mo_or_dn='sys/rack-unit-1/adaptor-1',
                        name='fc2', san_boot='disabled', wwnn='10:00:84:3D:C6:4D:2C:BA',
                        wwpn='20:00:84:3D:C6:4D:2C:BA')

# Push the object to CIMC
handle.add_mo(vhba)

# Commit the change
# handle.commit()

# Query CIMC and confirm that the vHBA has been created
print(handle.query_dn('sys/rack-unit-1/adaptor-1/host-fc-fc2'))

# Remove the newly created vHBA and commit the change
handle.remove_mo(vhba)
# handle.commit()

# Query for the vHBA to make sure it has been removed successfully; None will be returned
print(handle.query_dn('sys/rack-unit-1/adaptor-1/host-fc-fc2'))

# Logout of CIMC
handle.logout()