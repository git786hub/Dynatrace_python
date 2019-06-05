# AUTOSCRIPT NAME: CG_PLUSPSJPNUM
# CREATEDDATE: 2012-09-09 17:21:09
# CREATEDBY: UHD0
# CHANGEDATE: 2012-09-09 17:29:08
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

if jpnum <> None :
    strsql = "jpnum ='" + jpnum + "'"
    mbo.setValue("CONDITION", strsql)
else :
    mbo.setValueNull("CONDITION")