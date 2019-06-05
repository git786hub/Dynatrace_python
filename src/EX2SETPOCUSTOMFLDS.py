# AUTOSCRIPT NAME: EX2SETPOCUSTOMFLDS
# CREATEDDATE: 2014-02-21 11:43:10
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-02-18 23:31:40
# CHANGEBY: U047
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from psdi.tloam.app.po import PORemote

# get po line mboset for several of following sections
if onadd or ( mbo.isNull("ex2invappr") or mbo.isNull("ex2freightterms") ) :
    polset = mbo.getMboSet("POLINE")
    num = polset.count()

# set PO header service-PO flag when all the lines are a service type

if onadd :      # must run from header in add situation for when new po created, header is saved after the lines.
    oldsvcpo = mbo.getBoolean("ex2servicepo")   #remember current value, so only set new value if different
    newsvcpo = False
    # loop thru all the current lines
    ###mbo.setValue("description", mbo.getString("description") + " " + launchPoint)
    for i in range(num):
        polmbo = polset.getMbo(i)
        ###mbo.setValue("description", mbo.getString("description") + " " + str(polmbo.getInt("polinenum")) + " " + polmbo.getString("linetype"))
        if (polmbo.getString("linetype") == "SERVICE" or polmbo.getString("linetype") == "STDSERVICE") and not polmbo.toBeDeleted() :
            ###mbo.setValue("description", mbo.getString("description") + " T ")
            newsvcpo = True
        elif not polmbo.toBeDeleted():
            ###mbo.setValue("description", mbo.getString("description") + " F ")
            newsvcpo = False
            break
    if oldsvcpo <> newsvcpo :
        mbo.setValue("ex2servicepo", newsvcpo, MboConstants.NOACCESSCHECK)

# set header invoice approver if it is null, but some line has one
# also reach out to the PR to get freight terms

print "HHHHHHHHHHHHHHHHHHHHHHHHHH "
if mbo.isNull("ex2invappr") or mbo.isNull("ex2freightterms") :
    print "HHHHHHHHHHHHHHHHHHHHHHHHHH null"
    for i in range(polset.count()):
        print "HHHHHHHHHHHHHHHHHHHHHHHHHH line "
        print "HHHHHHHHHHHHHHHHHHHHHHHHHH line " + polmbo.getString("ex2invappr")
        polmbo = polset.getMbo(i)

        if i == 0 and mbo.isNull("ex2freightterms") :
            prlset = polmbo.getMboSet("EX2PRLTOPOL")
            if prlset.count() > 0 :
                prlmbo = prlset.getMbo(0)
                prset = prlmbo.getMboSet("PR")
                if prset.count() > 0 :
                    print "HHHHHHHHHHHHHHHHHHHHHHHHHH got pr "
                    prmbo = prset.getMbo(0)
                    mbo.setValue("ex2freightterms", prmbo.getString("ex2freightterms"))

        if not polmbo.isNull("ex2invappr") :
            print "HHHHHHHHHHHHHHHHHHHHHHHHHH not null "
            mbo.setValue("ex2invappr", polmbo.getString("ex2invappr"))
            break

# lastly, if freight terms not set, but oob field is set, copy it over
# else copy from the contract in next section
if mbo.isNull("ex2freightterms") and not mbo.isNull("freightterms") :
    print "HHHHHHHHHHHHHHHHHHHHHHHHHH got maximo ft "
    mbo.setValue("ex2freightterms", mbo.getString("freightterms"))

# get current blanket release number from the contract

if onadd and mbo.getString("potype") == "REL" and mbo.getDouble("revisionnum") == 0 :
    contset = mbo.getMboSet("PURCHVIEW")
    if contset.count() > 0:
        print "HHHHHHHHHHHHHHHHHHHHHHHHHH got contr "
        contmbo = contset.getMbo(0)
        poset = contmbo.getMboSet("EX2BLKTREL")
        if poset.count() > 0:
            mbo.setValue("ex2porelnum", poset.getMbo(0).getInt("ex2porelnum") + 1)
        else :
            mbo.setValue("ex2porelnum", 1)

        if mbo.isNull("ex2freightterms") and not contmbo.isNull("ex2freightterms") :
            print "HHHHHHHHHHHHHHHHHHHHHHHHHH got contr ft"
            mbo.setValue("ex2freightterms", contmbo.getString("ex2freightterms"))

#INC000001112547copying the Prline EX2Shipto to Poline Shipto Again
if onadd:
     polinelset = mbo.getMboSet("POLINE")
     num1 =  polinelset.count()
     if polinelset.count() > 0:
           for s in range (num1):
	        polinembo = polinelset.getMbo(s)
		prlset1 = polinembo.getMboSet("EX2PRLINE_NP")
		if prlset1.count() > 0 :
			 prlmbo1 = prlset1.getMbo(0)
                         polinembo.setValue("shipto", prlmbo1.getString("ex2shipto"), MboConstants.NOACCESSCHECK)