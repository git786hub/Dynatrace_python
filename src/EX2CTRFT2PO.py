# AUTOSCRIPT NAME: EX2CTRFT2PO
# CREATEDDATE: 2013-12-30 10:03:22
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-01-15 08:51:03
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote

#first see if owner is PO header and freight terms needs to be set
pombo = mbo.getOwner()
if onadd and pombo and isinstance(pombo,PORemote):
    # cross over freight terms from contract to po
    if pombo.isNull("ex2freightterms") :
        # yes, go get the contract value
        if mbo.isNull("contractrefid") :
            ctrset = mbo.getMboSet("EX2CONTRACT")
        else :
            ctrset = mbo.getMboSet("CONTRACTREF")
        if ctrset.count() > 0 :
            ctrmbo = ctrset.getMbo(0)
            # set freight terms
            pombo.setValue("ex2freightterms", ctrmbo.getString("ex2freightterms"),MboConstants.NOACCESSCHECK)
  
    # for release POs, copy the PR requester over to the PO for the Designated Approver
    if pombo.isNull("ex2desappr") :
        prlset = mbo.getMboSet("EX2PRLINE_NP")
        if prlset.count() > 0 :
            prlmbo = prlset.getMbo(0)
            prset = prlmbo.getMboSet("PR")
            if prset.count() > 0 :
                prmbo = prset.getMbo(0)
                # set designated approver
                pombo.setValue("ex2desappr", prmbo.getString("requestedby"),MboConstants.NOACCESSCHECK)

#INC000001349756 to blank Part Number and Catalog fields on POLINE while adding through Contract items option
appli = mbo.getThisMboSet().getParentApp()

if appli =='PO' and onadd:
  if mbo.getString("LINETYPE")== "ITEM": #this line added for INC000001496323
	mbo.setValueNull("MANUFACTURER",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("MODELNUM",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("CATALOGCODE",MboConstants.NOACCESSCHECK)
#INC000001349756 end