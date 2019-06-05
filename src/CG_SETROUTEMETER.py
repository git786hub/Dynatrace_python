# AUTOSCRIPT NAME: CG_SETROUTEMETER
# CREATEDDATE: 2012-07-24 08:34:22
# CREATEDBY: UHD0
# CHANGEDATE: 2014-05-13 06:18:09
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

routemeterset = None
assetmeterset = None
locmeterset = None

print mbo.getString("ROUTE")
print mbo.getString("ROUTESTOPID")

routemeterset = mbo.getMboSet("CG_ROUTEMETER")

assetmeterset = mbo.getMboSet("CG_ROUTEASSETMETER")

for i in range (assetmeterset.count()) :
    routemeter = routemeterset.add()
    assetmeter = assetmeterset.getMbo(i)
    routemeter.setValue("METER",assetmeter.getString("METERNAME"),MboConstants.NOACCESSCHECK)
    routemeter.setValue("WONUM",mbo.getString("WONUM"),MboConstants.NOACCESSCHECK)
    routemeter.setValue("SITEID",mbo.getString("SITEID"),MboConstants.NOACCESSCHECK)
    routemeter.setValue("ASSETNUM",assetmeter.getString("ASSETNUM"),MboConstants.NOACCESSCHECK)

locmeterset = mbo.getMboSet("CG_ROUTELOCMETER")

for j in range (locmeterset.count()) :
    routemeter = routemeterset.add()
    locmeter = locmeterset.getMbo(j)
    routemeter.setValue("METER",locmeter.getString("METERNAME"),MboConstants.NOACCESSCHECK)
    routemeter.setValue("WONUM",mbo.getString("WONUM"),MboConstants.NOACCESSCHECK)
    routemeter.setValue("SITEID",mbo.getString("SITEID"),MboConstants.NOACCESSCHECK)
    routemeter.setValue("LOCATION",locmeter.getString("LOCATION"),MboConstants.NOACCESSCHECK)



if (routemeterset is not None and not routemeterset.isEmpty()) :
   routemeterset.close()
   

if (assetmeterset is not None and not assetmeterset.isEmpty()) :
   assetmeterset.close()
   
if (locmeterset is not None and not locmeterset.isEmpty()) :
   locmeterset.close()