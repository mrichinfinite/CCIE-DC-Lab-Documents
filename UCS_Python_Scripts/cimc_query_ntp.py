# Query NTP from CIMC

# Imports
from imcsdk.imchandle import ImcHandle
import imc_creds

# Login to CIMC
handle = ImcHandle(imc_creds.cimc_ip, imc_creds.username, imc_creds.password)
handle.login()

# Query the CommNtpProvider class ID
ntp = handle.query_classid('CommNtpProvider')

# Print the results
print(ntp[0])

# Logout of CIMC
handle.logout()