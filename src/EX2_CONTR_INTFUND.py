# AUTOSCRIPT NAME: EX2_CONTR_INTFUND
# CREATEDDATE: 2013-09-16 11:47:44
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-08-12 04:24:07
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if app == "PLUSDCONTP" :

    # protect fields in the Internal Funding section Approval if contract is approved or if applicability checkbox is unchecked
    revnum = mbo.getInt("revisionnum")
    if revnum == 0 :
        mbo.setFieldFlag("EX2INFUNDREQ", MboConstants.READONLY, True)

    curstat = mbo.getString("STATUS")
    if curstat == "APPR"  or curstat == "EXPIRD"  or curstat == "REVISD"  or curstat == "SUSPND"  or curstat == "WSTART" or curstat == "CAN":
        mbo.setFieldFlag("EX2INFUNDREQ", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2INFUNDREQAMT", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2INFUNDES", MboConstants.READONLY, True)
    elif len(mbo.getString("STATUS")) > 0:            # detect the new record condition where getBoolean will throw an error
        if mbo.getBoolean("EX2INFUNDREQ") :      # Internal Funding Approval Required Indicator
            mbo.setFieldFlag("EX2INFUNDREQAMT", MboConstants.READONLY, False)
            mbo.setFieldFlag("EX2INFUNDES", MboConstants.READONLY, False)
        else:                                                      # Internal Funding Approval Not Required 
            mbo.setFieldFlag("EX2INFUNDREQAMT", MboConstants.READONLY, True)
            mbo.setFieldFlag("EX2INFUNDES", MboConstants.READONLY, True)
    else:       # new record, default for BU DOA approval required is No for new contracts, so protect the fields
        mbo.setFieldFlag("EX2INFUNDREQAMT", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2INFUNDES", MboConstants.READONLY, True)