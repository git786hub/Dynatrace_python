# AUTOSCRIPT NAME: CG_SETGLORGCODE
# CREATEDDATE: 2012-07-21 09:22:07
# CREATEDBY: UHD0
# CHANGEDATE: 2012-07-21 11:01:14
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import GLFormat
from psdi.mbo import MboConstants

orgcodemboset = mbo.getMboSet("LOCATIONS.CG_WORKCENTERORGCODE")

if orgcodemboset.count() > 0 :
    orgcodembo = orgcodemboset.getMbo(0)
    locmboset = mbo.getMboSet("CHILDLOCATIONS")
    if locmboset.count() > 0 :
        locmbo = locmboset.getMbo(0)

        newGLString = "?????-" + orgcodembo.getString("ORGCODE") + "-???????-???-????????-????-????"
        fmt = GLFormat(newGLString, locmbo.getString("orgid"))
        fmt.mergeString(locmbo.getString("GLAccount"))

        locmbo.setValue ("GLACCOUNT", fmt.toDisplayString(),MboConstants.NOACCESSCHECK)