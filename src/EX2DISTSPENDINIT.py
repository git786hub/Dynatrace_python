# AUTOSCRIPT NAME: EX2DISTSPENDINIT
# CREATEDDATE: 2014-02-17 15:14:38
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:03:19
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if not onadd:
    mbo.setFieldFlag("ex2primvendor", MboConstants.READONLY, True)
    mbo.setFieldFlag("ex2scndvendor", MboConstants.READONLY, True)