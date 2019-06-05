# AUTOSCRIPT NAME: EX2PURCONSGL
# CREATEDDATE: 2015-01-14 12:38:00
# CREATEDBY: UVX3
# CHANGEDATE: 2015-09-09 15:05:54
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants

#Set Inventory Consignment Control GL Account to PR/PO Line Debit Account
if mbo.getBoolean("CONSIGNMENT"):
	invMboSet = mbo.getMboSet("INVENTORY")
	if invMboSet.count() > 0:
		invMbo = invMboSet.getMbo(0)
		ctrlAcct = invMbo.getString("CONTROLACC")
		if ctrlAcct is not None:
			mbo.setValue("gldebitacct",ctrlAcct,MboConstants.NOACCESSCHECK)



#INC000001158045 Proc PR/PO Project Number Populated 

if launchPoint in  ["EX2PRLGLDEBACT","EX2POLGLDEBACT"]:
       GLDEBITACCT = mbo.getString("GLDEBITACCT")
       EX2PROJECT= mbo.getString("EX2PROJECT")
       if GLDEBITACCT is not None:
               project=GLDEBITACCT[23:31]
               if project != '????????' :
                     mbo.setValue("EX2PROJECT",project,MboConstants.NOACCESSCHECK)
       if GLDEBITACCT is None:
                 if EX2PROJECT is not None:
                     mbo.setValue("EX2PROJECT",'  ',MboConstants.NOACCESSCHECK)	
					 
#INC000001143633 Inventory ordering for warehouse 493 
if interactive and launchPoint == "EX2PRLGLDEBACT": 
	if mbo.getMboSet("EX2INVORDRGRP").count() == 0:
		gldebac = mbo.getString("GLDEBITACCT")
		if gldebac is not None and gldebac[0:41]=='TRN-571900-1545000-000-00000000-0000-0000':
			global errorkey, errorgroup
			errorkey="glInvalid"
			errorgroup="iface"
			params=["Invalid GL Account","Not allowed to order on 493 storeroom inventory account."]