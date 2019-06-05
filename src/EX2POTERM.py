# AUTOSCRIPT NAME: EX2POTERM
# CREATEDDATE: 2014-05-08 16:38:11
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-04-19 20:07:59
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote

#Set POTERM Siteid to PO Site id, rather than integration user default siteid
if not interactive and onadd:
 pombo=mbo.getOwner()
 if pombo and isinstance(pombo,PORemote) and pombo.getString("sourcesysid") in ["PTR","TED"]:
  posite=pombo.getString("SITEID")
  mbo.setValue("SITEID", posite,MboConstants.NOACCESSCHECK)