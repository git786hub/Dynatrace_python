# AUTOSCRIPT NAME: ITEMSTATUSROLLDOWN
# CREATEDDATE: 2014-08-22 04:05:46
# CREATEDBY: UVX3
# CHANGEDATE: 2014-08-22 07:36:46
# CHANGEBY: UM1R
# SCRIPTLANGUAGE: jython
# STATUS: Draft

status = mbo.getString("STATUS")
if status == "ACTIVE":
    itemorgSet = mbo.getMboSet("ITEMORGINFO")
    itemcnt = itemorgSet.count()
    for i in range(itemcnt):
        itemorgmbo = itemorgSet.getMbo(i)
        itemorgmbo.setValue("STATUS", status)