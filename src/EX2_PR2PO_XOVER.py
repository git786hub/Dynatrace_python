# AUTOSCRIPT NAME: EX2_PR2PO_XOVER
# CREATEDDATE: 2013-10-21 10:24:24
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-09-26 04:16:59
# CHANGEBY: U0OT
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
from psdi.mbo import MboConstants 
import sys
    
# set source of record creation for use in escalations and workflow
# logic is 1) set from interface source ID      2) set from app vbl (if populated)     3) (in crossover code) indicate whether from PR or RFQ app based on homogeneous lines
#        (code at end of script)      4) set as reorder if the description looks like that       5) set to "unknown"
if onadd:
    if not mbo.isNull("sourcesysid"):     # 1) if from interface, use source system
        mbo.setValue("ex2posource", mbo.getString("sourcesysid"))
    else:                              # 2) if the app is set, use that
        mbo.setValue("ex2posource", app)

    contset = mbo.getMboSet("PURCHVIEW")
    if contset.count() > 0 :
        contmbo = contset.getMbo(0)
        if mbo.getString("revisionnum")=="0":
            mbo.setValue("purchaseagent", contmbo.getString("purchaseagent"))

    # crossover code - detect whether all lines have same rfqnum or prnum, and if so, get source data using sqlformat-style query 
    ###print "XXXX XXXX PO %s ran on po %s %s XXXX XXXX "  %  (launchPoint, mbo.getString("siteid"), mbo.getString("ponum"))
    polset = mbo.getMboSet("POLINE")
    ###print "XXXX XXXX PO isnew - %d lines, status %s XXXX XXXX "  %  (polset.count(), mbo.getString("status"))

    if polset.count() > 0:
        polset.setOrderBy("rfqnum asc")   # check for all rfqnums the same by using order-by and checking first and last
        polmbo = polset.getMbo(0)
        polmbo2 = polset.getMbo(polset.count() - 1)      # used for all-lines-the-same check

        # only cross over RFQ header info if all lines from same RFQ
        if not polmbo.isNull("rfqnum") and polmbo2.getString("rfqnum") == polmbo.getString("rfqnum"):
            if mbo.isNull("ex2posource") :
                mbo.setValue("ex2posource", 'RFQ')     # 3A) source is RFQ app

            # could not get the RFQ mbo, it must be locked when creating PO from RFQ, so use rowset to select the RFQ from the database
            ck = mbo.getUserInfo().getConnectionKey()
            conn = mbo.getMboServer().getDBConnection(ck)
            stmt = conn.createStatement()
            ###print "XXXXXXXXXXXXX select rfqnum, status, ex2project, ex2tasksow, ex2dernum, requestedby, purchaseagent from rfq where rfqnum = '" + polmbo.getString("rfqnum") + "' and siteid = '" + polmbo.getString("siteid") + "'"
            rs = stmt.executeQuery("select rfqnum, status, ex2project, ex2tasksow, ex2dernum, requestedby, purchaseagent from rfq where rfqnum = '" + polmbo.getString("rfqnum") + "' and siteid = '" + polmbo.getString("siteid") + "'")
            if rs.next():
                ###print "XXXX XXXX PO QUERY- RFQ status %s XXXX XXXX"  %  (rs.getString("status"))  
                mbo.setValue("ex2project",rs.getString("ex2project"))  
                mbo.setValue("ex2tasksow",rs.getString("ex2tasksow"))  
                mbo.setValue("ex2dernum",rs.getString("ex2dernum"))  
                mbo.setValue("ex2requestedby",rs.getString("requestedby"))
                if mbo.isNull("purchaseagent") :
                    mbo.setValue("purchaseagent",rs.getString("purchaseagent"))

            mbo.getMboServer().freeDBConnection(ck)
            stmt.close()
            rs.close()

        else:       # not RFQ, try PR
            polset.setOrderBy("prnum asc")   # check for all prnums the same by using order-by and checking first and last
            polmbo = polset.getMbo(0)
            polmbo2 = polset.getMbo(polset.count() - 1)      # used for all-lines-the-same check
            # only cross over PR header info if all lines from same PR (and not all from same RFQ)
            if not polmbo.isNull("prnum") and polmbo2.getString("prnum") == polmbo.getString("prnum"):
                if mbo.isNull("ex2posource") :
                    mbo.setValue("ex2posource", 'PR')       # 3B) source is PR app

                # could not get the PR mbo, it must be locked when creating PO from PR, so use rowset to select the PR from the database
                ck = mbo.getUserInfo().getConnectionKey()
                conn = mbo.getMboServer().getDBConnection(ck)
                stmt = conn.createStatement()
                ###print "XXXXXXXXXXXXX select prnum, status, ex2project, ex2tasksow, ex2dernum, requestedby, ex2buyer, ex2invappr, ex2dropship from pr where prnum = '" + polmbo.getString("prnum") + "' and siteid = '" + polmbo.getString("siteid") + "'"
                rs = stmt.executeQuery("select prnum, status, ex2project, ex2tasksow, ex2dernum, requestedby, ex2buyer, ex2invappr, ex2dropship from pr where prnum = '" + polmbo.getString("prnum") + "' and siteid = '" + polmbo.getString("siteid") + "'")
                if rs.next():
                    ###print "XXXX XXXX PO QUERY- PR status %s XXXX XXXX"  %  (rs.getString("status"))  
                    mbo.setValue("ex2project",rs.getString("ex2project"))  
                    mbo.setValue("ex2tasksow",rs.getString("ex2tasksow"))  
                    mbo.setValue("ex2dernum",rs.getString("ex2dernum"))  
                    mbo.setValue("ex2requestedby",rs.getString("requestedby"))
                    mbo.setValue("ex2invappr",rs.getString("ex2invappr"))  
                    mbo.setValue("ex2dropship",rs.getString("ex2dropship"))  
                    if mbo.isNull("purchaseagent") :
                        mbo.setValue("purchaseagent",rs.getString("ex2buyer"))

                mbo.getMboServer().freeDBConnection(ck)
                stmt.close()
                rs.close()

    if mbo.isNull("ex2posource"):       # 4) if source is still not set (no interface, app vbl not populated), assumereorder -- check description to make sure
        if mbo.getString("DESCRIPTION")[0:21] ==   "Generated by reorder ":
            mbo.setValue("ex2posource", "Reorder")
        else:
            mbo.setValue("ex2posource", "Unknown")        # 5) all else fails

    if (mbo.getString("ex2posource") == "PR" or mbo.getString("ex2posource") == "RFQ") and mbo.isNull("purchaseagent") :
        userset = mbo.getMboSet("ex2userisbuyer")        # buyer must be in BUYER user group, else hardcode known generic buyer user
        if userset.count() > 0 :
            mbo.setValue("purchaseagent", mbo.getUserInfo().getLoginID())
        else :
            mbo.setValue("purchaseagent", "MXINTADM")
    
    
    if (mbo.getString("ex2posource") == "PR" and mbo.isNull("ex2requestedby")) :
        mbo.setValue("ex2requestedby", "MXINTADM")