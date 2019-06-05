# AUTOSCRIPT NAME: EX2INVOICESERVPO
# CREATEDDATE: 2013-12-10 13:02:03
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-02-10 10:49:13
# CHANGEBY: UUYC
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

# Ensure E-Pay Invoices are not for Service POs
def setError():
        global errorkey,errorgroup,params
        errorkey='ex2_servPOinvoice'
        errorgroup='invoice'

if mbo.getString("SOURCESYSID") == "EPAY":
    pomboset = mbo.getMboSet("INVC_PO")
    if pomboset.count() > 0:
        pombo = pomboset.getMbo(0)
        if pombo.getBoolean("EX2SERVICEPO"):
            setError()