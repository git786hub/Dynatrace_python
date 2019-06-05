# AUTOSCRIPT NAME: IPVALIDATOR
# CREATEDDATE: 2009-04-17 11:50:54
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2011-02-02 14:14:14
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

errmsg = ''
rc = 1
ipList = newValue.split('.')
if len(ipList) == 4:
   for i in ipList:
      try:
         i = int(i)
      except:
         rc = 0
         errmsg = i, ' is not a valid number. IP Addresses must contain valid numbers'
         break
      if i > 255:
         rc = 0
         errmsg = i, ' is greater than 255. Valid IP Addresses are between 0 and 255.'
         break
else:
   rc = 0
   errmsg = 'IP Addresses must be in the form nn.nn.nn.nn'
print rc
print errmsg