# AUTOSCRIPT NAME: EX2_ITEMORGSTATUS
# CREATEDDATE: 2016-09-07 04:16:33
# CREATEDBY: U03V
# CHANGEDATE: 2016-09-07 04:16:33
# CHANGEBY: UXHD
# SCRIPTLANGUAGE: python
# STATUS: Draft

status = mbo.getString("STATUS")
if status == "PENDOBS":
    itemorgSet = mbo.getMboSet("ITEMORGINFO")
    itemcnt = itemorgSet.count()
    for i in range(itemcnt):
        itemorgmbo = itemorgSet.getMbo(i)
        itemorgmbo.setValue("STATUS", status)
    inventoryset=mbo.getMboSet("INVENTORY")
    inventorycnt = inventoryset.count()
    for i in range(inventorycnt):
        inventorymbo = inventoryset.getMbo(i)
        inventorymbo.setValue("STATUS", status,11L)