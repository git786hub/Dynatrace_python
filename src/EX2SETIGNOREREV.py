# AUTOSCRIPT NAME: EX2SETIGNOREREV
# CREATEDDATE: 2014-01-07 12:41:19
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-01-08 08:08:47
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
import sys

# set magic flag to ignore contract revision issues
#if onadd:
try:
    mbo.setValue("po9", 1, MboConstants.NOACCESSCHECK)
    mbo.setValue("ignorecntrev", 1, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

except:
    #print "Exception occurred in running EX2SETIGNOREREV script: ", sys.exc_info()
    mbo.setValue("po9", 3, MboConstants.NOACCESSCHECK)