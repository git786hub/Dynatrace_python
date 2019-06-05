# AUTOSCRIPT NAME: UPDASSCPM
# CREATEDDATE: 2012-05-08 05:38:05
# CREATEDBY: UHD0
# CHANGEDATE: 2018-08-27 01:37:36
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
MboConstants.NOACCESSCHECK

sitemboset = mbo.getMboSet("SITE")
numsite = sitemboset.count()
for i in range(numsite) :
    sitembo = sitemboset.getMbo(i)
    if sitembo and sitembo.getString("SITEID") == "TRN"  :
        sitembo.select()

mbo.updateAssociatedPMs(sitemboset)
pmmboset = mbo.getMboSet("PM")
numpm = pmmboset.count()

for j in range(numpm) :
    pmmbo = pmmboset.getMbo(j)
    if pmmbo :
        if not pmmbo.getBoolean("OVERRIDEMASTERUPD") :
            pmmbo.setValue("CG_AUTOGEN",mbo.getString("CG_AUTOGEN"))
            pmmbo.setValue("PRIORITY",mbo.getString("PRIORITY")) 
            pmmbo.setValue("LEADTIME",mbo.getString("LEADTIME"),MboConstants.NOACCESSCHECK) 

            pmbitemset = pmmbo.getMboSet("CG_PMBUILDITEMRECORDS")
            countpmbitem = pmbitemset.count()

            if countpmbitem > 0 and (pmmbo.getString("STATUS") not in [ "ACTIVE","SUSPEND"] ) :
                pmmbo.setValue("STATUS","ACTIVE")

            if countpmbitem <= 0 and (pmmbo.getString("STATUS") in [ "ACTIVE","SUSPEND"]) :
                pmmbo.setValue("STATUS","INACTIVE")

pmmboset.save()