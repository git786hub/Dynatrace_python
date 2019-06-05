# AUTOSCRIPT NAME: EX2_CONTR_ONINIT
# CREATEDDATE: 2013-09-17 11:30:00
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-12-01 04:57:34
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if app == "PLUSDCONTP" :

    # protect all when it is in BUPEND or BUAPPR
    # Commented the below readonly code to fix the Incident: INC000000941040
    # if mbo.getString("STATUS") in ["BUAPPR", "BUPEND" ] : 
        # mbo.setFlag(MboConstants.READONLY, True)   #  set object readonly

    if not onadd:
        buyergroupuser = mbo.getMboSet("EX2BUYERUSERGROUP")
        if buyergroupuser.count() == 0:
            mbo.setFlag(MboConstants.READONLY, True) 

    # protect fields in the main tab if contract is approved 
    curstat = mbo.getString("STATUS")
    if curstat == "APPR"  or curstat == "EXPIRD"  or curstat == "REVISD"  or curstat == "SUSPND"  or curstat == "WSTART" or curstat == "CAN":
        mbo.setFieldFlag("EX2CONTEXREV", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2CONTOWN", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2FREIGHTTERMS", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2CONTCOOR", MboConstants.READONLY, True)

    # protect external revision in the main tab if user not in the Buyer group (or on rev 0) 
    elif onadd:
            mbo.setFieldFlag("EX2CONTEXREV", MboConstants.READONLY, False)
    else:
        groupusermbo = mbo.getMboSet("EX2BUYERUSERGROUP")
        if groupusermbo.count() == 0:
            mbo.setFieldFlag("EX2CONTEXREV", MboConstants.READONLY, True)
        if mbo.getInt("REVISIONNUM") == 0:
            mbo.setFieldFlag("EX2CONTEXREV", MboConstants.READONLY, True)

    # HIDE fields in the main tab if user is a contractor - i.e. in user group 3PSCM
    if not onadd and mbo.getMboSet("EX23PSCMUSERGROUP").count() > 0:
        mbo.setFieldFlag("TOTALCOST", MboConstants.HIDDEN, True)
        mbo.setFieldFlag("MAXVOL", MboConstants.HIDDEN, True)

mbo.setFieldFlag("MAXVOL", MboConstants.READONLY, False)
#mbo.setFieldFlag("MAXRELVOL", MboConstants.READONLY, False)