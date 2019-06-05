# AUTOSCRIPT NAME: CG_PLUSPRICESCH
# CREATEDDATE: 2012-11-03 22:32:12
# CREATEDBY: UHD0
# CHANGEDATE: 2012-11-04 12:19:43
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

parentmbo = mbo.getOwner()

if parentmbo.isRevision() :

    apprmboset = mbo.getMboSet("CG_PLUSRANGEMARKUP")
    apprmboset.reset()
    num = apprmboset.count()

    markupmboset = mbo.getMboSet("CG_PLUSMULTISTEP")

    for i in range(num):
        apprmbo = apprmboset.getMbo(i)
        apprmbonew = apprmbo.copy(markupmboset)
        apprmbonew.setValue("REVISIONNUM", mbo.getString("REVISIONNUM"))