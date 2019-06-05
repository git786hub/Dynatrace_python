# AUTOSCRIPT NAME: CG_SETDESC
# CREATEDDATE: 2012-07-02 09:14:35
# CREATEDBY: UHD0
# CHANGEDATE: 2012-07-02 15:29:58
# CHANGEBY: UGL3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.security import UserInfo
from psdi.mbo import MboServerInterface
from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.app.masterpm import MasterPMRemote

if (onadd or onupdate):
    masterPMSeqMboSet = mbo.getThisMboSet()
    masterPMMbo=mbo.getOwner()
    num=masterPMSeqMboSet.count()
    seq=mbo.getInt("INTERVAL")
    jpnum=mbo.getString("JPNUM")
    desc=""
    jobPlanMboSet=mbo.getMboSet("JOBPLAN")
    if jobPlanMboSet.count()>0:
        jobPlanMbo=jobPlanMboSet.getMbo(0)
        desc=jobPlanMbo.getString("DESCRIPTION")
    found=0
    thisMasterPM=mbo.getString("MASTERPMNUM")
    if num>0:
        for i in range(num) :
            mboMasterPMSeq = masterPMSeqMboSet.getMbo(i)
            masterpm= mboMasterPMSeq.getString("MASTERPMNUM")
            if thisMasterPM==masterpm:
                if mboMasterPMSeq.getInt("INTERVAL")<seq:
                    found=1
                    seq=mboMasterPMSeq.getInt("INTERVAL")
                    jpnum=mboMasterPMSeq.getString("JPNUM")
                    jobPlanMboSet=mboMasterPMSeq.getMboSet("JOBPLAN")
                    if jobPlanMboSet.count()>0:
                        jobPlanMbo=jobPlanMboSet.getMbo(0)
                        desc=jobPlanMbo.getString("DESCRIPTION")
                    if isinstance(masterPMMbo,MasterPMRemote) and not masterPMMbo.isNull("MASTERPMNUM"):
                        if masterPMMbo.getString("DESCRIPTION")=="":
                            masterPMMbo.setValue("DESCRIPTION",desc,MboConstants.NOACCESSCHECK)
                            masterPMMbo.setFieldFlag("DESCRIPTION", MboConstants.READONLY,True)
    if found==0:
        if isinstance(masterPMMbo,MasterPMRemote) and not masterPMMbo.isNull("MASTERPMNUM"):
            if masterPMMbo.getString("DESCRIPTION")=="":
                masterPMMbo.setValue("DESCRIPTION",desc,MboConstants.NOACCESSCHECK)
                masterPMMbo.setFieldFlag("DESCRIPTION", MboConstants.READONLY,True)