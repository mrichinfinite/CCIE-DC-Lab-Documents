# Obtain basic information about blade servers from UCSM

# Imports
from ucsmsdk.ucshandle import UcsHandle
import pandas as pd
from tabulate import tabulate
import creds

# Login to UCSM
handle = UcsHandle(creds.ucsm_vip, creds.username, creds.password)
handle.login()

# Query computeBlade class ID
blades = handle.query_classid('computeBlade')

# Retrieve information about blade servers and render into a dataframe
for blade in blades:
    df = pd.DataFrame({'DN': [blade.dn], 
            'Overall Status': [blade.oper_state], 
            'Admin State': [blade.admin_state], 
            'Discovery State': [blade.discovery], 
            'Avail State': [blade.availability], 
            'Assoc State': [blade.association], 
            'Power State': [blade.oper_power], 
            'Check Point': [blade.check_point]}, index=['Info'])

    # Print the dataframe
    print(tabulate(df, headers='keys', tablefmt='psql'))

# Logout of UCSM
handle.logout()
