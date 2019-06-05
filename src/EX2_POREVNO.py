# AUTOSCRIPT NAME: EX2_POREVNO
# CREATEDDATE: 2018-05-14 01:48:02
# CREATEDBY: U3LO
# CHANGEDATE: 2018-05-17 06:23:47
# CHANGEBY: U34H
# SCRIPTLANGUAGE: python
# STATUS: Draft

from psdi.server import MXServer

invoiceMbo=mbo.getOwner();
invoiceLineMboSet=invoiceMbo.getMboSet("INVOICELINE");
invoicenum=mbo.getString("INVOICENUM");
invoiceLineMboSet.reset();
invoiceMboSet=mbo.getMboSet("INVOICE");

descriptionInvoice=invoiceMbo.getString("DESCRIPTION");

poRevisioNum='';

invoiceMbo.setValue("DESCRIPTION","");

poMboSet=invoiceMbo.getMboSet("PO");
poMboSet.reset();

status=invoiceMbo.getString("STATUS");

if(poMboSet is not None and poMboSet!=''):
 poRevisioNum=poMboSet.getMbo(0).getString("REVISIONNUM");
 
invoicelineCount=invoiceLineMboSet.count();

if(invoicelineCount>0):
 for i in range(invoicelineCount) :
  invoicelineMbo=invoiceLineMboSet.getMbo(i);
  invoicelineMbo.setValue("POREVISIONNUM",poRevisioNum)

invoiceMbo.setValue("DESCRIPTION",descriptionInvoice);