# AUTOSCRIPT NAME: EX2VALIDATEGLONPR
# CREATEDDATE: 2015-07-15 06:26:58
# CREATEDBY: UVX3
# CHANGEDATE: 2015-12-02 23:03:22
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants


def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e


if interactive:
 mGLdebit = mbo.getString("GLDEBITACCT")
 if '?' in mGLdebit:
  setError("WOGLACCOUNT", "EnterCompleteGLAcount")
  
 print "VALIDATEGL: "+launchPoint+": End"