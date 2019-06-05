# AUTOSCRIPT NAME: CG_INSTALLDATE
# CREATEDDATE: 2012-02-17 15:31:25
# CREATEDBY: UHD0
# CHANGEDATE: 2012-07-10 04:34:33
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from java.util import Date

def setError():
        global errorkey,errorgroup,params
        errorkey='invalidinstalldate'
        errorgroup='asset'

if insdate is not None and insdate <> "" : 
    if Date() < insdate :
        setError()