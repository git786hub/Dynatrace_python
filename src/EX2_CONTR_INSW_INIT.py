# AUTOSCRIPT NAME: EX2_CONTR_INSW_INIT
# CREATEDDATE: 2013-09-17 13:49:52
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-02-25 10:21:57
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# protect fields in the main tab if contract is approved 
from psdi.mbo import MboConstants 
from psdi.app.contract.purch import PurchViewRemote

if app == "PLUSDCONTP" :

    contrmbo = mbo.getOwner()
    if isinstance(contrmbo,PurchViewRemote):

        curstat = contrmbo.getString("STATUS")
        #noinsappr = contrmbo.isNull("EX2PURINSWAPPR")
        if curstat == "APPR"  or curstat == "EXPIRD"  or curstat == "REVISD"  or curstat == "SUSPND"  or curstat == "WSTART" :    # or    noinsappr:
            mbo.setFieldFlag("EX2INSWCAT", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2REASON", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2INSWONC", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2INSWSUP", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2INSREQID", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2INSREQDATE", MboConstants.READONLY, True)