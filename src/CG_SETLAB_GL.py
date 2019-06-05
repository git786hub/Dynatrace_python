# AUTOSCRIPT NAME: CG_SETLAB_GL
# CREATEDDATE: 2013-07-25 01:28:46
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-07-25 02:59:20
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
    
personset = mbo.getMboSet("DUMMY_LABPER") 
strcondition = "PERSONID = '" + PERSONID +"'"
personset.setWhere(strcondition)

if (personset.count() > 0) :    
    personset1 = personset.getMbo(0)
    cmpany = personset1.getString("CG_CMPNY") 
    orgcode = personset1.getString("CG_ORGCODE") 

    buid = "ESD"
    if  cmpany == "13" :
        buid = "TRN"

    laborrateset = mbo.getMboSet("LABORCRAFTRATE")
    num = laborrateset.count()

    for i in range (num) :
        laborrate = laborrateset.getMbo(i)
        if orgcode is not None and orgcode <> "" :
            laborrate.setValue("GLACCOUNT",buid + "-" + orgcode +"-???????-101-????????-????-????")
        else :
            laborrate.setValue("GLACCOUNT",buid + "-??????-???????-101-????????-????-????")