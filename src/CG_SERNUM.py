# AUTOSCRIPT NAME: CG_SERNUM
# CREATEDDATE: 2015-04-02 04:38:09
# CREATEDBY: UQRM
# CHANGEDATE: 2016-09-07 04:49:00
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

assetserial = mbo.getString("SERIALNUM")
assetmanu=mbo.getString("CG_MANUFACTURER")

if app=="ASSETS_TRN":
    AssetMboSet=mbo.getMboSet("CG_SERIALMANUF")
else:
    AssetMboSet=mbo.getMboSet("CG_SERIALMANU")
num=AssetMboSet.count()

if(num>0 and assetserial is not None):
   setError("system", "sqlWithIdentifier", None)