# AUTOSCRIPT NAME: EX2VALGLPRLINE
# CREATEDDATE: 2015-11-17 06:34:10
# CREATEDBY: U03V
# CHANGEDATE: 2018-01-25 01:59:39
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.server import MXServer

maximo = MXServer.getMXServer()
def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e

def setError(g, e, p):
        global errorgroup, errorkey, params
        errorgroup = g
        errorkey = e
        params= p

userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()

if launchPoint == 'EX2VALGLPRLINE' and app=='PR' and mbo.getString("STATUS")=='APPR':
	prlset = mbo.getMboSet("PRLINE")
	num = prlset.count()
	i = 0
	for i in range(num):
		prlmbo = prlset.getMbo(i)
		mGLdebit = prlmbo.getString("GLDEBITACCT")
		print '################'
		print mGLdebit 
		if '?' in mGLdebit:
			setError("WOGLACCOUNT", "EnterCompleteGLAcount")

if launchPoint == 'EX2LOWCOST' and app == 'PLUSDWOTRK' and mbo.getString("STATUS")=='APPR':
	wpset = mbo.getMboSet("SHOWPLANMATERIAL")
	num = wpset.count()
	itemnum_param=''
	i = 0
	for i in range(num):
        	wpmbo=wpset.getMbo(i)
                itemnum =wpmbo.getString("ITEMNUM")
		itemSet=maximo.getMboSet("ITEM",userInfo)
		itemSet.setWhere("ITEMNUM='"+itemnum+"'");
        	woactSet=mbo.getMboSet("WOACTIVITY")
		woactSet.setWhere("TASKID='"+wpmbo.getString("TASKID")+"'");
        	glACct= woactSet.getMbo(0).getString("GLACCOUNT")  
        	if glACct is not None:
			if ( itemSet.getMbo(0).getString("EX2LOWCOST")== 'N' and 'DDLOWCST' in glACct):
				if itemnum_param =='' :
					itemnum_param=itemnum
				else:
					itemnum_param=itemnum_param+", "+itemnum
        
	if itemnum_param !='' :
		setError("EX2WO","LowCost item", [itemnum_param, glACct ])

if launchPoint=='EX2WOACTIVITY' and app!='PLUSDWOTRK' :
  glacct = mbo.getString("GLACCOUNT")
  item1=''
  wpmatset=mbo.getMboSet("WPMATSET")
  i=0
  num=wpmatset.count()
  if (wpmatset is not None):
    for i in range(num):
      wpmatmbo=wpmatset.getMbo(i)
      wpmatItemset=wpmatmbo.getMboSet("ITEM")
      itemnum=wpmatmbo.getString('ITEMNUM')
      if(wpmatItemset.getMbo(0).getString("EX2LOWCOST")== 'N' and 'DDLOWCST' in glacct):
        if (item1==''):
          item1=itemnum
        else: 
          item1=item1 + ", " + itemnum
  if (item1 !=''):
    setError("EX2WO","LowCost item", [item1, glacct ])