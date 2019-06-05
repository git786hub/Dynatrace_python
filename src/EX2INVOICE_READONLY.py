# AUTOSCRIPT NAME: EX2INVOICE_READONLY
# CREATEDDATE: 2016-04-07 04:27:23
# CREATEDBY: UVX3
# CHANGEDATE: 2016-04-20 08:01:17
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: python
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.app.invoice import InvoiceRemote

if(isinstance(mbo, InvoiceRemote) and mbo.getString("STATUS")=='PAID'):
   fields1 = ['EX2EXTREMARKS', 'EX2INTREMARKS', 'EX2INVAPPR', 'EX2PREPAID', 'EX2CONTROLAMT','REMITADDRESS4','EX2PSACCRUE']
   mbo.setFieldFlag(fields1,MboConstants.READONLY, True)
  
if(isinstance(mbo, InvoiceRemote) and mbo.getString("STATUS")=='CLEARED'):
   fields2 = ['EX2EXTREMARKS','EX2INTREMARKS','EX2INVAPPR','EX2PREPAID','PAIDDATE','CHECKNUM','BANKACCOUNT','EX2BANK',
   'EX2CONTROLAMT','REMITADDRESS4','CHECKCODE','EX2PSACCRUE']
   mbo.setFieldFlag(fields2,MboConstants.READONLY, True)
 
else:
   mbo.setFieldFlag('REMITADDRESS4',MboConstants.READONLY, True)