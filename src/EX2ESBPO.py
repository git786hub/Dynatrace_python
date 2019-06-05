# AUTOSCRIPT NAME: EX2ESBPO
# CREATEDDATE: 2014-04-17 10:22:17
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-08-09 03:00:42
# CHANGEBY: UXHD
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants

vendor=mbo.getString("VENDOR")[0:7]
print "Vendor " + vendor
cSet=mbo.getMboSet('CONTRACTREF')
# If contract not found let OOTB error handling handle
if cSet.count()>0 :
	contract=cSet.getMbo(0)
	# Throw error if contract and PO vendors not same
	if vendor != contract.getString("VENDOR")[0:7] :
		global errorkey, errorgroup
		errorkey="vendNotApply"
		errorgroup="po"
        if vendor == contract.getString("VENDOR") [0:7]:
            
              shipvia=contract.getString("SHIPVIA")
              mbo.setValue("SHIPVIA",shipvia,11L)
              paymentterms=contract.getString("PAYMENTTERMS")
              mbo.setValue("PAYMENTTERMS",paymentterms,11L)
              fob=contract.getString("FOB")
              mbo.setValue("FOB",fob,11L)