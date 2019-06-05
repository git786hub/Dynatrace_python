# AUTOSCRIPT NAME: CG_BILLTOTAL
# CREATEDDATE: 2012-12-09 09:13:50
# CREATEDBY: UHD0
# CHANGEDATE: 2013-04-24 07:49:52
# CHANGEBY: UWUD
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

billlineset = mbo.getMboSet("PLUSPBILLBATCH_BILLLINE")
num = billlineset.count()

totalmaterialmarkup = 0
sumbillprice = 0
sumbilltotal = 0

for i in range(num):
    billlinembo = billlineset.getMbo(i)
    billlinematmarkup = 0
    billlinewomboset = billlinembo.getMboSet("PLUSPBILLLINE_WORKORDER")
    wocount = billlinewomboset.count()
    linebillprice = billlinembo.getDouble("BILLEDPRICE")
    
    if wocount > 0 and linebillprice > 0  :
        wombo = billlinewomboset.getMbo(0)
        billlinematmarkup = wombo.getDouble("CG_PLUSMATERIALPRICE")

        agreedprice = billlinembo.getDouble("TOTALBILLED")
        billprice = billlinembo.getDouble("TOTALBILLED")

        sumbillprice = sumbillprice + linebillprice 

        agreedprice = agreedprice  + billlinematmarkup 
        billprice = billprice + billlinematmarkup 

        totalmaterialmarkup = totalmaterialmarkup + billprice 
        billlinembo.setValue("CG_AGREEDPRICE",agreedprice,MboConstants.NOACCESSCHECK)
        billlinembo.setValue("CG_BILLEDPRICE",billprice,MboConstants.NOACCESSCHECK)
    
    if wocount > 0 and linebillprice <= 0  :
        billlinembo.setValue("CG_AGREEDPRICE",billlinembo.getDouble("TOTALBILLED"),MboConstants.NOACCESSCHECK)
        billlinembo.setValue("CG_BILLEDPRICE",billlinembo.getDouble("TOTALBILLED"),MboConstants.NOACCESSCHECK)

pretaxtotal = mbo.getDouble("PRETAXTOTAL")
pretaxtotal = pretaxtotal - sumbillprice + totalmaterialmarkup

#if pretaxtotal < 0 :
#    pretaxtotal = 0
mbo.setValue("CG_BILLTOTAL",pretaxtotal,MboConstants.NOACCESSCHECK)