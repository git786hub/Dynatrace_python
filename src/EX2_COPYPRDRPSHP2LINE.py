# AUTOSCRIPT NAME: EX2_COPYPRDRPSHP2LINE
# CREATEDDATE: 2013-09-30 17:54:47
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-10-01 07:33:49
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# Populate custom PRLine fields from PR header

from psdi.mbo import MboConstants 

PRLineSet = mbo.getMboSet("PRLINE")
numprl = PRLineSet.count()

for j in range(numprl) :
    prlmbo = PRLineSet.getMbo(j)
    if prlmbo:
        if prlmbo.isNull("EX2DROPSHIP"):
            prlmbo.setValue("EX2DROPSHIP",mbo.getString("EX2DROPSHIP"),MboConstants.NOACCESSCHECK)