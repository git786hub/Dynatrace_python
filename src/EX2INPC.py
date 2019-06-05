# AUTOSCRIPT NAME: EX2INPC
# CREATEDDATE: 2014-03-20 22:03:04
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-04-09 04:27:48
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.util import MXApplicationException
from java.util import Date
from java.util import Calendar

## EX2INVOCE sql : invoicenum = :invoicenum and siteid = :siteid

invoiceset = mbo.getMboSet("EX2INVOICE")
c = Calendar.getInstance()


try:    
        iinvcount = invoiceset.count()
        if iinvcount > 0 :
            inv = invoiceset.getMbo(0)
            inv.validateForApproval()
            inv.checkForServiceLineTolerance()
            inv.checkForPOLineTolerance()
            inv.checkForTaxTolerance()
            inv.checkForServiceLinePOTolerance()


except MXApplicationException, e :

        print "****** PRECHECK VALIDATION FAILED **********  "

        where=invoiceset.getCompleteWhere()
        invoiceset.setWhere(where)
        invoiceset.reset()

        invErrorSet = mbo.getMboSet("EX2IVERRORS")
        invErrorMbo=invErrorSet.add()
        invErrorMbo.setValue("ORGID", mbo.getString("ORGID"))
        invErrorMbo.setValue("SITEID", mbo.getString("SITEID"))
        invErrorMbo.setValue("EX2INVOICENUM", mbo.getString("INVOICENUM"))
        invErrorMbo.setValue("EX2ERRDESC", e.getMessage())
        invErrorMbo.setValue("EX2MSGSETID",  "MX")
        invErrorMbo.setValue("EX2MSGID",  "MX")
        invErrorMbo.setValue("EX2ERRDATE",  Date())

        if mbo.getString('STATUS') != 'MISMATCH' :
            mbo.changeStatus('MISMATCH',Date(),'Changed By PREVALIDATION')
else:
        where=invoiceset.getCompleteWhere()
        invoiceset.setWhere(where)
        invoiceset.reset()
        print "****** PRECHECK VALIDATION COMPLETE 1**********  "
        if mbo.getString('STATUS') != 'WAPPR' :
               mbo.changeStatus('WAPPR', c.add(Calendar.SECOND,-10),'Changed By PREVALIDATION')

        print "****** PRECHECK VALIDATION COMPLETE **********  "

#ticket INC000001443912 
if ((mbo.getString('DOCUMENTTYPE') != 'CREDIT')):
	invoiceLineSet = mbo.getMboSet('INVOICELINE')    # relationship to get all invoiceline
	linecount = invoiceLineSet.count()
	print linecount
	recPOQuantity = 0
        if linecount > 0 :
		for i in range(linecount):
                        invQuantity = 0
                        invcQuantitiy = 0
                        flag =0
			invoiceLineMbo =invoiceLineSet.getMbo(i)
			print invoiceLineMbo.getString('linetype')
			if(invoiceLineMbo.getString('linetype') in ['MATERIAL','ITEM']) :
				poLineSet = invoiceLineMbo.getMboSet('POLINE')  # Relationship to get poline
				polcount = poLineSet.count()
				print polcount
				if polcount > 0 :
					recPOQuantity = poLineSet.getMbo(0).getInt('RECEIVEDQTY')
					print recPOQuantity
					allinvLineSet = invoiceLineMbo.getMboSet('EX2INVOICELINE') 
					print allinvLineSet
					allLinecount = allinvLineSet.count()
					print allLinecount
					if allLinecount > 0 :
                                                print 'aaaaaaaaaaaaaaaaaaaaaaa'
						for j in range(allLinecount):
							invQuantity = invQuantity + allinvLineSet.getMbo(j).getInt('INVOICEQTY')
							print invQuantity
					invQuantity = invQuantity + invoiceLineMbo.getInt('INVOICEQTY')
					print invQuantity
					qtyDiff = recPOQuantity - invQuantity
					print qtyDiff
					if  (qtyDiff < 0):
						invcLineSet = invoiceLineMbo.getMboSet('EX2CREDITINV')  # Relationship to get invoiceline
						invclcount = invcLineSet.count()
						if invclcount > 0 :
							for k in range(invclcount):
								invcQuantitiy = invcQuantitiy - invcLineSet.getMbo(k).getInt('INVOICEQTY')
								if  (qtyDiff > invcQuantitiy):
									flag =1
						else :
							flag =1
						if (flag ==1):
                                                        print 'NNNNNNNNNNNNNNNNNNNNNNNNNN'
							invErrorSet = mbo.getMboSet("EX2IVERRORS")
							invErrorMbo=invErrorSet.add()
							invErrorMbo.setValue("ORGID", mbo.getString("ORGID"))
							invErrorMbo.setValue("SITEID", mbo.getString("SITEID"))
							invErrorMbo.setValue("EX2INVOICENUM", mbo.getString("INVOICENUM"))
							invErrorMbo.setValue("EX2ERRDESC", "Cannot approve invoice " +invoiceLineMbo.getString('invoicenum')+" because there are quantity mismatch for line "+invoiceLineMbo.getString('invoicelinenum')+" of purchase order "+invoiceLineMbo.getString('ponum')+".")
							invErrorMbo.setValue("EX2MSGSETID",  "MX")
							invErrorMbo.setValue("EX2MSGID",  "MX")
							invErrorMbo.setValue("EX2ERRDATE",  Date())
							if mbo.getString('STATUS') != 'MISMATCH' :
								mbo.changeStatus('MISMATCH',Date(),'Changed By PREVALIDATION')