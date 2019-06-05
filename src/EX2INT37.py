# AUTOSCRIPT NAME: EX2INT37
# CREATEDDATE: 2014-03-26 17:37:57
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-15 15:40:26
# CHANGEBY: UUN8
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.app.invoice import InvoiceRemote

if user=="MXINTADM" :
	status="APPR"
	mbo.createReverseInvoice(status)
        revInv=mbo.getMboSet('REVINVREVERSE')
        revInvcount = revInv.count()
        if revInvcount > 0 :
           revInv.getMbo(0).changeStatus('APPR',Date(),'Changed By INT37')