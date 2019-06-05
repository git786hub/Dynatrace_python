# AUTOSCRIPT NAME: EX2TRLZERO
# CREATEDDATE: 2018-06-12 05:34:09
# CREATEDBY: U1MZ
# CHANGEDATE: 2018-06-26 04:52:29
# CHANGEBY: U1LI
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.asset import AssetRemote
from psdi.mbo import MboConstants


description = mbo.getString("DESCRIPTION")
description = description.replace(".0000000000",".0")
description = description.replace(".000000000",".0")
description = description.replace(".00000000",".0")
description = description.replace(".0000000",".0")
description = description.replace("000000000 ","0 ")
description = description.replace("000000000, ","0,")
description = description.replace("00000000 ","0 ")
description = description.replace("00000000, ","0,")
description = description.replace("0000000 ","0 ")
description = description.replace("0000000, ","0,")
description = description.replace("000000 ","0 ")
description = description.replace("000000,","0,")
description = description.replace("00000 ","0 ")
description = description.replace("00000,","0,")
mbo.setValue("DESCRIPTION",description, MboConstants.NOVALIDATION)