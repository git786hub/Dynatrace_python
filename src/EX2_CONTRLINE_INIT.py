# AUTOSCRIPT NAME: EX2_CONTRLINE_INIT
# CREATEDDATE: 2013-10-17 08:21:51
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-27 19:11:46
# CHANGEBY: UUYC
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.app.contract.purch import PurchViewRemote

if app == "PLUSDCONTP" :

    # HIDE fields in the main tab if user is a contractor - i.e. in user group 3PSCM
    contmbo = mbo.getOwner()     # try getOwner first
    if not contmbo or not isinstance(contmbo,PurchViewRemote):
        contmbo = mbo.getMboSet("CONTRACT").getMbo(0)     # then try the relationship

    # protect fields after approval process started
    # Commented the below readonly code to fix the Incident: INC000000941040
    # if contmbo.getString("status") in ["BUAPPR", "BUPEND" ] : 
    #     mbo.setFlag(MboConstants.READONLY, True)   #  set object readonly

    buyergroupuser = contmbo.getMboSet("EX2BUYERUSERGROUP")
    if buyergroupuser.count() == 0:
        mbo.setFlag(MboConstants.READONLY, True) 

    if contmbo and isinstance(contmbo,PurchViewRemote):
        if contmbo.getMboSet("EX23PSCMUSERGROUP").count() > 0:
            mbo.setFieldFlag("UNITCOST", MboConstants.HIDDEN, True)
            mbo.setFieldFlag("LINECOST", MboConstants.HIDDEN, True)