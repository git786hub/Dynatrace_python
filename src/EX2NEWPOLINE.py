# AUTOSCRIPT NAME: EX2NEWPOLINE
# CREATEDDATE: 2014-05-09 09:11:04
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-05-06 04:26:39
# CHANGEBY: UFAP
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote

#Setting up contract and commodity details for Inbound PETE release POs
#INC000001145129 including ACIS,W2MS,EEPM and BROUSSARD Interfaces
#INC000001239591 Assigning Contract Information on STD & REL POs
v_log = 'A'
if onadd:
  pombo = mbo.getOwner()
  v_log = 'B'
  if pombo and isinstance(pombo,PORemote): 
    v_log = 'C'
    if pombo.getString("potype") in ["STD","REL"]: 
       v_log = 'D'
       mbo.setValue("contractrefnum",pombo.getString("contractrefnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
       mbo.setValue("contractrefid",pombo.getString("contractrefid"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
       mbo.setValue("contractrefrev",pombo.getString("contractrefrev"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
       
       # Start of  - INC000001362113  - PMR- 45888,004,000- PROC--Contract Revision   
       contractlineset=mbo.getMboSet("EX2CONTRACTLINE")
       strlinecond = "itemnum= '" + mbo.getString("itemnum") + "' and linetype='ITEM' and contractnum='" + pombo.getString("contractrefnum") + "' and linestatus='APPR'"
       contractlineset.setWhere(strlinecond)
       polineset=mbo.getMboSet("EX2POLINE")
       strpolinecond="itemnum='" + mbo.getString("itemnum") + "' and revisionnum<" + pombo.getString("REVISIONNUM")+" and ponum='"+pombo.getString("PONUM")+"' and revisionnum in (select revisionnum from po where ponum='"+pombo.getString("PONUM")+ "' and status != 'CAN')"
       print strpolinecond
       polineset.setWhere(strpolinecond)
       print "************$$$$ Before contract line loop %%%%%%%%%%%"
       if (contractlineset.count()>0 and polineset.count()==0):
           contractlinembo=contractlineset.getMbo(0)
           if (contractlinembo.getString("revisionnum") != pombo.getString("contractrefrev")):
             mbo.setValue("unitcost",contractlinembo.getDouble("unitcost"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION) 
       #End of  - INC000001362113  - PMR- 45888,004,000- PROC--Contract Revision

       if pombo.getString("sourcesysid") in ["PTR", "ACIS", "W2MS", "EEPM", "BROUSSARD","TED"]:
           ctrlset = pombo.getMboSet("EX2CONTREFLINE")
           if pombo.getString("sourcesysid")=="BROUSSARD":
             strcond = "contractlinenum = '" + mbo.getString("polinenum") +"'"
             ctrlset.setWhere(strcond)
    
           #Assign the first contract line reference to PO Line
           if ctrlset.count() > 0 :
             ctrlmbo = ctrlset.getMbo(0)
             mbo.setValue("contreflineid",ctrlmbo.getString("contractlineid"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
             mbo.setValue("commodity",ctrlmbo.getString("commodity"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
             mbo.setValue("commoditygroup",ctrlmbo.getString("commoditygroup"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
             mbo.setValue("orderunit",ctrlmbo.getString("orderunit"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
           ctrlset.reset()
    mbo.setValue("PL1",v_log,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)  #for troubleshooting purpose only, this and v_log can be removed later.