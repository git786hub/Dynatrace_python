# AUTOSCRIPT NAME: CG_UPDSEQ
# CREATEDDATE: 2014-10-12 09:32:55
# CREATEDBY: UVX3
# CHANGEDATE: 2018-08-19 19:21:16
# CHANGEBY: U171
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

metersetrec = mbo.getMboSet("ACTIVEASSETMETERNEW")
metrec = metersetrec.getMbo(0)
sequence = metrec.getString("SEQUENCE")

if (sequence is not None and sequence <> '') :
   mbo.setValue("CG_METSEQUENCE",metrec.getString("SEQUENCE"))