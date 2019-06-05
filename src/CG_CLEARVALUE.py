# AUTOSCRIPT NAME: CG_CLEARVALUE
# CREATEDDATE: 2012-07-08 16:54:05
# CREATEDBY: UHD0
# CHANGEDATE: 2012-07-15 14:54:10
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 
dVehhrs = 0

if mbo.getDouble("REGULARHRS") is not None:
    dVehhrs = dVehhrs + mbo.getDouble("REGULARHRS") 

if mbo.getDouble("PREMIUMPAYHOURS") is not None:
    dVehhrs = dVehhrs + mbo.getDouble("PREMIUMPAYHOURS") 

if mbo.getBoolean("CG_PRIVEHICLE") :
    mbo.setValue("CG_PRIVEHICLEHRS",dVehhrs,MboConstants.NOACCESSCHECK)
else :
    mbo.setValueNull("CG_PRIVEHICLEHRS",MboConstants.NOACCESSCHECK)