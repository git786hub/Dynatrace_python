# AUTOSCRIPT NAME: EX2DEFBIN
# CREATEDDATE: 2015-07-03 06:52:41
# CREATEDBY: UVX3
# CHANGEDATE: 2015-07-03 06:52:41
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.server import MXServer

tostorelocv = mbo.getString("TOSTORELOC")
tobin = mbo.getString("TOBIN")

if tostorelocv is None or tostorelocv <> "" :
   mbo.setValue("TOBIN", "" ,MboConstants.NOACCESSCHECK)

if tostorelocv is not None and tostorelocv  <> "" :
   invmboset = mbo.getMboSet("TOINVENTORY")
   if (invmboset.count() >0) :
        mbo.setValue("TOBIN", invmboset.getMbo(0).getString("BINNUM"),MboConstants.NOACCESSCHECK)