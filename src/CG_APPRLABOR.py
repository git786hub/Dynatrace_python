# AUTOSCRIPT NAME: CG_APPRLABOR
# CREATEDDATE: 2012-07-11 09:50:12
# CREATEDBY: UHD0
# CHANGEDATE: 2014-05-13 06:18:48
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.util import Date
from psdi.app.workorder import WORemote

sertransmboset = None
priVehicleMboSet = None
labtransset = None

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e

def setMboValues(newmbo) :
    newmbo.setValue("LABORCODE", mbo.getString("LABORCODE"),MboConstants.NOACCESSCHECK)
    newmbo.setValue("REFWO", mbo.getString("REFWO"),MboConstants.NOACCESSCHECK)
    newmbo.setValueNull("CG_PRIVEHICLEHRS",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("CG_ORIGLABTRANSID", mbo.getString("LABTRANSID"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("CG_PRIVEHICLE", False,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("ENTERDATE", mbo.getDate("ENTERDATE"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("STARTDATE", mbo.getDate("STARTDATE"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("ENTERBY", mbo.getString("ENTERBY"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("CG_STARTTIME", mbo.getDate("CG_STARTTIME"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("CG_FINISHTIME", mbo.getDate("CG_FINISHTIME"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValueNull("CG_MEALS",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
    newmbo.setValue("GENAPPRSERVRECEIPT", True,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOOVERWRITE)
    newmbo.setValue("PLUSPCUSTOMER", mbo.getString("PLUSPCUSTOMER"), MboConstants.NOACCESSCHECK)
    newmbo.setValue("PLUSPCUSTCURCODE", mbo.getString("PLUSPCUSTCURCODE"), MboConstants.NOACCESSCHECK)
    newmbo.setValue("PLUSPAGREEMENT", mbo.getString("PLUSPAGREEMENT"), MboConstants.NOACCESSCHECK)
    newmbo.setValue("PLUSPPRICESCHED", mbo.getString("PLUSPPRICESCHED"), MboConstants.NOACCESSCHECK)
    newmbo.setValue("PLUSPREVNUM", mbo.getString("PLUSPREVNUM"), MboConstants.NOACCESSCHECK)

labtransid = mbo.getString("LABTRANSID")
labtransid = labtransid.replace(',', '')


noerrgen = True

if appflag == 1:

    if mbo.getString("LABORCODE") == user:
        noerrgen = False
        setError("labrep", "CannotApproveOwnLabor for Lab Rep ID" + labtransid)

    if mbo.getDouble("REGULARHRS") == 0 and mbo.getDouble("PREMIUMPAYHOURS") ==0 :
        noerrgen = False
        setError("labrep", "Can not Approve labor with zero regular and zero exception hours for Lab Rep ID" + labtransid)


    if mbo.getString("CG_APPROVER.RESPPARTY") <> user and noerrgen :
        noerrgen = False
        setError("labrep", "NotValidApproverLabor for Lab Rep ID" + labtransid)

    if noerrgen and Date() < mbo.getDate("STARTDATE") and noerrgen :
        noerrgen = False
        setError("labrep", "ZeroTolerance for Lab Rep ID" + labtransid)

    if noerrgen and '?' in mbo.getString("GLDEBITACCT") and mbo.getString("REFWO") <> "" :
        noerrgen = False
        setError("labrep", "inValidGL for Lab Rep ID" + labtransid)
	
    labtransset = mbo.getThisMboSet()
    wombo = mbo.getLineOwner(False)

    if mbo.getString("TRANSTYPE") == 'WORK' :   
       wombo.setValue("CG_LABREPFLAG", True,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)

    if not wombo is None :
        if wombo.getString("CG_PROJNO") <> "" and noerrgen:
            if wombo.getString("CG_CANAPPROVELABOR") == 'N':
                noerrgen = False
                setError("LABAUTHTRN", "labauth")

    if mbo.getBoolean("CG_PRIVEHICLE") and noerrgen :
        priVehicleMboSet = mbo.getMboSet("CG_MULTIVEHICLE")
        toolitemMboSet = mbo.getMboSet("CG_MULTIVEHICLE.CG_TOOLITEM")
        
        if priVehicleMboSet.count() > 0 and toolitemMboSet.count() > 0 :
            mbotoolset = mbo.getMboSet("CG_SHOWACTUALTOOL")

            if not wombo is None :
                mbotoolset.setOwner(wombo)    
            mbotool = mbotoolset.add()
            mbotool.setValue("TRANSDATE", mbo.getDate("TRANSDATE"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("REFWO", mbo.getString("REFWO"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("ITEMNUM", priVehicleMboSet.getMbo(0).getString("ITEMNUM"),MboConstants.NOACCESSCHECK)
            mbotool.setValue("TOOLHRS", mbo.getDouble("CG_PRIVEHICLEHRS"),MboConstants.NOACCESSCHECK)
            mbotool.setValue("LABTRANSID", mbo.getString("LABTRANSID"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("ENTERDATE", mbo.getDate("ENTERDATE"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("ENTERBY", mbo.getString("ENTERBY"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("PLUSPCUSTOMER", mbo.getString("PLUSPCUSTOMER"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("PLUSPCUSTCURCODE", mbo.getString("PLUSPCUSTCURCODE"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("PLUSPAGREEMENT", mbo.getString("PLUSPAGREEMENT"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("PLUSPPRICESCHED", mbo.getString("PLUSPPRICESCHED"), MboConstants.NOACCESSCHECK)
            mbotool.setValue("PLUSPREVNUM", mbo.getString("PLUSPREVNUM"), MboConstants.NOACCESSCHECK)

    if mbo.getString("PREMIUMPAYCODE") <> "" and noerrgen and mbo.getString("CG_MEALPAY.DESCRIPTION") <> "" :
        for i in range(mbo.getInt("CG_MEALS")) :
            sertransmboset = mbo.getMboSet("CG_PLUSPGBTRANS")
            sertrans = sertransmboset.add()
            sertrans.setValue("TRANSDATE", mbo.getDate("STARTDATE"), MboConstants.NOACCESSCHECK)
            sertrans.setValue("WONUM", mbo.getString("REFWO"), MboConstants.NOACCESSCHECK)
            sertrans.setValue("TYPE", mbo.getString("CG_MEALCHARGECODE.PREMIUMPAYCODE"),MboConstants.NOACCESSCHECK)
            sertrans.setValue("LINEPRICE", mbo.getDouble("CG_MEALCHARGECODE.DEFAULTRATE"),MboConstants.NOACCESSCHECK)
            sertrans.setValue("BILLPRICE", mbo.getDouble("CG_MEALCHARGECODE.DEFAULTRATE"),MboConstants.NOACCESSCHECK)
            sertrans.setValue("CG_LABTRANSID", mbo.getString("LABTRANSID"),MboConstants.NOACCESSCHECK)

            if  wombo.getString("PLUSPAGREEMENT") <> "" :
                woutil = wombo.getWOUtil()
                woutil.createTransactions(wombo, "PLUSPGBTRANS", sertrans)

            seclabmbo = labtransset.add()
            setMboValues(seclabmbo)

            seclabmbo.setValueNull("REGULARHRS",MboConstants.NOACCESSCHECK)
            seclabmbo.setValue("PREMIUMPAYCODE",mbo.getString("CG_MEALPAY.DESCRIPTION"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            seclabmbo.setValue("PREMIUMPAYHOURS","0.5",MboConstants.NOACCESSCHECK)

    if mbo.getString("SKILLLEVEL") == "UPGRADED" and noerrgen :
        if mbo.getInt("REGULARHRS") > 0 :
            seclabmboureg = labtransset.add()
            setMboValues(seclabmboureg)

            seclabmboureg.setValueNull("REGULARHRS",MboConstants.NOACCESSCHECK)
            seclabmboureg.setValue("PREMIUMPAYCODE",mbo.getString("CG_UPGRADEPAYREG.DESCRIPTION"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            seclabmboureg.setValueNull("PREMIUMPAYHOURS",MboConstants.NOACCESSCHECK)

        if mbo.getInt("PREMIUMPAYHOURS") > 0 and mbo.getString("CG_UPGRADEPAYPP.DESCRIPTION") <> "":
            seclabmboupp = labtransset.add()
            setMboValues(seclabmboupp)

            seclabmboupp.setValueNull("REGULARHRS",MboConstants.NOACCESSCHECK)
            seclabmboupp.setValue("PREMIUMPAYCODE",mbo.getString("CG_UPGRADEPAYPP.DESCRIPTION"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
            seclabmboupp.setValueNull("PREMIUMPAYHOURS",MboConstants.NOACCESSCHECK)

if (sertransmboset is not None and not sertransmboset.isEmpty()) :
 sertransmboset.close()
 

if (priVehicleMboSet is not None and not priVehicleMboSet.isEmpty()) :
 priVehicleMboSet.close()
 

if (labtransset is not None and not labtransset.isEmpty()) :
 labtransset.close()