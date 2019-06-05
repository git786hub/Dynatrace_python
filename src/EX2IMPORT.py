# AUTOSCRIPT NAME: EX2IMPORT
# CREATEDDATE: 2016-06-16 04:46:55
# CREATEDBY: UVX3
# CHANGEDATE: 2016-06-16 04:46:55
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: python
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote


mboset = mbo.getThisMboSet()
mboset.save()