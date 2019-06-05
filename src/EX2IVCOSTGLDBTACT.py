# AUTOSCRIPT NAME: EX2IVCOSTGLDBTACT
# CREATEDDATE: 2014-05-02 11:36:46
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:17:09
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

if onadd :
  ivlmbo = mbo.getOwner()
  if  not ivlmbo.isNull("linetype") and not ivlmbo.isNull("itemnum") and not ivlmbo.isNull("ponum") and not ivlmbo.isNull("positeid") :
      if ivlmbo.getString("linetype") == "STDSERVICE" and ivlmbo.getString("itemnum") == "FREIGHT" :
         siteset = ivlmbo.getMboSet("EX2SITE")
         if siteset.count() > 0 :
            sitembo = siteset.getMbo(0)
            mbo.setValue("gldebitacct", sitembo.getString("EX2FREIGHTACCT"),MboConstants.NOACCESSCHECK)