# AUTOSCRIPT NAME: CG_COPYATTACHDOC
# CREATEDDATE: 2012-07-15 21:28:19
# CREATEDBY: UHD0
# CHANGEDATE: 2014-05-13 06:19:55
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

failurelistmboset = None
failurereportmboset = None
locMboSet = None
woAttachMboSet = None
locAttachMboSet = None
docInfoSet = None
pmMboSet = None

noerrgen = True

if status == "COMP" :
    failurelistmboset = mbo.getMboSet("CG_FAILURELIST")
    
    failurereportmboset = mbo.getMboSet("FAILUREREPORT")
    

    if mbo.getString("CG_WORKTYPE") == "Corrective" and mbo.isNull("CG_SUBWORKTYPE") and ((failurelistmboset.count() > 0 and not failurereportmboset.count() > 0) or  mbo.isNull("FAILURECODE") or mbo.isNull("CG_FAILUREREPORTEDBY") or mbo.isNull("REMARKDESC") or mbo.isNull("REMARKENTERDATE") or mbo.isNull("FAILDATE") )  :
        setError("cg_wottrn", "failureDetailsRequired", None)
        noerrgen = False


if status == "COMP" and mbo.getString("CG_SUBWORKTYPE") == "RSR" and mbo.getString("SITEID") == "TRN"  and noerrgen :
    locMboSet = mbo.getMboSet("LOCATION")
    
    if locMboSet.count() > 0:
        locMbo = locMboSet.getMbo(0)
        woAttachMboSet = mbo.getMboSet("PLUSCDOCLINKS")
        locAttachMboSet = locMbo.getMboSet("DOCLINKS")
        
      # Below section is commented out 
      # To avoid auto deletion of linked documents on workorder's location
      # for j in range (locAttachMboSet.count()) :
      #     locAttMbo = locAttachMboSet.getMbo(j)
      #     locAttMbo.delete()
        
        for i in range(woAttachMboSet.count()):
            woAttachMbo = woAttachMboSet.getMbo(i)

            if woAttachMbo.getString("OWNERTABLE") == "WORKORDER":
    
                locAttachMbo = locAttachMboSet.add()
                docInfoSet = locAttachMbo.getMboSet("DOCINFO")
                docInfo = docInfoSet.add()  
    
                locAttachMbo.setValue("DOCINFOID",docInfo.getString("DOCINFOID"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    
                locAttachMbo.setValue("DOCUMENT", woAttachMbo.getString("DOCUMENT"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                locAttachMbo.setValue("OWNERTABLE", "LOCATIONS", MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                locAttachMbo.setValue("OWNERID", locMbo.getUniqueIDValue(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                locAttachMbo.setValue("DOCTYPE", woAttachMbo.getString("DOCTYPE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                locAttachMbo.setValue("GETLATESTVERSION", woAttachMbo.getBoolean("GETLATESTVERSION"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)            
                locAttachMbo.setValue("COPYLINKTOWO", woAttachMbo.getBoolean("COPYLINKTOWO"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                
                locAttachMbo.setValue("URLTYPE", woAttachMbo.getString("URLTYPE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                
                locAttachMbo.setValue("URLNAME", woAttachMbo.getString("URLNAME"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)          

                docInfo.setValue("DOCUMENT",woAttachMbo.getString("DOCUMENT"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                docInfo.setValue("DESCRIPTION",woAttachMbo.getString("DOCINFO.DESCRIPTION"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                docInfo.setValue("DOCTYPE",woAttachMbo.getString("DOCTYPE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                docInfo.setValue("URLTYPE", woAttachMbo.getString("URLTYPE"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)                
                docInfo.setValue("URLNAME", woAttachMbo.getString("URLNAME"), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

if status == "COMP" and noerrgen  :
    pmMboSet = mbo.getMboSet("PM")
    if pmMboSet.count() > 0 :
        pmmbo = pmMboSet.getMbo(0)
        if not pmmbo.isNull("MASTERPM") :
            pmmbo.setValue("CG_PMGEN",pmmbo.getBoolean("MASTERPM.CG_AUTOGEN"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            pmmbo.setValue("CG_AUTOGEN",pmmbo.getBoolean("MASTERPM.CG_AUTOGEN"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

if (failurelistmboset is not None and not failurelistmboset.isEmpty()) :
   failurelistmboset.close()

if (failurereportmboset is not None and not failurereportmboset.isEmpty()) :
   failurereportmboset.close()

if (locMboSet is not None and not locMboSet.isEmpty()) :
   locMboSet.close()

if (woAttachMboSet is not None and not woAttachMboSet.isEmpty()) :
   woAttachMboSet.close()

if (locAttachMboSet is not None and not locAttachMboSet.isEmpty()) :
   locAttachMboSet.close()

if (docInfoSet is not None and not docInfoSet.isEmpty()) :
   docInfoSet.close()

if (pmMboSet is not None and not pmMboSet.isEmpty()) :
   pmMboSet.close()