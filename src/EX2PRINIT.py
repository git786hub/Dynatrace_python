# AUTOSCRIPT NAME: EX2PRINIT
# CREATEDDATE: 2013-10-09 16:26:54
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-08-01 02:55:52
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if interactive :

    # HIDE fields in the main tab if user is a contractor - i.e. in user group 3PSCM

    if mbo.getMboSet("EX23PSCMUSERGROUP").count() > 0:
        mbo.setFieldFlag("PRETAXTOTAL", MboConstants.HIDDEN, True)
        mbo.setFieldFlag("TOTALTAX1", MboConstants.HIDDEN, True)
        mbo.setFieldFlag("TOTALCOST", MboConstants.HIDDEN, True)
        mbo.setFieldFlag("TOTALBASECOST", MboConstants.HIDDEN, True)


    # protect fields in the PR object unless user is in BUYER user group

    groupusermbo = mbo.getMboSet("EX2BUYERUSERGROUP")
    if groupusermbo.count() == 0:
        mbo.setFieldFlag("EX2BUYER", MboConstants.READONLY, True)
        mbo.setFieldFlag("INCLUSIVE1", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2FREIGHTTERMS", MboConstants.READONLY, True)
        mbo.setFieldFlag("PAYMENTTERMS", MboConstants.READONLY, True)
        mbo.setFieldFlag("FOB", MboConstants.READONLY, True)
        mbo.setFieldFlag("SHIPVIA", MboConstants.READONLY, True)


    # protect fields in the PR object unless user is in INVENTORY user group

    groupuser2mbo = mbo.getMboSet("EX2INVUSERGROUP_SEC")
    if groupuser2mbo.count() == 0:
        mbo.setFieldFlag("INTERNAL", MboConstants.READONLY, True)