# AUTOSCRIPT NAME: IMPORTLOC
# CREATEDDATE: 2015-02-20 04:27:55
# CREATEDBY: UQRM
# CHANGEDATE: 2015-02-20 04:27:55
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.location import LocationRemote

print "RARARARA- in UPDATEDESC script"

aassetMboSet= mbo.getThisMboSet()
print "RARARARA - got mboset"

print "RARARARARA - owner is asset remote"
locationMboSet= mbo.getThisMboSet()
whereclause = " cg_import = '1' "
locationMboSet.setWhere(whereclause)
locationMboSet.clearWarnings()
count = locationMboSet.count()
print "RARARARARA - filtered mboset "

for j in range(count):
        print "RARARA - in for loop"
        locationmbo = locationMboSet.getMbo(j)
        locationmbo.updateDesc()
        locationmbo.save()
        print "RARARARA - setting CG_IMPORT"
        locationmbo.setValue("CG_IMPORT","0")
        print "RARARARA - value set"