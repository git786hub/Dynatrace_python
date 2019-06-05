# AUTOSCRIPT NAME: CG_CRRBTNWPM
# CREATEDDATE: 2018-08-27 10:00:57
# CREATEDBY: U4B0
# CHANGEDATE: 2018-08-27 13:15:23
# CHANGEBY: U4B0
# SCRIPTLANGUAGE: jython
# STATUS: Draft

locmboset = mbo.getMboSet("CG_LOCBR")

numl = locmboset.count()
for i in range(numl) :
    locmbo = locmboset.getMbo(i)
    if locmbo:
        locmbo.select()

assetmboset = mbo.getMboSet("CG_ASSETBR")

numa = assetmboset.count()
for j in range(numa) :
    assetmbo = assetmboset.getMbo(j)
    if assetmbo :
        assetmbo.select()


mbo.createAssociatedPMs ( assetmboset , locmboset )
ownermboset = mbo.getThisMboSet()
ownermboset.clearWarnings()
ownermboset.save()