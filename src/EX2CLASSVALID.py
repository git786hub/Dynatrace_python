# AUTOSCRIPT NAME: EX2CLASSVALID
# CREATEDDATE: 2018-10-14 04:15:45
# CREATEDBY: U4B0
# CHANGEDATE: 2018-10-30 04:04:27
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e



if mbo.getThisMboSet().getParentApp()=='WOT_TRN' and not mbo.isNull("JPNUM"):
 if mbo.getString("JPNUM") in ['JP00028-013', 'JP00028-014'] and not mbo.isNull("CLASSSTRUCTUREID"):
  classstructureSet= mbo.getMboSet("CLASSSTRUCTURE")
  classstructureMbo=classstructureSet.getMbo(0)
  if classstructureMbo.getString("CLASSIFICATIONID") !='BATTERY_CELLCORDER_VRLA':
   setError("Classification mismatch","Please select BATTERY_CELLCORDER_VRLA as classification")
 elif mbo.getString("JPNUM") in ['JP00028-001'] and not mbo.isNull("CLASSSTRUCTUREID"):
  classstructureSet= mbo.getMboSet("CLASSSTRUCTURE")
  classstructureMbo=classstructureSet.getMbo(0)
  if classstructureMbo.getString("CLASSIFICATIONID") !='BATTERY_CELLCORDER_VLA':
   setError("Classification mismatch","Please select BATTERY_CELLCORDER_VLA as classification")