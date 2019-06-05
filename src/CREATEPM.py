# AUTOSCRIPT NAME: CREATEPM
# CREATEDDATE: 2012-10-14 14:31:34
# CREATEDBY: UHD0
# CHANGEDATE: 2015-01-22 10:52:50
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

locmboset = mbo.getMboSet("CG_LOCOPER")

numl = locmboset.count()
for i in range(numl) :
    locmbo = locmboset.getMbo(i)
    if locmbo:
        locmbo.select()

assetmboset = mbo.getMboSet("CG_ASSET")

numa = assetmboset.count()
for j in range(numa) :
    assetmbo = assetmboset.getMbo(j)
    if assetmbo :
        assetmbo.select()


mbo.createAssociatedPMs ( assetmboset , locmboset )
ownermboset = mbo.getThisMboSet()
ownermboset.clearWarnings()
ownermboset.save()