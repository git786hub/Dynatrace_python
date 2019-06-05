# AUTOSCRIPT NAME: CG_MATMARKUP
# CREATEDDATE: 2013-09-19 06:09:12
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-09-19 06:09:12
# CHANGEBY: UM7V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

ownermbo = mbo.getOwner()

wpmatset = mbo.getThisMboSet()
wpmatnum = wpmatset.count()
matprice = 0
for j in range(wpmatnum):
     wpmat = wpmatset.getMbo(j)
     if wpmat and not wpmat.toBeDeleted():
         lineprice = wpmat.getDouble("PLUSPLINEPRICE")
         matprice = matprice + lineprice

matmarkupset = ownermbo.getMboSet("PLUSPPRICESCHED.CG_MATERIALRANGEMARKUP") 
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

pluspwoprice = ownermbo.getMboSet("PLUSPWOPRICETOTALS").getMbo(0)
pluspwoprice.setValue("CG_ESTMATPRICE",matprice,MboConstants.NOACCESSCHECK)