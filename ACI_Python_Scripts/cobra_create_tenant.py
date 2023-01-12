# Imports
import cobra.mit.access
import cobra.mit.request
import cobra.mit.session
import cobra.model.fv
import cobra.model.pol
import cobra.model.vns
from cobra.internal.codec.xmlcodec import toXMLStr
import sys
from creds import *

# Count args
args = len(sys.argv)

# Log into APIC and create dir object
ls = cobra.mit.session.LoginSession(URL, USERNAME, PASSWORD)
md = cobra.mit.access.MoDirectory(ls)
md.login()

# Top level object on which operations will be made
polUni = cobra.model.pol.Uni('')

# Build the request and take new Tenant name as argument
for i in range(1, args):
    fvTenant = cobra.model.fv.Tenant(polUni, ownerkey='', name=sys.argv[i], descr='', userdom=':all:', nameAlias='', OwnerTag='', annotation='')
    vnsSvcCont = cobra.model.vns.SvcCont(fvTenant, userdom=':all:', annotation='')
    fvRsTenantMonPol = cobra.model.fv.RsTenantMonPol(fvTenant, userdom=':all:', annotation='', tnMonEPGPolName='')

# Commit generated code to APIC
print(toXMLStr(polUni))
c = cobra.mit.request.ConfigRequest()
c.addMo(polUni)
md.commit(c)
