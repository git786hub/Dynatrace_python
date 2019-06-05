# AUTOSCRIPT NAME: CG_WORKORDEROBJ
# CREATEDDATE: 2012-04-11 10:42:18
# CREATEDBY: UHD0
# CHANGEDATE: 2018-06-15 06:07:10
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import GLFormat
from psdi.mbo import MboConstants
from psdi.security import UserInfo
from psdi.app.asset import AssetRemote
from psdi.app.location import LocationRemote
from psdi.app.workorder import WO
from java.util import Date

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

owner = mbo.getOwner()
if (isinstance(owner,AssetRemote) or isinstance(owner,LocationRemote)) and not mbo.isNull("JPNUM"):
	jpnum = mbo.getString("JPNUM")
	#mbo.setValueNull("JPNUM")
	mbo.setValue("JPNUM",jpnum, MboConstants.NOACCESSCHECK)


if onadd or onupdate:
    if (mbo.getString("LOCATION") in ["LINE","SECTION"]):
        mbo.setValue("CG_WORKCENTER", mbo.getString("WO_ASSET.CG_WORKMAJ.ALNVALUE"), MboConstants.NOACCESSCHECK)
    else:
        mbo.setValue("CG_WORKCENTER", mbo.getString("LOCATION.CG_INWORKCENTER.CG_LOCLEGACYID"), MboConstants.NOACCESSCHECK)


if (mbo.getString("CG_WORKTYPE") == "CORRECTIVE"  or mbo.getString("CG_WORKTYPE") == "CAPITAL"  or mbo.getString("CG_WORKTYPE") == "OPERATIONS" )  and mbo.getString("STATUS") <> "APPR" and mbo.isNull("PMNUM") and onadd:
    mbo.changeStatus("APPR",Date(),"Auto Approved by Script",MboConstants.NOACCESSCHECK)


mWorktype = mbo.getString("CG_WORKTYPE")
mProjno = mbo.getString("CG_PROJNO")

mbo.setValueNull("cg_defaultreadingdate",MboConstants.NOACCESSCHECK)

noerrgen = True

if mProjno is not None and mProjno != "":
    if len(mProjno) < 8 and interactive  and mbo.getThisMboSet().getParentApp() in ["ASSETS_TRN"] and mbo.getString("SITEID") =='TRN':
        setError("cg_wottrn", "ProjCodeLength", None)
        noerrgen = False
	
    if mWorktype.upper() not in ["CAPITAL", "JOB ORDER"] and len(mProjno) > 2 and mProjno[2].upper() != 'P' and noerrgen:
        setError("cg_wottrn", "projnoNeedP", None)
        noerrgen = False

    if mWorktype.upper() in ["CAPITAL", "JOB ORDER"] and len(mProjno) > 2 and mProjno[2].upper() == 'P' and noerrgen :
        setError("cg_wottrn", "projnoCannotHaveP", None)
        noerrgen = False

if ( mProjno is None or mProjno == "" ) and mWorktype.upper() == "CAPITAL" and noerrgen :
    setError("system", "allnullrequired", ["Project Number"])
    noerrgen = False

if mWorktype.upper() in ["CAPITAL"] and mbo.getMboSet("CG_PARENTCAPITALWO").count() > 0 and noerrgen :
    setError("cg_wottrn", "capitalWoExists", None)
    noerrgen = False

if noerrgen and not mbo.isNull("ROUTESTOPID") and not mbo.isNull("WO_PARENT.GLACCOUNT") :
    fmt = GLFormat(mbo.getString ("WO_PARENT.GLACCOUNT"), mbo.getString("ORGID"))
    fmt.mergeString(mbo.getString("GLACCOUNT"))
    mbo.setValue("GLACCOUNT",fmt.toDisplayString(), MboConstants.NOACCESSCHECK)

if noerrgen :

    mattranset = mbo.getMboSet("SHOWACTUALMATERIAL") 
    mattrannum = mattranset.count()
    matprice = 0
    for j in range(mattrannum):
        mattran = mattranset.getMbo(j)
        if mattran :
            lineprice = mattran.getDouble("PLUSPLINEPRICE") 
            matprice = matprice + lineprice

    matmarkupset = mbo.getMboSet("PLUSPPRICESCHED.CG_MATERIALRANGEMARKUP") 
    tmnum = matmarkupset.count()
    tempmarkup = 0
    for i in range(tmnum):
        matmarkup = matmarkupset.getMbo(i)
        if matmarkup :
            maxmarkup = matmarkup.getDouble("TOPRICE")             
            minmarkup = matmarkup.getDouble("FROMPRICE")
            markupvalue = matmarkup.getDouble("CALC")
        
            if matprice > maxmarkup :
                tempmarkup = tempmarkup + (( maxmarkup - minmarkup ) * markupvalue / 100 )

            if matprice > minmarkup  and matprice < maxmarkup :
                tempmarkup = tempmarkup + (( matprice - minmarkup ) * markupvalue / 100 )

    matprice = matprice + tempmarkup

    mbo.setValue("CG_PLUSMATERIALPRICE",tempmarkup,MboConstants.NOACCESSCHECK)

wojpnum = mbo.getString("JPNUM")
woactfinish = mbo.getDate("ACTFINISH")
wofaildate = mbo.getDate("FAILDATE")
wofailreportedby = mbo.getString("CG_FAILUREREPORTEDBY")

failureset=mbo.getMboSet("FAILUREREPORT")
failurecount = failureset.count()

for i in range(failurecount) :
    failure=failureset.getMbo(i)
    failure.setValue("JPNUM",wojpnum,MboConstants.NOACCESSCHECK)
    failure.setValue("ACTFINISH",woactfinish,MboConstants.NOACCESSCHECK)
    failure.setValue("FAILDATE",wofaildate,MboConstants.NOACCESSCHECK)
    failure.setValue("REPORTEDBY",wofailreportedby,MboConstants.NOACCESSCHECK)
    failure.setValue("REMARKS",mbo.getString("REMARKDESC"),MboConstants.NOACCESSCHECK)
    failure.setValue("FAILUREDATE",mbo.getDate("REMARKENTERDATE"),MboConstants.NOACCESSCHECK)