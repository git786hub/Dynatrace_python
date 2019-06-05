# AUTOSCRIPT NAME: EX2TRAPDUPINVCS
# CREATEDDATE: 2014-09-30 00:50:14
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-09-30 00:50:14
# CHANGEBY: UM1R
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 

def setError():
        global errorkey,errorgroup,params
        errorkey='ex2_dupinvoice'
        errorgroup='invoice'

dupinvmboset = mbo.getMboSet("ex2dupinvoice")
if  dupinvmboset.count() > 0 :
    setError()