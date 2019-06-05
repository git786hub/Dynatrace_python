# AUTOSCRIPT NAME: RBACRSPEC2
# CREATEDDATE: 2011-11-22 15:20:07
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2011-11-22 17:29:04
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

import sys

print "in Create Specification Attribute script"

try: 
   specMboSet = scriptHome.getMboSet("TICKETSPEC")
   specMbo = specMboSet.add()
   specMbo.setValue("assetattrid", spec_attr)
   print "Specification Attribute " + spec_attr +  " was created successfully"
   rba_rc = "0"

except:
   print "Error creating specification attribute : ", sys.exc_info()
   rba_rc = "1"