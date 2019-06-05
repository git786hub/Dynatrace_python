# AUTOSCRIPT NAME: EX2PCONTSTATUS
# CREATEDDATE: 2013-10-16 09:10:17
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-10-16 09:46:59
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# set external rev to zero for new draft contracts
from psdi.mbo import MboConstants 

curstat = mbo.getString("STATUS")
if onadd and curstat == "DRAFT":
    mbo.setFieldFlag("EX2CONTEXREV", MboConstants.READONLY, False)
    mbo.setValue("EX2CONTEXREV", 0)
    mbo.setFieldFlag("EX2CONTEXREV", MboConstants.READONLY, True)