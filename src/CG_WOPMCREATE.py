# AUTOSCRIPT NAME: CG_WOPMCREATE
# CREATEDDATE: 2013-09-13 02:51:25
# CREATEDBY: UFDA
# CHANGEDATE: 2014-09-26 01:56:13
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants


pmrecall = None
masterpmrecall=None
pmrecall = mbo.getMboSet("PM")
pmrec = pmrecall.getMbo(0)
masterpmrecall= pmrec. getMboSet("MASTERPM")
masterpmrec= masterpmrecall.getMbo(0)
if (masterpmrec.getInt("APPLYMPMTOLOC")) == 1:
      if len(pmrec.getString("LOCATION"))  > 0:
          if len(pmrec.getString("ASSETNUM"))  == 0:
              mbo.setValue("ASSETNUM"," ")