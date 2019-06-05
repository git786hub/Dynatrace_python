# AUTOSCRIPT NAME: EX2_CONTR_BUDOA
# CREATEDDATE: 2013-09-16 10:26:58
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-08-12 04:26:35
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

# protect fields in the BU DOA Approval section if contract is approved or if applicability checkbox is unchecked

from psdi.mbo import MboConstants 

if interactive and app in ["PLUSDCONTP"]  :

    curstat = mbo.getString("STATUS")
    if curstat == "APPR"  or curstat == "EXPIRD"  or curstat == "REVISD"  or curstat == "SUSPND"  or curstat == "WSTART" or curstat == "CAN":
        mbo.setFieldFlag("EX2BUDOAREQ", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2BUAPPRDOATYPE", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2BUAPPRDOAAMT", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2PURDESAPPR", MboConstants.READONLY, True)
    elif len(mbo.getString("STATUS")) > 0:            # detect the new record condition where getBoolean will throw an error
        if mbo.getBoolean("EX2BUDOAREQ") :      # BU DOA Approval Required Indicator
            mbo.setFieldFlag("EX2BUAPPRDOATYPE", MboConstants.READONLY, False)
            mbo.setFieldFlag("EX2BUAPPRDOAAMT", MboConstants.READONLY, False)
            mbo.setFieldFlag("EX2PURDESAPPR", MboConstants.READONLY, False)
        else:                                                      # BU DOA Approval Not Required 
            mbo.setFieldFlag("EX2BUAPPRDOATYPE", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2BUAPPRDOAAMT", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2PURDESAPPR", MboConstants.READONLY, True)
    else:       # new record, default for BU DOA approval required is Yes for new contracts, so open the fields
        mbo.setValue("EX2BUDOAREQ",1,MboConstants.NOACCESSCHECK)
        mbo.setFieldFlag("EX2BUAPPRDOATYPE", MboConstants.READONLY, False)
        mbo.setFieldFlag("EX2BUAPPRDOAAMT", MboConstants.READONLY, False)
        mbo.setFieldFlag("EX2PURDESAPPR", MboConstants.READONLY, False)