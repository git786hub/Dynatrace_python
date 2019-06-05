# AUTOSCRIPT NAME: EX2POLINEINIT
# CREATEDDATE: 2013-10-09 17:22:17
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-10-10 23:58:57
# CHANGEBY: U4MU
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote



if interactive :
 if app in ["PO"]:
    pombo = mbo.getOwner()
    # if poline object owner is not the PO header, get it using the relationship 
    if not pombo or not isinstance(pombo,PORemote):   
        pombo = mbo.getMboSet("PO").getMbo(0)
    if pombo and isinstance(pombo,PORemote):

        # protect po when it is in workflow (DOA-related processes)
        #if pombo.getString("STATUS") == "BUPEND" : 
        asgnset = pombo.getMboSet("EX2DOAWFASGN")
        if asgnset.count() > 0 :
            mbo.setFlag(MboConstants.READONLY, True)   #  set object readonly

        # HIDE fields in the main tab if user is a contractor - i.e. in user group 3PSCM
        if pombo.getMboSet("EX23PSCMUSERGROUP").count() > 0:
            mbo.setFieldFlag("UNITCOST", MboConstants.HIDDEN, True)
            mbo.setFieldFlag("LINECOST", MboConstants.HIDDEN, True)
            mbo.setFieldFlag("TAX1", MboConstants.HIDDEN, True)
            mbo.setFieldFlag("LOADEDCOST", MboConstants.HIDDEN, True)
            mbo.setFieldFlag("RECEIVEDUNITCOST", MboConstants.HIDDEN, True)
            mbo.setFieldFlag("RECEIVEDTOTALCOST", MboConstants.HIDDEN, True)

if launchPoint=='EX2POLINEDESCRIPTION':
 receivedqty=mbo.getDouble("RECEIVEDQTY") 
 if receivedqty>0 and interactive:
      mbo.setFieldFlag("DESCRIPTION", MboConstants.READONLY, True)