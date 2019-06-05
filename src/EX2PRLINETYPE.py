# AUTOSCRIPT NAME: EX2PRLINETYPE
# CREATEDDATE: 2013-10-08 15:03:10
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-02-01 03:54:30
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Active

# ensure material and service/tool lines not mixed on the PR

from psdi.mbo import MboConstants 

def setError(g, e, p):
        global errorgroup, errorkey, params
        errorgroup = g
        errorkey = e
        params= p

prlinesmboset = mbo.getThisMboSet()
num = prlinesmboset.count()
thetype = 'X'
for i in range(num):
    prlinembo = prlinesmboset.getMbo(i)
    prlinetype = prlinembo.getString("LINETYPE")
    if prlinetype == 'ITEM' or prlinetype == 'MATERIAL':
        thistype = 'M'
    else:
        thistype = 'S'
    if thetype == 'X':
        thetype = thistype
    elif thetype <> thistype: 
        setError('pr', 'ex2_mixedtypes', [''])

#INC000001488133
if launchPoint == 'EX2PRLINEITEM' and not mbo.isNull("ITEMNUM"):
 itemOrgSet= mbo.getMboSet("EX2ITEMSTATUSPMBUILDVAL" )
 if (itemOrgSet.isEmpty()):
   setError("item", "ActionNotAllowedInvalidStatus", [mbo.getString("ITEMNUM"),"inventory"])
#end INC000001488133