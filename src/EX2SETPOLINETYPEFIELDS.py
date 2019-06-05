# AUTOSCRIPT NAME: EX2SETPOLINETYPEFIELDS
# CREATEDDATE: 2013-10-31 09:14:43
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-06-01 00:11:08
# CHANGEBY: U3LO
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote

# set PO header service-PO flag when all the lines are a service type
# currently does not fire on the delete event

pombo = mbo.getOwner()
# if poline object owner is not the PO header, get it using the relationship 
if not pombo or not isinstance(pombo,PORemote):   
    pombo = mbo.getMboSet("PO").getMbo(0)

if pombo and isinstance(pombo,PORemote):
    oldsvcpo = pombo.getBoolean("ex2servicepo")   #remember current value, so only set new value if different
    newsvcpo = False
    # loop thru all the current lines
    polset = mbo.getThisMboSet()
    num = polset.count()
    i = 0
    ###pombo.setValue("description", pombo.getString("description") + " " + launchPoint)
    for i in range(num):
        polmbo = polset.getMbo(i)
        ###pombo.setValue("description", pombo.getString("description") + " " + str(polmbo.getInt("polinenum")) + " " + polmbo.getString("linetype"))
        if (polmbo.getString("linetype") == "SERVICE" or polmbo.getString("linetype") == "STDSERVICE") and not polmbo.toBeDeleted() :
            ###pombo.setValue("description", pombo.getString("description") + " T ")
            newsvcpo = True
        elif not polmbo.toBeDeleted():
            ###pombo.setValue("description", pombo.getString("description") + " F ")
            newsvcpo = False
            break
    if oldsvcpo <> newsvcpo :
        pombo.setValue("ex2servicepo", newsvcpo, MboConstants.NOACCESSCHECK)