# AUTOSCRIPT NAME: CG_LABRATEOBJ
# CREATEDDATE: 2012-07-09 06:18:20
# CREATEDBY: UHD0
# CHANGEDATE: 2016-01-28 01:43:52
# CHANGEBY: U153
# SCRIPTLANGUAGE: jython
# STATUS: Draft

buid = "ESD"

if personsite == "TRN" :
    print '@@@@@@personsite is TRN'
    print 'personsite'
    buid = "TRN"

# update the glaccount only if its not already set.
if ((mbo.getString("GLACCOUNT") == "?????-??????-???????-101-????????-????-????") or (mbo.getString("GLACCOUNT") == "?????-??????-???????-000-????????-????-????") ):       
    if orgcode is not None and orgcode <> "" :
            mbo.setValue("GLACCOUNT", buid + "-" + orgcode +"-???????-101-????????-????-????")
    else :
        mbo.setValue("GLACCOUNT", buid + "-??????-???????-101-????????-????-????")