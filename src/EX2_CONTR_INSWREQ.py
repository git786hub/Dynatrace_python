# AUTOSCRIPT NAME: EX2_CONTR_INSWREQ
# CREATEDDATE: 2013-09-16 11:20:50
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-08-12 04:25:59
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if interactive and app in ["PLUSDCONTP"] :

    # protect fields in the Insurance Waiver section if contract is approved or if applicability checkbox is unchecked
    curstat = mbo.getString("STATUS")
    if curstat == "APPR"  or curstat == "EXPIRD"  or curstat == "REVISD"  or curstat == "SUSPND"  or curstat == "WSTART" or curstat == "CAN":
        mbo.setFieldFlag("EX2INSREQIND", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2PURINSWAPPR", MboConstants.READONLY, True)
    elif len(mbo.getString("STATUS")) > 0:            # detect the new record condition where getBoolean will throw an error
        if mbo.getBoolean("EX2INSREQIND") :      # Insurance Waiver Approval Required Indicator
            mbo.setFieldFlag("EX2PURINSWAPPR", MboConstants.READONLY, False)
        else:                                                      # Insurance Waiver Not Required 
            mbo.setFieldFlag("EX2PURINSWAPPR", MboConstants.READONLY, True)
    else:       # new record, default for Insurance Waiver approval required is No for new contracts, so protect the fields
        mbo.setFieldFlag("EX2PURINSWAPPR", MboConstants.READONLY, True)