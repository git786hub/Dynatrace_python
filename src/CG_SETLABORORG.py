# AUTOSCRIPT NAME: CG_SETLABORORG
# CREATEDDATE: 2012-07-09 05:03:04
# CREATEDBY: UHD0
# CHANGEDATE: 2016-01-28 01:23:48
# CHANGEBY: U153
# SCRIPTLANGUAGE: jython
# STATUS: Draft

laborset = mbo.getMboSet("LABOR")
if 0 < laborset.count() :
    labor = laborset.getMbo(0)
    labor.setValueNull("CG_APPROVER")

buid = "ESD"
if  personsite == "TRN" :
    buid = "TRN"

laborrateset = mbo.getMboSet("CG_LABORCRAFTRATE")
num = laborrateset.count()

for i in range (num) :
    laborrate = laborrateset.getMbo(i)
    if orgcode is not None and orgcode <> "" :
        laborrate.setValue("GLACCOUNT",buid + "-" + orgcode +"-???????-101-????????-????-????")
    else :
        laborrate.setValue("GLACCOUNT",buid + "-??????-???????-101-????????-????-????")