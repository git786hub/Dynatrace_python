# AUTOSCRIPT NAME: OSOUT.EX2EMTINVENTORY
# CREATEDDATE: 2016-08-19 22:20:34
# CREATEDBY: UGVD
# CHANGEDATE: 2016-08-19 22:20:34
# CHANGEBY: UGVD
# SCRIPTLANGUAGE: jython
# STATUS: Draft

#Script to calculate and update Quantity on Order value from the Open POs & Receipts.
from psdi.mbo import MboConstants
from psdi.mbo import Mbo


def overrideValues(ctx):

  totalorderedqty=0.0
  polinercvdqty=0.0
  polineordqty=0.0

  if ctx.getMboName()=='INVENTORY':
   mbo = ctx.getMbo()
   polineSet = mbo.getMboSet("EX2EMTQTYONODR")
   polcount = polineSet.count()

   for i in range(polcount):
     mbopoline = polineSet.getMbo(i)
     polineordqty = mbopoline.getInt("ORDERQTY")
     polinercvdqty = mbopoline.getInt("RECEIVEDQTY")
     totalorderedqty = totalorderedqty + polineordqty - polinercvdqty

   ctx.overrideCol("EX2QTYONORDER",totalorderedqty)