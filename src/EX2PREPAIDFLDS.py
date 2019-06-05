# AUTOSCRIPT NAME: EX2PREPAIDFLDS
# CREATEDDATE: 2013-12-04 12:56:04
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-04-16 10:22:58
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if interactive and len(mbo.getString("STATUS")) > 0:            # check status to avoid the new record condition where getBoolean will throw an error
    # protect fields (in the invoice app) when the prepaid chekbox is unchecked
    ivstatset = mbo.getMboSet("STATUSDESC")
    ivstat = ivstatset.getMbo(0)
    if mbo.getBoolean("EX2PREPAID") and not ivstat.getString("maxvalue") in ["APPR","PNDREV","REVERSED"] :      # Invoice Prepaid Indicator, internal status value
        mbo.setFieldFlag("checkcode", MboConstants.READONLY, False)
        mbo.setFieldFlag("checknum", MboConstants.READONLY, False)
        mbo.setFieldFlag("ex2bank", MboConstants.READONLY, False)
        mbo.setFieldFlag("bankaccount", MboConstants.READONLY, False)
        mbo.setFieldFlag("paiddate", MboConstants.READONLY, False)
        mbo.setFieldFlag("checkcode", MboConstants.REQUIRED, True)
        mbo.setFieldFlag("checknum", MboConstants.REQUIRED, True)
        mbo.setFieldFlag("ex2bank", MboConstants.REQUIRED, True)
        mbo.setFieldFlag("bankaccount", MboConstants.REQUIRED, True)
        mbo.setFieldFlag("paiddate", MboConstants.REQUIRED, True)
    else:
        # only clear the values when running from the lauchpoint where the user unchecked the checkbox
        if launchPoint == "EX2PREPAID" :
            mbo.setValueNull("checkcode", MboConstants.NOACCESSCHECK)
            mbo.setValueNull("checknum", MboConstants.NOACCESSCHECK)
            mbo.setValueNull("ex2bank", MboConstants.NOACCESSCHECK)
            mbo.setValueNull("bankaccount", MboConstants.NOACCESSCHECK)
            mbo.setValueNull("paiddate", MboConstants.NOACCESSCHECK)
        mbo.setFieldFlag("checkcode", MboConstants.READONLY, True)
        mbo.setFieldFlag("checknum", MboConstants.READONLY, True)
        mbo.setFieldFlag("ex2bank", MboConstants.READONLY, True)
        mbo.setFieldFlag("bankaccount", MboConstants.READONLY, True)
        mbo.setFieldFlag("paiddate", MboConstants.READONLY, True)
        mbo.setFieldFlag("checkcode", MboConstants.REQUIRED, False)
        mbo.setFieldFlag("checknum", MboConstants.REQUIRED, False)
        mbo.setFieldFlag("ex2bank", MboConstants.REQUIRED, False)
        mbo.setFieldFlag("bankaccount", MboConstants.REQUIRED, False)
        mbo.setFieldFlag("paiddate", MboConstants.REQUIRED, False)