# AUTOSCRIPT NAME: EX1ITEMORGINFOSTATUS
# CREATEDDATE: 2014-08-12 05:15:12
# CREATEDBY: UM1R
# CHANGEDATE: 2014-09-04 11:38:08
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

istatus = mbo.getString("STATUS")
itemorgSet = mbo.getMboSet("EX1ITEMORGINFO")
itemcnt = itemorgSet.count()
for i in range(itemcnt):
    itemorgmbo = itemorgSet.getMbo(i)
    orgid = itemorgmbo.getString("ORGID")
    if orgid == "ONCOR":
        itemorgmbo.setValue("STATUS", "PENDING")