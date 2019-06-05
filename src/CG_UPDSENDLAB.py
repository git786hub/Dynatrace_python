# AUTOSCRIPT NAME: CG_UPDSENDLAB
# CREATEDDATE: 2014-01-29 09:31:46
# CREATEDBY: UVX3
# CHANGEDATE: 2014-05-13 06:20:21
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

laborrecset = None

laborrecset = mbo.getMboSet("LABOR")
laborrec = laborrecset.getMbo(0)
sendlaborflag = laborrec.getBoolean("CG_SENDLABOR")
if ( sendlaborflag <> True ) :
    mbo.setValue("CG_PAYSENT",1)

if (laborrecset is not None and not laborrecset.isEmpty()) :   
   laborrecset.close()