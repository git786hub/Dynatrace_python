# AUTOSCRIPT NAME: CG_ACTTOTAL
# CREATEDDATE: 2014-02-05 08:37:17
# CREATEDBY: UVX3
# CHANGEDATE: 2014-02-05 13:29:13
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

totallabor = mbo.getDouble("labbillpr")
totalmat = mbo.getDouble("matbillpr")
totaltool = mbo.getDouble("toolbillpr")
totalsrv = mbo.getDouble("srvbillpr")
totalfee = mbo.getDouble("feebillpr")

totallaborpln = mbo.getDouble("estlabprice")
totalmatpln = mbo.getDouble("cg_estmatprice")
totaltoolpln = mbo.getDouble("esttoolprice")
totalsrvpln = mbo.getDouble("estsrvprice")
totalfeepln = mbo.getDouble("estfeeprice")

totalall = totallabor + totalmat + totaltool  + totalsrv + totalfee

totalpln = totallaborpln  + totalmatpln + totaltoolpln + totalsrvpln + totalfeepln

mbo.setValue("CG_ACTTOTALS",totalall,MboConstants.NOACCESSCHECK)
mbo.setValue("CG_PLNTOTALS",totalpln,MboConstants.NOACCESSCHECK)