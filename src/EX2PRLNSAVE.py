# AUTOSCRIPT NAME: EX2PRLNSAVE
# CREATEDDATE: 2018-03-23 07:14:45
# CREATEDBY: U3LO
# CHANGEDATE: 2018-05-06 00:57:15
# CHANGEBY: U3LO
# SCRIPTLANGUAGE: python
# STATUS: Draft

from psdi.mbo import MboConstants 
from psdi.app.pr import PRRemote
from psdi.mbo import MboRemote

def setError():
    global errorkey, errorgroup
    errorkey="ex2notaxorship"
    errorgroup="invoice"

if mbo.isNull("ex2taxcode") and mbo.isNull("ex2shipto") :
   setError()