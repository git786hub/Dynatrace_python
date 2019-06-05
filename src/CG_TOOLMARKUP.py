# AUTOSCRIPT NAME: CG_TOOLMARKUP
# CREATEDDATE: 2012-09-12 10:38:39
# CREATEDBY: UHD0
# CHANGEDATE: 2014-05-13 06:25:41
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.workorder import WORemote
from psdi.mbo import MboConstants

toolmarkupset = None

ownermbo = mbo.getOwner()

if lineprice <> None and lineprice <> 0 and ownermbo <> None and isinstance(ownermbo ,WORemote):
    toolmarkupset = ownermbo.getMboSet("PLUSPPRICESCHED.CG_TOOLRANGEMARKUP") 
    tmnum = toolmarkupset.count()
    tempmarkup = 0
    for i in range(tmnum):
        toolmarkup = toolmarkupset.getMbo(i)
        if toolmarkup :
            maxmarkup = toolmarkup.getDouble("TOPRICE")             
            minmarkup = toolmarkup.getDouble("FROMPRICE")
            markupvalue = toolmarkup.getDouble("CALC")
        
            if lineprice > maxmarkup :
                tempmarkup = tempmarkup + (( maxmarkup - minmarkup ) * markupvalue / 100 )

            if lineprice > minmarkup  and lineprice < maxmarkup :
                tempmarkup = tempmarkup + (( lineprice - minmarkup ) * markupvalue / 100 )

    lineprice = lineprice + tempmarkup

if (toolmarkupset is not None and not toolmarkupset.isEmpty()) :   
   toolmarkupset.close()