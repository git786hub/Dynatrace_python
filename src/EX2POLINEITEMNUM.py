# AUTOSCRIPT NAME: EX2POLINEITEMNUM
# CREATEDDATE: 2014-05-02 10:00:43
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:19:18
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote

if onadd and not mbo.isNull("linetype") and not mbo.isNull("itemnum") :
  if mbo.getString("linetype") == "STDSERVICE" and mbo.getString("itemnum") == "FREIGHT" :
        siteset = mbo.getMboSet("EX2SITE")
        if siteset.count() > 0 :
            sitembo = siteset.getMbo(0)
            mbo.setValue("GLDEBITACCT", sitembo.getString("EX2FREIGHTACCT"),MboConstants.NOACCESSCHECK)