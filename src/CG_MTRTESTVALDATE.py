# AUTOSCRIPT NAME: CG_MTRTESTVALDATE
# CREATEDDATE: 2013-09-17 02:52:21
# CREATEDBY: UFDA
# CHANGEDATE: 2013-09-23 12:20:28
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

# Check if for input asset number, a test result already available

import time
from java.text import SimpleDateFormat
from time import strftime
fmt = SimpleDateFormat('MM/dd/yy')

def setError(g, k):
    global errorkey, errorgroup, params
    errorgroup = g
    errorkey = k



iptestdate = mbo.getString("TESTDATE")
ipmetertestid = mbo.getString("CG_METERTESTID")

metertestset = mbo.getMboSet("CG_METERTESTMETERTEST")

meterassetcount = metertestset.count()
if (meterassetcount > 0) : 
    for i in range(meterassetcount) :
    
        astmtrrec = metertestset.getMbo(i)
        testdateexist = astmtrrec.getString("TESTDATE")
        metertestid = astmtrrec.getString("CG_METERTESTID")
        parstestdate = fmt.parse(testdateexist)
        
        inpatestdate = fmt.parse(iptestdate)
        
        if (parstestdate == inpatestdate and metertestid <> ipmetertestid) :
            setError("FAILURECODE", " Meter test already exists for this test date.  Cannot have two meter tests for the same date")


#dateformat="12/1/10"