# AUTOSCRIPT NAME: EX2INVENTORYCHECK
# CREATEDDATE: 2015-10-20 13:24:16
# CREATEDBY: U03V
# CHANGEDATE: 2019-02-07 16:41:56
# CHANGEBY: UGVD
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.app.po import PORemote
from psdi.app.pr import PRRemote
from psdi.server import MXServer


maximo = MXServer.getMXServer()

errmsg = ''
def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p


if (launchPoint in ["EX2POLINEINVENTORYCHECK","EX2PRLINEINVENTORYCHECK"]):

#ITO-19709 to clear out GL debit account when ever storeroom is removed from pr/po line # start
  initialValue=mbo.getMboValue("STORELOC").getPreviousValue().asString()
  if (initialValue!='' and mbo.getString("STORELOC")=='' and "1545000" in mbo.getString("GLDEBITACCT")):
    mbo.setValueNull("GLDEBITACCT",MboConstants.NOACCESSCHECK)
#ITO-19709 to clear out GL debit account when ever storeroom is removed from pr/po line # end

  owner = mbo.getOwner()
  if (isinstance(owner,PRRemote) or isinstance(owner,PORemote)) :
    if owner.getBoolean("INTERNAL"):
      InventoryMboSet = mbo.getMboSet("INVENTORY")
      if InventoryMboSet.count()==0 and storeloc is not None:
        setError("PRPO", "Item "+ mbo.getString("Itemnum") +" is not set up for selected Storeroom "+storeloc+". Please set up item first and then try.")

  if(storeloc is not None):
    if(isinstance(owner,PORemote) ):
      userInfo = mbo.getUserInfo()
      personid=mbo.getUserInfo().getPersonId()
      groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
      groupuserSet.setWhere("GROUPNAME in   ('INVENTORY','METERSHOP','METERSHOP2','ADMIN','ADMIN2','MAXADMIN','BUYER','SCMAPPROVER','AP','IVTOLERANCE','IVTOL4CMDTY','RBAWFADMIN','MAXADMDIS','MAXADMTRN','SCMADMIN','SERVICECOORD') and userid='"+personid+"'")
      groupuserSet1=maximo.getMboSet("PERSONGROUPTEAM",userInfo)
      groupuserSet1.setWhere("PERSONGROUP = 'SR"+storeloc+ "' and respparty='"+personid+"'")
      print '$$$$$$$$$$$$ in PR/PO APp'
      print groupuserSet1.getWhere()
      print groupuserSet.getWhere()
      if (groupuserSet.count()==0 and groupuserSet1.count()==0):
        setError("Inventory", "User Does not have access to selected storeroom")


#ITO-43396 to clear out storeroom when ever gl debit acount is modified from pr/po line # start

if (launchPoint in ["EX2PRLINECONTROLACCCHCK","EX2POLINECONTROLACCCHCK"]):
 
  initialValue=mbo.getMboValue("GLDEBITACCT").getPreviousValue().asString()
  storeloc=mbo.getString("STORELOC")
  if (initialValue!='' and interactive and mbo.getString("STORELOC")!=''):
    invset=mbo.getMboSet("INVENTORY")
    if (invset.isEmpty()==False):
      if (invset.getMbo(0).getBoolean("CONSIGNMENT")==False and mbo.getString("GLDEBITACCT")=='' ):
        mbo.setValueNull("STORELOC",MboConstants.NOACCESSCHECK)
      elif( invset.getMbo(0).getBoolean("CONSIGNMENT")==False and "1545000" not in mbo.getString("GLDEBITACCT")):
        setError("prline","ex2prlineinvgldebtacctval", [storeloc])
  if (mbo.getString("STORELOC")=='' and mbo.getString("GLDEBITACCT")!='' and "1545000" in mbo.getString("GLDEBITACCT")):
    mbo.setValueNull("GLDEBITACCT",MboConstants.NOACCESSCHECK)

#ITO-43396 to clear out storeroom when ever gl debit acount is modified from pr/po line # end