# AUTOSCRIPT NAME: EX2DISTSPENDRESET
# CREATEDDATE: 2014-02-17 17:52:56
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:03:26
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
from psdi.mbo import MboConstants
from java.util import Calendar
from java.util import Date
import sys

# after first save, if user clicks the reset checkbox, reinitialize the values to primary vendor and all zeroes
if (not onadd) :

    # Use the Calendar to get the current Date/Time
    c = Calendar.getInstance()
    c.add(Calendar.SECOND,0)

    #mbo.setValue("ex2escalate", 1)   # flag for notification to contract buyer
    mbo.setValue("ex2primactive", 1)
    mbo.setValue("ex2primcurrqty", 0)
    mbo.setValue("ex2primitdqty", 0)
    mbo.setValue("ex2primactdate", c.getTime())
    mbo.setValue("ex2scndactive", 0)
    mbo.setValueNull("ex2scndcurrqty")
    mbo.setValueNull("ex2scndactdate")
    mbo.setValue("ex2scndcurrqty", 0)
    mbo.setValue("ex2scnditdqty", 0)
    #mbo.setValue("ex2reset", 0)    # reset the reset flag

    # use sql to activate / deactivate contract lines - set status APPR / WAPPR (cannot use mbo, it does not allow WAPPR coz active PO exists)
    qry1 = "update contractline set linestatus = 'APPR' where itemnum = '" + mbo.getString("ex2itemnum")
    qry1 = qry1 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
    qry1 = qry1 + mbo.getString("ex2primvendor") + "' and status = 'APPR')"
    qry2 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + mbo.getString("ex2itemnum")
    qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
    qry2 = qry2 + mbo.getString("ex2scndvendor") + "' and status = 'APPR')"
    ck = mbo.getUserInfo().getConnectionKey()
    conn = mbo.getMboServer().getDBConnection(ck)
    stmt = conn.createStatement()
    rs = stmt.executeQuery(qry1)
    rs = stmt.executeQuery(qry2)
    mbo.getMboServer().freeDBConnection(ck)
    stmt.close()
    rs.close()