# AUTOSCRIPT NAME: EX2_CONTR_EXECV
# CREATEDDATE: 2013-09-16 13:45:39
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-08-12 04:28:16
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if interactive and app in ["PLUSDCONTP"] :

    # protect fields in the Contract Executor section if contract is approved or if applicability checkbox is unchecked
    curstat = mbo.getString("STATUS")
    if curstat == "APPR"  or curstat == "EXPIRD"  or curstat == "REVISD"  or curstat == "SUSPND"  or curstat == "WSTART" or curstat == "CAN":
        mbo.setFieldFlag("EX2EXECREQ", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2PUREXECVAPPR", MboConstants.READONLY, True)
    elif len(mbo.getString("STATUS")) > 0:            # detect the new record condition where getBoolean will throw an error
        if mbo.getBoolean("EX2EXECREQ") :      # Contract Executor Approval Required Indicator
            mbo.setFieldFlag("EX2PUREXECVAPPR", MboConstants.READONLY, False)
        else:                                                      # Contract Executor Approval Not Required 
            mbo.setFieldFlag("EX2PUREXECVAPPR", MboConstants.READONLY, True)
    else:       # new record, default for Contract Executor approval required is No for new contracts, so protect the fields
        mbo.setFieldFlag("EX2PUREXECVAPPR", MboConstants.READONLY, True)