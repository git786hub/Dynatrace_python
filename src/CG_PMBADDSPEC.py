# AUTOSCRIPT NAME: CG_PMBADDSPEC
# CREATEDDATE: 2012-04-10 04:19:20
# CREATEDBY: UHD0
# CHANGEDATE: 2012-06-07 18:24:01
# CHANGEBY: UWUD
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.item import ItemRemote

ownermbo = mbo.getOwner()
pmbuildspecset = mbo.getMboSet("CG_PMBUILDSPEC")
num = pmbuildspecset.count()

if isinstance(ownermbo,ItemRemote) and num == 0 and ownermbo.getBoolean("CG_PMBUILD") :
    pmbuildspecmbo = pmbuildspecset.add()
    pmbuildspecmbo.setValue("ASSETATTRID",mbo.getString("ASSETATTRID"))
    pmbuildspecmbo.setValue("ITEMNUM",mbo.getString("ITEMNUM"))
    pmbuildspecmbo.setValue("CLASSSTRUCTUREID",mbo.getString("CLASSSTRUCTUREID"))