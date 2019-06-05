# AUTOSCRIPT NAME: EX2PROTECTINVCLNSINWF
# CREATEDDATE: 2013-12-11 07:06:23
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-10-20 05:03:25
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.app.invoice import InvoiceRemote

#actvwfmboset = mbo.getMboSet("ex2activewfasgn")   # is there an active assignment?
#if  interactive and actvwfmboset.count() > 0 :

groupuserSet=mbo.getMboSet("EX2GROUPUSER")

if interactive :
    invcmbo = mbo.getOwner()
    if invcmbo and isinstance(invcmbo,InvoiceRemote) :
        if (invcmbo.getString("status") == "BUPEND")  or (groupuserSet.isEmpty() and invcmbo.getString("status") == "REVIEW") :
            mbo.setFlag(MboConstants.READONLY, True)        #  set object readonly

        #if not invcmbo.isNull("sourcesysid") :
        mbo.setFieldFlag("invoicelinenum_longdescription", MboConstants.READONLY, True)