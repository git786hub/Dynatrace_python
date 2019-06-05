# AUTOSCRIPT NAME: CG_VALIDNEGHRS
# CREATEDDATE: 2012-07-17 02:56:43
# CREATEDBY: UHD0
# CHANGEDATE: 2015-11-17 07:28:44
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

selectedrow = 0

ownmbo = None
noerrgen = True
mbononegset = None
sertransmboset = None
seclabmbo = None

if negativehrs == 1 :

    mbononegset = mbo.getMboSet("CG_APPROVEDLABOR_NONEGATIVE")
    mbononegset1 = mbo.getMboSet("CG_APPROVEDLABLOR_CONTRACTOR")

    num = mbononegset.count()
    num1 = mbononegset1.count()

    for i in range (num) :
        mbononeg = mbononegset.getMbo(i)
        if mbononeg.isSelected() :
            selectedrow = selectedrow + 1
            ownmbo = mbononeg 
    
    for i in range (num1) :
        mbononeg = mbononegset1.getMbo(i)
        if mbononeg.isSelected() :
            selectedrow = selectedrow + 1
            ownmbo = mbononeg 

    if selectedrow == 0 :
        setError("labreptrn", "noRecords", None)
        negativehrs = 0
        noerrgen = False

    if selectedrow >  1 and noerrgen  :
        setError("labreptrn", "moreRecords", None)
        negativehrs = 0
        noerrgen = False

    if (mbo.getDouble("REGULARHRS") <> 0 or mbo.getDouble("PREMIUMPAYHOURS") <> 0  or mbo.getDouble("CG_PRIVEHICLEHRS") <> 0) and noerrgen :
        setError("labreptrn", "cannotHaveReportedHours", None)
        negativehrs = 0
        noerrgen = False

    if negativehrs == 1 and noerrgen :
        mbo.setValue("CG_ORIGLABTRANSID", ownmbo.getString("LABTRANSID"),MboConstants.NOACCESSCHECK)
        mbo.setValue("REGULARHRS", -1 * ownmbo.getDouble("REGULARHRS"),MboConstants.NOACCESSCHECK)
        mbo.setValue("CG_PRIVEHICLE", False,MboConstants.NOACCESSCHECK)

        if ownmbo.getString("PREMIUMPAYCODE") <> "" :
            mbo.setValue("PREMIUMPAYCODE", ownmbo.getString("PREMIUMPAYCODE"),MboConstants.NOACCESSCHECK)
            mbo.setValue("PREMIUMPAYHOURS",  -1 * ownmbo.getDouble("PREMIUMPAYHOURS"),MboConstants.NOACCESSCHECK)
            mbo.setValue("CG_MEALS",  -1 * ownmbo.getDouble("CG_MEALS"),MboConstants.NOACCESSCHECK)

            for i in range(ownmbo.getInt("CG_MEALS")) :
                sertransmboset = mbo.getMboSet("CG_PLUSPGBTRANS")
                sertrans = sertransmboset.add()
                sertrans.setValue("WONUM", ownmbo.getString("REFWO"), MboConstants.NOACCESSCHECK)
                sertrans.setValue("TYPE", ownmbo.getString("CG_MEALCHARGECODE.PREMIUMPAYCODE"),MboConstants.NOACCESSCHECK)
                sertrans.setValue("LINEPRICE", -1 * ownmbo.getDouble("CG_MEALCHARGECODE.DEFAULTRATE"),MboConstants.NOACCESSCHECK)
                sertrans.setValue("CG_LABTRANSID", mbo.getString("LABTRANSID"),MboConstants.NOACCESSCHECK)

                seclabmbo = mbo.copy()
                seclabmbo.setValue("PREMIUMPAYCODE",ownmbo.getString("CG_MEALPAY.DESCRIPTION"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                seclabmbo.setValue("PREMIUMPAYHOURS","-0.5",MboConstants.NOACCESSCHECK)
                seclabmbo.setValueNull("REGULARHRS",MboConstants.NOACCESSCHECK)
                seclabmbo.setValueNull("CG_PRIVEHICLEHRS",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                seclabmbo.setValue("CG_ORIGLABTRANSID", mbo.getString("LABTRANSID"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                seclabmbo.setValue("CG_PRIVEHICLE", False,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                seclabmbo.setValueNull("CG_MEALS",MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
                seclabmbo.setValue("GENAPPRSERVRECEIPT", True,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOOVERWRITE)

        mbo.setValue("GENAPPRSERVRECEIPT", True,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOOVERWRITE)




if (sertransmboset is not None and not sertransmboset.isEmpty()) :  
      sertransmboset.close()

if (mbononegset is not None and not mbononegset.isEmpty()) :
     mbononegset.close()