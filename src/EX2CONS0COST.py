# AUTOSCRIPT NAME: EX2CONS0COST
# CREATEDDATE: 2014-11-03 15:50:24
# CREATEDBY: UVX3
# CHANGEDATE: 2016-02-09 13:52:07
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 

def setError():
    global errorkey,errorgroup,params
    errorkey='EX2ZEROUNITCOST'
    errorgroup='inventory'

v_return=0

if v_cons is None:
    v_cons= 0

if launchPoint =='EX2MATUSECONS':
 if (mbo.getString("issuetype")=='RETURN'):
  v_return=1

if v_cons==1 and (v_ucost==0 or v_return==1) and v_cucost is not None:
    v_ucost=v_cucost
    #To know on what cost item was issued. Only for troubleshooting purpose.
    if launchPoint =='EX2MATUSECONS' :
        mbo.setValue('IT8','0UC',MboConstants.NOACCESSCHECK)