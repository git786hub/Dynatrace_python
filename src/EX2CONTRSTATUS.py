# AUTOSCRIPT NAME: EX2CONTRSTATUS
# CREATEDDATE: 2013-10-15 08:44:04
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:03:09
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# Verify Owner populated before contract is approved 
from psdi.mbo import MboConstants 

def setError():
        global errorkey,errorgroup,params
        errorkey='ex2_ownernull'
        errorgroup='contract'

curstat = mbo.getString("STATUS")
if curstat == "APPR"  and mbo.isNull("EX2CONTOWN"):
    setError()