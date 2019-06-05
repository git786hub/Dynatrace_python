# AUTOSCRIPT NAME: EX2UPDATEDISTSPEND
# CREATEDDATE: 2014-02-14 13:21:41
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-02-09 01:43:18
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
from psdi.mbo import MboConstants
import sys
 
# look for po lines with distributed-spend items
if mbo.getInt("REVISIONNUM") ==0:
	polset = mbo.getMboSet("POLINE")
	vendor = "nobody"
	poorderdate = ""                                               # vender should initialized once ticket INC000001140016 
	for i in range(polset.count()) :
		polmbo = polset.getMbo(i)
		if i == 0 :    # get PO vendor (just once)
			vendor = mbo.getString("vendor")
		poorderdate = mbo.getDate("orderdate")
	 
		dsset = polmbo.getMboSet("ex2distspend")
		if dsset.count() > 0 :     # if dist spending on this item
			dsmbo = dsset.getMbo(0)
			dsmbo.setFlag(MboConstants.READONLY, False)
			ex2effdate=dsmbo.getDate("EX2EFFDATE")

	  # primary vendor on PO, add to his total.Ticket 1140016
			if vendor == dsmbo.getString("ex2primvendor") and dsmbo.getBoolean("ex2primactive")==1 and ex2effdate < poorderdate: 
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
					dsmbo.setValue("ex2primcurrqty", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)	 # change 				
					 

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

	 # secondary vendor on PO, add to his total. Ticket 1140016

			elif vendor == dsmbo.getString("ex2scndvendor") and dsmbo.getBoolean("ex2scndactive")==1 and ex2effdate < poorderdate:   
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
					dsmbo.setValue("EX2SCNDCURRQTY", 0, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)    # change

					

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