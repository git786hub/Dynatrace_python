# AUTOSCRIPT NAME: EX2_SARCOMM
# CREATEDDATE: 2013-09-17 16:24:22
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-09-18 15:28:31
# CHANGEBY: UGL3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.app.item import ItemRemote

commodity=mbo.getString("EX2NEWCOMMODITY")
if (commodity!=None and commodity!=""):
    commMboSet=mbo.getMboSet("EX2_SARCOMMODITIES")
    if (commMboSet.count()>0):
        parentCommMbo=commMboSet.getMbo(0)
        parentComm=parentCommMbo.getString("PARENT")
        mbo.setValue("EX2NEWCOMMGROUP", parentComm, MboConstants.NOACCESSCHECK)