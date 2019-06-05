# AUTOSCRIPT NAME: EX2CONT2POXOVER
# CREATEDDATE: 2013-11-04 15:11:47
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:03:02
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

#mbo.setValue("description", "one")
#if not mbo.isNull("contractrefnum") :
#    mbo.setValue("description", mbo.getString("description") + " " + mbo.getString("contractrefnum") + " ")
#if not mbo.isNull("contractrefid") :
#    mbo.setValue("description", mbo.getString("description") + " " + str(mbo.getInt("contractrefid")) + " ")
contset = mbo.getMboSet("PURCHVIEW")
if contset.count() > 0 :
    contmbo = contset.getMbo(0)
    mbo.setValue("purchaseagent", contmbo.getString("purchaseagent"))