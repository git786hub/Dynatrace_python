# AUTOSCRIPT NAME: EX2UPDATEDISTSPENDAPPR
# CREATEDDATE: 2015-11-18 04:09:25
# CREATEDBY: U03V
# CHANGEDATE: 2017-02-16 00:31:46
# CHANGEBY: U171
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.security import UserInfo
from psdi.mbo import MboConstants
import sys
 
# look for po lines with distributed-spend items
print '---------------------------------INC000001140016 ------------------------------------------1---------------------------'
if mbo.getInt("REVISIONNUM") ==0:
        print '---------------------------------INC000001140016 ------------------------------------------2---------------------------'
	polset = mbo.getMboSet("POLINE")
        polset.setFlag(MboConstants.READONLY, False)
	vendor = "nobody"
	poorderdate = ""                                               # vender should initialized once ticket INC000001140016 
	for i in range(polset.count()) :
		polmbo = polset.getMbo(i)
 		if i == 0 :    # get PO vendor (just once)
			vendor = mbo.getString("vendor")
		poorderdate = mbo.getDate("orderdate")
	 
		dsset = polmbo.getMboSet("ex2distspend")
		if dsset.count() > 0 :     # if dist spending on this item
			apprdsSet = polmbo.getMboSet("EX2DISTSPENDAPPR")
			if apprdsSet.count()==0:
                                print '---------------------------------INC000001140016 ------------------------------------------3---------------------------'
				dsmbo = dsset.getMbo(0)
				dsmbo.setFlag(MboConstants.READONLY, False)
				ex2effdate=dsmbo.getDate("EX2EFFDATE")

		  # primary vendor on PO, add to his total.Ticket 1140016
				if vendor == dsmbo.getString("ex2primvendor") and dsmbo.getBoolean("ex2primactive")==1 and ex2effdate < poorderdate: 
                                        print '---------------------------------INC000001140016 ------------------------------------------4---------------------------'
					currqty = dsmbo.getDouble("ex2primcurrqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2primcurrqty", currqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					itdqty = dsmbo.getDouble("ex2primitdqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2primitdqty", itdqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					dsmbo.setValue("ex2scndcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change 
					dsmbo.setValue("ex2ponum",mbo.getString("ponum") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change

					if currqty >= dsmbo.getDouble("ex2primspendqty") :   # maxed out spend quantity, swap to secondary vendor
						dsmbo.setValue("ex2escalate", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)   # flag for notification to contract buyer
						dsmbo.setValue("ex2primactive", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2scndactive", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2scndactdate", mbo.getDate("changedate"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValueNull("ex2primactdate", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)   
						dsmbo.setValue("ex2primcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change 						
						 

						# use sql to activate/deactivate contractlines-set status APPR/WAPPR cannot use mbo,it does not allow WAPPR cz active PO exists
						qry1 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + polmbo.getString("itemnum")
						qry1 = qry1 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry1 = qry1 + dsmbo.getString("ex2primvendor") + "' and status = 'APPR')"
						qry2 = "update contractline set linestatus = 'APPR' where itemnum = '" + polmbo.getString("itemnum")
						qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry2 = qry2 + dsmbo.getString("ex2scndvendor") + "' and status = 'APPR')"
						ck = mbo.getUserInfo().getConnectionKey()
						conn = mbo.getMboServer().getDBConnection(ck)
						stmt = conn.createStatement()
						rs = stmt.executeQuery(qry1)
						rs = stmt.executeQuery(qry2)
						mbo.getMboServer().freeDBConnection(ck)
						stmt.close()
						rs.close()
						
						
		  # primary vendor on PO, add to his total.Ticket 1140016
				elif vendor == dsmbo.getString("ex2primvendor") and dsmbo.getBoolean("ex2primactive")==0 and ex2effdate < poorderdate:
                                        print '---------------------------------INC000001140016 ------------------------------------------5---------------------------' 
					currqty = dsmbo.getDouble("ex2scndcurrqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2scndcurrqty", currqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					itdqty = dsmbo.getDouble("ex2scnditdqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2scnditdqty", itdqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					dsmbo.setValue("ex2ponum",mbo.getString("ponum") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change
					contractSet=dsmbo.getMboSet("EX2SCNDCONTRACT1")
					if contractSet.count()>0:
						mbo.setValue("vendor",dsmbo.getString("ex2scndvendor"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOACTION)
						contractmbo=contractSet.getMbo(0)
						mbo.setValue("contractrefnum",contractmbo.getString("contractnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						mbo.setValue("contractrefid",contractmbo.getString("contractid"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						mbo.setValue("contractrefrev",contractmbo.getString("revisionnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						polmbo.setValue("contractrefnum",contractmbo.getString("contractnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						polmbo.setValue("contractrefid",contractmbo.getString("contractid"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						polmbo.setValue("contractrefrev",contractmbo.getString("revisionnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					if currqty >= dsmbo.getDouble("ex2scndspendqty") :   # maxed out spend quantity, swap to primary vendor
						dsmbo.setValue("ex2escalate", 1,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)   # flag for notification to contract buyer
						dsmbo.setValue("ex2scndactive", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2primactive", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2primactdate", mbo.getDate("changedate"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValueNull("ex2scndactdate", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)   # change		
						dsmbo.setValue("ex2scndcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change 						

						# use sql to activate/deactivate contractlines-set status APPR/WAPPR(cannot use mbo,it doesnt allow WAPPR cz active PO exists
						qry1 = "update contractline set linestatus = 'APPR' where itemnum = '" + polmbo.getString("itemnum")
						qry1 = qry1 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry1 = qry1 + dsmbo.getString("ex2primvendor") + "' and status = 'APPR')"
						qry2 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + polmbo.getString("itemnum")
						qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry2 = qry2 + dsmbo.getString("ex2scndvendor") + "' and status = 'APPR')"
						ck = mbo.getUserInfo().getConnectionKey()
						conn = mbo.getMboServer().getDBConnection(ck)
						stmt = conn.createStatement()
						rs = stmt.executeQuery(qry1)
						rs = stmt.executeQuery(qry2)
						mbo.getMboServer().freeDBConnection(ck)
						stmt.close()
						rs.close()
						
		 # secondary vendor on PO, add to his total. Ticket 1140016

				elif vendor == dsmbo.getString("ex2scndvendor") and dsmbo.getBoolean("ex2scndactive")==1 and ex2effdate < poorderdate:   
                                        print '---------------------------------INC000001140016 ------------------------------------------6---------------------------'
					currqty = dsmbo.getDouble("ex2scndcurrqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2scndcurrqty", currqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					itdqty = dsmbo.getDouble("ex2scnditdqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2scnditdqty", itdqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					dsmbo.setValue("ex2primcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change 
					dsmbo.setValue("ex2ponum",mbo.getString("ponum") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change
		 
					if currqty >= dsmbo.getDouble("ex2scndspendqty") :   # maxed out spend quantity, swap to primary vendor
						dsmbo.setValue("ex2escalate", 1,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)   # flag for notification to contract buyer
						dsmbo.setValue("ex2scndactive", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2primactive", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2primactdate", mbo.getDate("changedate"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValueNull("ex2scndactdate", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)   # change
						dsmbo.setValue("ex2scndcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change 
						
						# use sql to activate/deactivate contractlines-set status APPR/WAPPR(cannot use mbo,it doesnt allow WAPPR cz active PO exists
						qry1 = "update contractline set linestatus = 'APPR' where itemnum = '" + polmbo.getString("itemnum")
						qry1 = qry1 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry1 = qry1 + dsmbo.getString("ex2primvendor") + "' and status = 'APPR')"
						qry2 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + polmbo.getString("itemnum")
						qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry2 = qry2 + dsmbo.getString("ex2scndvendor") + "' and status = 'APPR')"
						ck = mbo.getUserInfo().getConnectionKey()
						conn = mbo.getMboServer().getDBConnection(ck)
						stmt = conn.createStatement()
						rs = stmt.executeQuery(qry1)
						rs = stmt.executeQuery(qry2)
						mbo.getMboServer().freeDBConnection(ck)
						stmt.close()
						rs.close()
						
				elif vendor == dsmbo.getString("ex2scndvendor") and dsmbo.getBoolean("ex2scndactive")==0 and ex2effdate < poorderdate: 
                                        print '---------------------------------INC000001140016 ------------------------------------------7---------------------------'
					currqty = dsmbo.getDouble("ex2primcurrqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2primcurrqty", currqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					itdqty = dsmbo.getDouble("ex2primitdqty") + polmbo.getDouble("orderqty")
					dsmbo.setValue("ex2primitdqty", itdqty, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
					dsmbo.setValue("ex2scndcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change 
					dsmbo.setValue("ex2ponum",mbo.getString("ponum") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change
					contractSet=dsmbo.getMboSet("EX2PRIMCONTRACT1")
					if contractSet.count()>0:
						mbo.setValue("vendor",dsmbo.getString("ex2primvendor"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOACTION)
						contractmbo=contractSet.getMbo(0)
						mbo.setValue("contractrefnum",contractmbo.getString("contractnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						mbo.setValue("contractrefid",contractmbo.getString("contractid"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						mbo.setValue("contractrefrev",contractmbo.getString("revisionnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						polmbo.setValue("contractrefnum",contractmbo.getString("contractnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						polmbo.setValue("contractrefid",contractmbo.getString("contractid"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						polmbo.setValue("contractrefrev",contractmbo.getString("revisionnum"),MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)

					if currqty >= dsmbo.getDouble("ex2primspendqty") :   # maxed out spend quantity, swap to secondary vendor
						dsmbo.setValue("ex2escalate", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)   # flag for notification to contract buyer
						dsmbo.setValue("ex2primactive", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2scndactive", 1, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2scndactdate", mbo.getDate("changedate"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValueNull("ex2primactdate", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
						dsmbo.setValue("ex2primcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)      # change 
						
						

						# use sql to activate/deactivate contractlines-set status APPR/WAPPR cannot use mbo,it does not allow WAPPR cz active PO exists
						qry1 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + polmbo.getString("itemnum")
						qry1 = qry1 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry1 = qry1 + dsmbo.getString("ex2primvendor") + "' and status = 'APPR')"
						qry2 = "update contractline set linestatus = 'APPR' where itemnum = '" + polmbo.getString("itemnum")
						qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
						qry2 = qry2 + dsmbo.getString("ex2scndvendor") + "' and status = 'APPR')"
						ck = mbo.getUserInfo().getConnectionKey()
						conn = mbo.getMboServer().getDBConnection(ck)
						stmt = conn.createStatement()
						rs = stmt.executeQuery(qry1)
						rs = stmt.executeQuery(qry2)
						mbo.getMboServer().freeDBConnection(ck)
						stmt.close()
						rs.close()