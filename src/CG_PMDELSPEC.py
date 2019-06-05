# AUTOSCRIPT NAME: CG_PMDELSPEC
# CREATEDDATE: 2012-05-01 20:43:18
# CREATEDBY: UHD0
# CHANGEDATE: 2012-05-01 21:01:38
# CHANGEBY: TRNADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

pmbuildspecset = mbo.getMboSet("CG_PMBUILDSPEC")
num = pmbuildspecset.count()

for i in range(num) :
    pmbuildspec = pmbuildspecset.getMbo(i)
    pmbuildspec.delete()