# AUTOSCRIPT NAME: EX2PRLINEQQUNITCOST
# CREATEDDATE: 2014-01-23 12:19:29
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-01-23 12:24:55
# CHANGEBY: UUYC
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants

if not mbo.getMboValue("EX2QUICKQUOTEIND").isNull(): 
    unitcost=ex2qqunitcost