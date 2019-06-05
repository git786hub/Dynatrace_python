# AUTOSCRIPT NAME: IMPORTASSET
# CREATEDDATE: 2014-10-12 09:57:32
# CREATEDBY: UVX3
# CHANGEDATE: 2014-10-12 10:05:53
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.asset import AssetRemote

print "SASASASA - in UPDATEDESC script"

aassetMboSet= mbo.getThisMboSet()
print "SASASASA - got mboset"

print "SASASASA - owner is asset remote"
aassetMboSet= mbo.getThisMboSet()
whereclause = " cg_import = '1' "
aassetMboSet.setWhere(whereclause)
aassetMboSet.clearWarnings()
count = aassetMboSet.count()
print "SASASASA - filtered mboset "

for j in range(count):
        print "SASASASA - in for loop"
        assetmbo = aassetMboSet.getMbo(j)
        assetmbo.updateDesc()
        assetmbo.save()
        print "SASASASA - setting CG_IMPORT"
        assetmbo.setValue("CG_IMPORT","0")
        print "SASASASA - value set"