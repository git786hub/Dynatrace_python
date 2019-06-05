# AUTOSCRIPT NAME: CG_TOOLTRANSOBJ
# CREATEDDATE: 2012-04-11 09:42:10
# CREATEDBY: UHD0
# CHANGEDATE: 2013-01-15 03:32:39
# CHANGEBY: UFCV
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e

mGLdebit = mbo.getString("GLDEBITACCT")
if mGLdebit is not None and '?' in mGLdebit:
    setError("inventory", "invalidGLDebitAccount")

mtoolhrs = mbo.getString("TOOLHRS")
if mtoolhrs == "0:00":
    setError("tooltrans","zerotoolhrs")