# AUTOSCRIPT NAME: UPLOADDOC
# CREATEDDATE: 2015-03-05 21:11:42
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-01-06 06:00:00
# CHANGEBY: U144
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.invoice import InvoiceRemote
from psdi.mbo import MboConstants

global mbo

status = mbo.getString("STATUS")

if isinstance(mbo, InvoiceRemote) and ((mbo.getInternalStatus() == 'PAID') or (status=='CLEARED')):
  fields = ['EX2EXTREMARKS', 'EX2INTREMARKS', 'EX2INVAPPR', 'EX2PREPAID', 'EX2CONTROLAMT','EX2PSACCRUE']
  mbo.setFlag(7,False)
  mbo.setFieldFlag(fields, 7, True)
  mbo.setFieldFlag("EX2INTREMARKS",7,False)
  mbo.setFlag(524295,False)

# Added the below two lines for the defect 39 of Maximo 7.6 Upgrade Project

  mboSet= mbo.getMboSet("DOCLINKS")
  mboSet.setFlag(7, False)