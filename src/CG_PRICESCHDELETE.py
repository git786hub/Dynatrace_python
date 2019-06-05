# AUTOSCRIPT NAME: CG_PRICESCHDELETE
# CREATEDDATE: 2012-11-04 12:07:20
# CREATEDBY: UHD0
# CHANGEDATE: 2012-11-04 12:12:30
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

matmarkupmboset = mbo.getMboSet("CG_MATERIALRANGEMARKUP")
matmarkupmboset.reset()
matmarkupmboset.deleteAll()

toolmarkupmboset = mbo.getMboSet("CG_TOOLRANGEMARKUP")
toolmarkupmboset.reset()
toolmarkupmboset.deleteAll()