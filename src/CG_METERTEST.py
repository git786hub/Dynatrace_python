# AUTOSCRIPT NAME: CG_METERTEST
# CREATEDDATE: 2013-11-01 06:07:20
# CREATEDBY: UFDA
# CHANGEDATE: 2013-11-22 08:37:43
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

if mbo.getString("FL_WHR_REG_AL") is None or mbo.getString("FL_WHR_REG_AL") == ""  :
   mbo.setValue("FL_WHR_REG_AL", mbo.getString("FL_WHR_REG_AF"))

if mbo.getString("LL_WHR_REG_AL") is None or mbo.getString("LL_WHR_REG_AL") == ""  :
   mbo.setValue("LL_WHR_REG_AL", mbo.getString("LL_WHR_REG_AF"))

if mbo.getString("FL_VARH_REG_AL") is None or mbo.getString("FL_VARH_REG_AL") == ""  :
   mbo.setValue("FL_VARH_REG_AL", mbo.getString("FL_VARH_REG_AF"))

if mbo.getString("LL_VARH_REG_AL") is None or mbo.getString("LL_VARH_REG_AL") == ""  :
   mbo.setValue("LL_VARH_REG_AL", mbo.getString("LL_VARH_REG_AF"))

if mbo.getString("PF_REG_AL") is None or mbo.getString("PF_REG_AL") == ""  :
   mbo.setValue("PF_REG_AL", mbo.getString("PF_REG_AF"))

if mbo.getString("DEMAND_REG_AL") is None or mbo.getString("DEMAND_REG_AL") == ""  :
   mbo.setValue("DEMAND_REG_AL", mbo.getString("DEMAND_REG_AF"))

# if mbo.getString("METER_SEAL_AL") is None or mbo.getString("METER_SEAL_AL") == ""  :
  # mbo.setValue("METER_SEAL_AL", mbo.getString("METER_SEAL_AF"))

# if mbo.getString("SOCKET_SEAL_AL") is None or mbo.getString("SOCKET_SEAL_AL") == ""  :
#   mbo.setValue("SOCKET_SEAL_AL", mbo.getString("SOCKET_SEAL_AF"))

if mbo.getString("AL_KWH_RDG") is None or mbo.getString("AL_KWH_RDG") == ""  :
   mbo.setValue("AL_KWH_RDG", mbo.getString("AF_KWH_RDG"))

if mbo.getString("AL_KW_RDG") is None or mbo.getString("AL_KW_RDG") == ""  :
   mbo.setValue("AL_KW_RDG", mbo.getString("AF_KW_RDG"))

if mbo.getString("AL_KVARH_RDG") is None or mbo.getString("AL_KVARH_RDG") == ""  :
   mbo.setValue("AL_KVARH_RDG", mbo.getString("AF_KVARH_RDG"))

if mbo.getString("AL_PF_RDG") is None or mbo.getString("AL_PF_RDG") == ""  :
   mbo.setValue("AL_PF_RDG", mbo.getString("AF_PF_RDG"))

if mbo.getString("AL_RE_WHR_REG") is None or mbo.getString("AL_RE_WHR_REG") == ""  :
   mbo.setValue("AL_RE_WHR_REG", mbo.getString("AF_RE_WHR_REG"))

if mbo.getString("AL_ME_WHR_REG") is None or mbo.getString("AL_ME_WHR_REG") == ""  :
   mbo.setValue("AL_ME_WHR_REG", mbo.getString("AF_ME_WHR_REG"))

if mbo.getString("AL_LE_WHR_REG") is None or mbo.getString("AL_LE_WHR_REG") == ""  :
   mbo.setValue("AL_LE_WHR_REG", mbo.getString("AF_LE_WHR_REG"))