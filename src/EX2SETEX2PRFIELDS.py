# AUTOSCRIPT NAME: EX2SETEX2PRFIELDS
# CREATEDDATE: 2013-11-01 14:32:16
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-03-23 07:16:03
# CHANGEBY: U1J2
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote
from java.lang import Math


# set link fields for use after the PO has been cancelled (and Maximo link fields are cleared)

if launchPoint !='EX2POLINVAPPR':
	if not mbo.isNull("prlinenum") and not mbo.isNull("prnum") and mbo.isNull("ex2prnum") :
		prnm = mbo.getString("prnum")
		prln = mbo.getInt("prlinenum")
		mbo.setValue("ex2prnum", prnm, MboConstants.NOACCESSCHECK)
		mbo.setValue("ex2prlinenum", prln, MboConstants.NOACCESSCHECK)
              #  test = mbo.getString("ex2prnum")

        if onadd:
                GLDEBITACCT = mbo.getString("GLDEBITACCT")
                EX2PROJECT= mbo.getString("EX2PROJECT")
                if GLDEBITACCT is not None:
                    project=GLDEBITACCT[23:31]
                    if project != '????????' :
                        mbo.setValue("EX2PROJECT",project,MboConstants.NOACCESSCHECK)


	# set poline shipto from prline, override maximo copying from po header


	if onadd and not mbo.isNull("ex2prnum") :
		prlset = mbo.getMboSet("EX2PRLINE_NP")
		if prlset.count() > 0 :
			prlmbo = prlset.getMbo(0)
               	        mbo.setValue("shipto", prlmbo.getString("ex2shipto"), MboConstants.NOACCESSCHECK)
                        mbo.setValue("EX2DROPSHIP", prlmbo.getString("EX2DROPSHIP"), MboConstants.NOACCESSCHECK)
                        mbo.setValue("EX2EXTREMARKS", prlmbo.getString("EX2EXTREMARKS"), MboConstants.NOACCESSCHECK)
                        mbo.setValue("EX2EXTREMARKS_LONGDESCRIPTION", prlmbo.getString("EX2EXTREMARKS_LONGDESCRIPTION"),MboConstants.NOACCESSCHECK)
                        # Carry over Taxcode from PRLINE to POLINE
                        mbo.setValue("ex2taxcode", prlmbo.getString("ex2taxcode"), MboConstants.NOACCESSCHECK)
     
# set header invoice approver if it is null, but this line has one

if onadd and not mbo.isNull("ex2invappr") :
    pombo = mbo.getOwner()
    # if poline object owner is not the PO header, get it using the relationship 
    if not pombo or not isinstance(pombo,PORemote):   
        pombo = mbo.getMboSet("PO").getMbo(0)
    if pombo and isinstance(pombo,PORemote):
        if pombo.isNull("ex2invappr") :
            pombo.setValue("ex2invappr", mbo.getString("ex2invappr"), MboConstants.NOACCESSCHECK)

#INC000001422195 - Workaround fix to maintain tolerance limit for CONSIGNMENT items.
# INC000001002285 - Workaround fix to derive tolerance limit from inventory if created from PR and inventory has no invvendor.
#INC000001422195-PROC - receipt tolerance qty issue

receipttolrence=mbo.getInt("RECEIPTTOLERANCE")
receipttolqty=mbo.getDouble("RECEIPTTOLQTY")
orderqty=mbo.getInt("ORDERQTY")

def setTolerance():
  if mbo.getString("LINETYPE")=="ITEM":
    if not mbo.isNull("ITEMNUM"):
	if not mbo.isNull("STORELOC"):
	  invmbo = mbo.getMboSet("INVENTORY").getMbo(0)
	  if invmbo is not None:
	      mbo.setValue("RECEIPTTOLERANCE",invmbo.getString("RECEIPTTOLERANCE"), MboConstants.NOACCESSCHECK)
          else:
              mbo.setValue("RECEIPTTOLERANCE",35, MboConstants.NOACCESSCHECK)
	else:
	  itemmbo = mbo.getMboSet("ITEM").getMbo(0)
	  if itemmbo is not None:
              mbo.setValue("RECEIPTTOLERANCE",itemmbo.getString("RECEIPTTOLERANCE"), MboConstants.NOACCESSCHECK)
          else:
              mbo.setValue("RECEIPTTOLERANCE",35, MboConstants.NOACCESSCHECK)
  elif mbo.getString("LINETYPE") in ("MATERIAL","TOOL"):
      mbo.setValue("RECEIPTTOLERANCE",0, MboConstants.NOACCESSCHECK)
  elif mbo.getString("LINETYPE")=="STDSERVICE" and mbo.getString("ITEMNUM") in ("FREIGHT","RESTOCK FEE DIS","RESTOCK FEE TRN"):
      mbo.setValue("RECEIPTTOLERANCE",0, MboConstants.NOACCESSCHECK)
          
		
if onadd or onupdate:
	setTolerance()
	receipttolrence=mbo.getInt("RECEIPTTOLERANCE")
        if not mbo.isNull("RECEIPTTOLERANCE"):
	    mbo.setValue("RECEIPTTOLQTY",(orderqty*receipttolrence/100),MboConstants.NOACCESSCHECK|MboConstants.NOACTION)
elif mbo.isModified("ITEMNUM") or mbo.isModified("STORELOC") or mbo.isModified("ORDERQTY"):
	setTolerance()
	receipttolrence=mbo.getInt("RECEIPTTOLERANCE")


# Set RECEIPTTOLQTY to lowest whole number irrespective of Receipt Tolerance

if ( receipttolqty <> "" and receipttolqty is not None and receipttolqty <>0  ) :
  receipttolqty=mbo.getDouble("RECEIPTTOLQTY")
  mbo.setValue("RECEIPTTOLQTY",Math.floor(receipttolqty),MboConstants.NOACCESSCHECK)
  mbo.setValue("RECEIPTTOLERANCE",receipttolrence, MboConstants.NOACCESSCHECK|MboConstants.NOACTION)