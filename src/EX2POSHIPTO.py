# AUTOSCRIPT NAME: EX2POSHIPTO
# CREATEDDATE: 2018-04-10 13:33:57
# CREATEDBY: U1MZ
# CHANGEDATE: 2018-04-17 07:27:08
# CHANGEBY: U3LO
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 
from psdi.server import MXServer
maximo=MXServer.getMXServer()
#shipto=mbo.getString("SHIPTO")
siteid=mbo.getString("SITEID")
prpolineset=mbo.getMboSet("EX2PRLINE_NP")
if onadd and mbo.isModified("SHIPTO") and mbo.isNull("SHIPTO") and prpolineset.isEmpty() and interactive :
  if (siteid=='TRN'):
    mbo.setValue("SHIPTO",493,MboConstants.NOACCESSCHECK)
  if (siteid=='DIS'):
    mbo.setValue("SHIPTO",886,MboConstants.NOACCESSCHECK)