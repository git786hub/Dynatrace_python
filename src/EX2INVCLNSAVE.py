# AUTOSCRIPT NAME: EX2INVCLNSAVE
# CREATEDDATE: 2014-04-16 19:02:15
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-04-26 14:28:19
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.app.invoice import InvoiceRemote

def setError():
    global errorkey, errorgroup
    errorkey="ex2notaxorship"
    errorgroup="invoice"

# get invoice header
ivmbo = mbo.getOwner()
if not (ivmbo and isinstance(ivmbo,InvoiceRemote)) :
    ivset = mbo.getMboSet("invoice")
    if ivset.count() > 0 :
        ivmbo = ivset.getMbo(0)

# set shipto from the storeroom on consignment invoices (else next check will fail)
if ivmbo and isinstance(ivmbo,InvoiceRemote) :
    if ivmbo.getString("documenttype") in  ["CONSIGNMENT"] and mbo.isNull("ex2shipto") :
        locset = mbo.getMboSet("ex2consstoreroom")
        if locset.count() > 0 :
            locmbo = locset.getMbo(0)
            mbo.setValue("ex2shipto", locmbo.getString("shiptoaddresscode"), MboConstants.NOACCESSCHECK)

# either the tax code or the ship-to address is required
if user != 'MXINTADM':                         # INC000001308217 Allow MIF created invoice with null Shipto/taxcode, check will be handled in update of invoice - EX2SETDONOTACCRUE
  if not mbo.getBoolean("TAXEXEMPT") :         # if not TAXEXEMPT : check for null value of EX2TAXCODE and EX2SHIPTO 
	if mbo.isNull("ex2taxcode") and mbo.isNull("ex2shipto") :
		#unless tax not required on invoice header
		if ivmbo and isinstance(ivmbo,InvoiceRemote) :
			if not ivmbo.getBoolean("ex2psaccrue") :   # not psaccrue means tax is req'd
				setError()
		else :
			setError()

#INC000001222587 Check EDI Invoices having matching poline and item number
if onadd and ivmbo.getString("sourcesysid") ==  "EDI" :
 poMboSet = mbo.getMboSet("poline")
 if poMboSet.count() > 0:
  poMbo = poMboSet.getMbo(0)
  if mbo.getString("itemnum") <> poMbo.getString("itemnum") :
    global errorkey, errorgroup
    errorkey="notvalid"
    errorgroup="system"
    params=["item number on PO Line " + mbo.getString("polinenum"), mbo.getString("itemnum") ]