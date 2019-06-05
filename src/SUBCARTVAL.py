# AUTOSCRIPT NAME: SUBCARTVAL
# CREATEDDATE: 2009-04-17 11:56:20
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2011-02-02 14:14:14
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

rc = 1
errmsg = ''

foundPMSC_2021A = False
foundPMSC_2007A = False

numItems = len(itemsInCart)

for i in range(numItems):
   item  = itemsInCart[i]
   if item != None:
      itemnum = item.getString("PMSCITEMNUM")
      if itemnum == 'PMSC_2021A':
         attrs = itemAttributes[i]
         dbyesno = attrs.getValue("INSTDB")
         if dbyesno == '1':
            foundPMSC_2021A = True
      elif itemnum == 'PMSC_2007A':
         foundPMSC_2007A = True

if foundPMSC_2021A == True and foundPMSC_2007A == False:
      rc = 0
      errmsg = 'If Build New Server with Middleware is in the cart and the Install DB attribute is 1, then the Add Database To Server offering must also be included in the cart'

print rc
print errmsg