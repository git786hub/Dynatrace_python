# AUTOSCRIPT NAME: EX2SETDONOTACCRUE
# CREATEDDATE: 2014-03-20 12:51:12
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-03-02 15:03:18
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from java.util import Date 

#Commented to set the date on Invoice when the Invoice is created from the Cron Task 
#if onadd and mbo.getString("documenttype") in  ["CONSIGNMENT"]  and app in ["INVOICE"]:
if onadd and mbo.getString("documenttype") in  ["CONSIGNMENT"] :
    mbo.setValue("VENDORINVOICENUM", mbo.getString("INVOICENUM"), MboConstants.NOACCESSCHECK)
    mbo.setValue("INVOICEDATE", Date(), MboConstants.NOACCESSCHECK)

if onadd and mbo.getString("sourcesysid") in  ["BROUSSARD", "EEPM", "ACIS", "W2MS"] :
    mbo.setValue("ex2psaccrue", True)


# set taxable flag based on taxability of the lines

if mbo.getString("status") not in ["PD", "PSREVERSE", "UPD", "CANCEL", "HOLD", "CLEARED", "PAID", "PENDREV"] :
    if mbo.getBoolean("ex2psaccrue") :
        mbo.setValue("ex2taxexempt", True, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    else :
        mbo.setValue("ex2taxexempt", True, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
        lineset1 = mbo.getMboSet("invoiceline")
        lineset1.setWhere(" taxexempt=0 ")
        if lineset1.count() > 0:
            mbo.setValue("ex2taxexempt", False, MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

# INC000001308217 Check after creation of Invoice lines having null shipto taxcode created from interface
if onupdate and not mbo.getString("ex2psaccrue"):
    lineset2 = mbo.getMboSet("invoiceline")
    lineset2.setWhere(" taxexempt = 0 and (ex2shipto is null or ex2taxcode is null)" )
    if lineset2.count() > 0:
        global errorkey, errorgroup
        errorkey="ex2notaxorship"
        errorgroup="invoice"