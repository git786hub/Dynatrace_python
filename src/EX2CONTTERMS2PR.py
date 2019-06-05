# AUTOSCRIPT NAME: EX2CONTTERMS2PR
# CREATEDDATE: 2013-12-16 18:38:08
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-09-07 07:02:31
# CHANGEBY: U0OT
# SCRIPTLANGUAGE: jython
# STATUS: Active

contset = mbo.getMboSet("CONTRACTREF")
if contset.count() > 0 :
    contmbo = contset.getMbo(0)
    pctermset = contmbo.getMboSet("CONTRACTTERM")
    if pctermset.count() > 0 :
        prtermset = mbo.getMboSet("PRTERM")
    for i in range(pctermset.count()):
        pctermmbo = pctermset.getMbo(i)
        prtermmbo = prtermset.add()
        prtermmbo.setValue("prnum",mbo.getString("prnum"))
        prtermmbo.setValue("seqnum",pctermmbo.getString("seqnum"),11L)
        prtermmbo.setValue("termid",pctermmbo.getString("termid"))
        prtermmbo.setValue("description",pctermmbo.getString("description"),11L)
        prtermmbo.setValue("orgid",mbo.getString("orgid"))
        prtermmbo.setValue("siteid",mbo.getString("siteid"))
        prtermmbo.setValue("canedit",pctermmbo.getBoolean("canedit"))
        prtermmbo.setValue("sendtovendor",pctermmbo.getBoolean("sendtovendor"))