# AUTOSCRIPT NAME: EX2POWFSEQ
# CREATEDDATE: 2015-07-13 02:57:33
# CREATEDBY: U047
# CHANGEDATE: 2015-07-20 09:36:03
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboSetRemote

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e
	
thisValue = mbo.getInt("ex2perseq")
if(thisValue<=0):
	setError("ex2powf", "NotValidSequence")
ex2powfMboSet = mbo.getThisMboSet()
num = ex2powfMboSet.count()
print'------------------------------------------ex2powf:num--------------------------------------'
print num
for i in range(num):
	mbo1 =ex2powfMboSet.getMbo(i)
        if(thisValue==mbo1.getInt("ex2perseq") and mbo.getString("ex2person") !=mbo1.getString("ex2person")):
		setError("ex2powf", "duplicateSequence")