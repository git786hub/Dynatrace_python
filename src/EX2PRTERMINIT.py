# AUTOSCRIPT NAME: EX2PRTERMINIT
# CREATEDDATE: 2013-11-07 17:11:38
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:04:17
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if interactive :

    # protect terms and conditions from non-buyers

    groupuserset = mbo.getMboSet("EX2BUYERUSERGROUP")
    if groupuserset.count() == 0:
        mbo.setFlag(MboConstants.READONLY, True)   #  set object readonly