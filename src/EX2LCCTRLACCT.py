# AUTOSCRIPT NAME: EX2LCCTRLACCT
# CREATEDDATE: 2014-04-30 10:00:54
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:18:59
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
from psdi.mbo import SqlFormat

sqf = SqlFormat("orgid=:1 and DFLTGROUP=:2 and GROUPVALUE=:3");
sqf.setObject(1,"ACCOUNTDEFAULTS","ORGID", mbo.getString("orgid"));
sqf.setObject(2,"ACCOUNTDEFAULTS","DFLTGROUP", "LABORREC");
sqf.setObject(3,"ACCOUNTDEFAULTS","GROUPVALUE", "LABORRECACCT");

accountDefaultsSet = mbo.getMboSet("$ACCOUNTDEFAULS","ACCOUNTDEFAULTS", sqf.format());
if accountDefaultsSet.count() > 0 :
    accLContAccMbo = accountDefaultsSet.getMbo(0)
    mbo.setValue("controlaccount",accLContAccMbo.getString("GLDefault"),MboConstants.NOACCESSCHECK);