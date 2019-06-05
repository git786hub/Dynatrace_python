# AUTOSCRIPT NAME: EX2IVMISMATCHERR
# CREATEDDATE: 2014-05-05 12:13:09
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:14:25
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
from psdi.util import *
from psdi.app.invoice import InvoiceRemote
from psdi.mbo import *
from  java.util import *
from  java.lang import *
from  psdi.server import  MXServer
from psdi.security import UserInfo

if(mbo == None):
        print "******   MBO IS NULL ********** "
else:
        c = Calendar.getInstance()
        ivErrorSet = mbo.getMboSet("EX2IVERRORS")
        ivErrorMbo=ivErrorSet.add()
        ivErrorMbo.setValue("ORGID", mbo.getString("ORGID"))
        ivErrorMbo.setValue("SITEID", mbo.getString("SITEID"))
        ivErrorMbo.setValue("EX2INVOICENUM", mbo.getString("INVOICENUM"))
        ivErrorMbo.setValue("EX2ERRDESC", "The Invoice quantity exceeds the PO Line quantity on at least one Service or Standard Service line on this Invoice. Correct the Invoice Lines or contact the Buyer to revise the PO and continue processing.")
        ivErrorMbo.setValue("EX2MSGSETID",  "MX")
        ivErrorMbo.setValue("EX2MSGID",  "MX")
        ivErrorMbo.setValue("EX2ERRDATE",  c.getTime())
        ivErrorSet.save()