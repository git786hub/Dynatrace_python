# AUTOSCRIPT NAME: EX2INVREVCODE
# CREATEDDATE: 2014-08-19 02:16:32
# CREATEDBY: UVX3
# CHANGEDATE: 2014-08-20 01:11:17
# CHANGEBY: UUY8
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e


if mbo.getString("EX2INVREVCODE") is not None and mbo.getString("EX2INVREVCODE")  != "" :
   mbo.setValue("EX2INVREVCODE",(mbo.getString("EX2INVREVCODE")).upper(),2)
   revCode= mbo.getString("EX2INVREVCODE")

   if len(revCode) != 4:
      setError("EX2INVREVCODE","INVALIDLEN")
      
   if revCode[0].upper() != 'W':
      setError("EX2INVREVCODE","INVALIDCHAR")

   if revCode[1] != '1' and revCode[1] != '2' and revCode[1] != '3' and revCode[1] != '4' and revCode[1].upper() != 'C' :
      setError("EX2INVREVCODE","INVALIDCODE")