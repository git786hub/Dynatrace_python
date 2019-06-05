# AUTOSCRIPT NAME: EX2_PO_ONINIT
# CREATEDDATE: 2013-10-03 17:02:56
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-05-14 07:42:58
# CHANGEBY: U3LO
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
from psdi.security import UserInfo
from psdi.server import  MXServer

if interactive :
 if app in ["PO"]:
    # protect ponum so only can autonum
    mbo.setFieldFlag("PONUM", MboConstants.READONLY, True)
    #ITO-24395 to make revision comments and revision long description field editable for buyers and service coordinators when po is in pending revision status # Start
    from psdi.mbo import MboConstants
    
    personid=mbo.getUserInfo().getPersonId()
   
    groupuserset=mbo.getMboSet("$PO2GROUPUSER","GROUPUSER","USERID='"+personid+"' and GROUPNAME in ('BUYER','SERVICECOORD')")
    
    if (mbo.getString("STATUS")=='PNDREV' and not groupuserset.isEmpty()):
      mbo.setFieldFlag("REVCOMMENTS",MboConstants.READONLY,False)
      mbo.setFieldFlag("REVCOMMENTS_LONGDESCRIPTION",MboConstants.READONLY,False)
    groupuserset.reset()  
    #ITO-24395 to make revision comments and revision long description field editable for buyers and service coordinators when po is in pending revision status # end
    # protect po when it is in workflow - BUPEND processes only
    #if mbo.getString("STATUS") == "BUPEND" : 
    #asgnset = mbo.getMboSet("EX2DOAWFASGN")
    #if asgnset.count() > 0 :
        #mbo.setFlag(MboConstants.READONLY, True)   #  set object readonly
        
        
    
    # protect fields in the main tab if contract is approved 
    curstat = mbo.getString("STATUS")
    if curstat == "APPR"  or curstat == "COMPLETE"  or curstat == "REVISD"  or curstat == "SUSPND"  or curstat == "PROCESSED":
        mbo.setFieldFlag("EX2TASKSOW", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2DERNUM", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2REQUESTEDBY", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2REVOWNER", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2REVBUYER", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2DESAPPR", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2PROJECT", MboConstants.READONLY, True)
        mbo.setFieldFlag("EX2FREIGHTTERMS", MboConstants.READONLY, True)
        mbo.setFieldFlag("ex2desbuapprind", MboConstants.READONLY, True)
        mbo.setFieldFlag("ex2servicepo", MboConstants.READONLY, True)
        mbo.setFieldFlag("ex2buapprdoatype", MboConstants.READONLY, True)




    # HIDE fields in the main tab if user is a contractor - i.e. in user group 3PSCM
    if mbo.getMboSet("EX23PSCMUSERGROUP").count() > 0:
        mbo.setFieldFlag("PRETAXTOTAL", MboConstants.HIDDEN, True)
        mbo.setFieldFlag("TOTALTAX1", MboConstants.HIDDEN, True)
        mbo.setFieldFlag("TOTALCOST", MboConstants.HIDDEN, True)
        mbo.setFieldFlag("TOTALBASECOST", MboConstants.HIDDEN, True)

    # protect the DER number in the main tab if PO is created in the PR app 
    source = mbo.getString("ex2posource")
    if source == "PR" :
        mbo.setFieldFlag("EX2DERNUM", MboConstants.READONLY, True)

if not interactive:
	personid=mbo.getUserInfo().getPersonId()
	if personid != 'MAXINTADM':
		# protect fields in the main tab if contract is approved 
		curstat = mbo.getString("STATUS")
		if curstat == "APPR"  or curstat == "PROCESSED":    
			mbo.setFieldFlag("EX2TASKSOW", MboConstants.READONLY, True)
			mbo.setFieldFlag("EX2DERNUM", MboConstants.READONLY, True)
			mbo.setFieldFlag("EX2REQUESTEDBY", MboConstants.READONLY, True)
			mbo.setFieldFlag("EX2REVOWNER", MboConstants.READONLY, True)
			mbo.setFieldFlag("EX2REVBUYER", MboConstants.READONLY, True)
			mbo.setFieldFlag("EX2DESAPPR", MboConstants.READONLY, True)
			mbo.setFieldFlag("EX2PROJECT", MboConstants.READONLY, True)
			mbo.setFieldFlag("EX2FREIGHTTERMS", MboConstants.READONLY, True)
			mbo.setFieldFlag("ex2desbuapprind", MboConstants.READONLY, True)
			mbo.setFieldFlag("ex2servicepo", MboConstants.READONLY, True)
			mbo.setFieldFlag("ex2buapprdoatype", MboConstants.READONLY, True)