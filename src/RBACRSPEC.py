# AUTOSCRIPT NAME: RBACRSPEC
# CREATEDDATE: 2011-11-22 10:47:30
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2011-11-23 09:38:37
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