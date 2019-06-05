# AUTOSCRIPT NAME: CG_LIMSREP
# CREATEDDATE: 2013-09-24 07:10:45
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-07-29 05:21:45
# CHANGEBY: U14Q
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.lang import String
from java.rmi import RemoteException
from java.text import SimpleDateFormat
from javax.mail import MessagingException
from com.ibm.tivoli.maximo.report.birt.admin import ReportAdminServiceRemote
from com.ibm.tivoli.maximo.report.birt.runtime import ReportParameterData
from psdi.mbo import MboRemote
from psdi.security import UserInfo
from psdi.server import MXServer
from java.io import File
from java.util import Date
from java.io import FileOutputStream
from psdi.util import MXException
from java.util import Calendar
from java.util import Date
from psdi.app.report import ReportUtil
from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.mbo import SqlFormat

print "******************** LIMS REPORT ********************"

reportname = "cg_lims.rptdesign"
emailfrom = "maxadmin@oncor.com"

emaillist = ""
emailmboset = mbo.getMboSet("CG_EMAILNOTIFY")
cnt = emailmboset.count()
for x in range(cnt):
    emailmbo = emailmboset.getMbo(x)
    emaillist= emailmbo.getString("EMAIL_CONTACT")

emailbody = "Email from OILNOTIFICATION Escalation, please find attached Notification Report"

#emailto  = []

#for lst in emaillist.split(','):
#    emailto.append(lst)


#emailto.append("Mark.Ashford@oncor.com")
#emailto.append("James.Babcock@oncor.com")
#emailto.append("Mike.Hamilton@oncor.com")
#emailto.append("Edgar.Judd@oncor.com")
#emailto.append("John.Dukes@oncor.com")
#emailto.append("Phillip.Pruente@oncor.com")
#emailto.append("IBM_Oncor_Maximo_Support@oncor.com")

TEXTPARAM1 = mbo.getString("METERNAME")
TEXTPARAM2 = mbo.getString("ASSETNUM")
TEXTPARAM3 = mbo.getString("COMPARTMENT")
TEXTPARAM4 = mbo.getString("SOURCE")
TEXTPARAM5 = mbo.getString("LABID")
TEXTPARAM6 = mbo.getString("CONDITION")
OBSV = mbo.getString("OBSERVATION")

emailsubject = ''

tmpid = ""
rpthdr = ""
submetconmboset = mbo.getMboSet("CG_NOTIFYSUBJECT")
cnt = submetconmboset.count()
for x in range(cnt):
    submetconmbo = submetconmboset.getMbo(x)
    tmpid = submetconmbo.getString("TEMPID")
    rpthdr = submetconmbo.getString("RPTHEADING")

trf = ""
subtrfmboset = mbo.getMboSet("CG_NOTIFYLOCATION")
cnt = subtrfmboset.count()
for x in range(cnt):
    subtrfmbo = subtrfmboset.getMbo(x)
    trf= subtrfmbo.getString("CG_LOCLEGACYID")
                

stnname = ""
substnnmmboset = mbo.getMboSet("CG_NOTIFYLOCATIONSPEC")
cnt = substnnmmboset.count()
for x in range(cnt):
    substnnmmbo = substnnmmboset.getMbo(x)
    stnname= substnnmmbo.getString("ALNVALUE")

anadt = ""   
subanadtmboset = mbo.getMboSet("CG_OILNOTIFICATION")
cnt = subanadtmboset.count()
for x in range(cnt):
    subanadtmbo = subanadtmboset.getMbo(x)
    anadt= subanadtmbo.getString("ANALYSISDATE")
                
snum = ""   
subsnummboset = mbo.getMboSet("CG_NOTIFYSNUM")
cnt = subsnummboset.count()
for x in range(cnt):
    subsnummbo = subsnummboset.getMbo(x)
    snum= subsnummbo.getString("SERIALNUM")

emailsubject = " "+tmpid+" - "+stnname+" - "+anadt+" - "+trf+" - "+TEXTPARAM3+" - "+snum+" - "+rpthdr+" - "+TEXTPARAM4 


#para = ReportParameterData()
#para.addParameter("metername",TEXTPARAM1)
#para.addParameter("assetnum",TEXTPARAM2)
#para.addParameter("compartment",TEXTPARAM3)
#para.addParameter("source",TEXTPARAM4)
#para.addParameter("labid",TEXTPARAM5)
#para.addParameter("condition",TEXTPARAM6)

#filename = emailsubject+".pdf"
#print filename

#ui = mbo.getUserInfo()

#print " ready to run REPORT ********************"
#reportservice = MXServer.getMXServer().lookup("BIRTREPORT")
#reportOutput = reportservice.runReport(ui, reportname, "ASSETS_TRN", para, emailsubject, "pdf")
                                                                
#s = String(reportOutput)

#MXServer.sendEMail(emailto, emailfrom, emailsubject, emailbody, s, filename)

print "===================Start of the schedule report code for INC000001338853================================"

v_reportname=reportname
v_appname="ASSETS_TRN"
v_emailtype="attach"
v_maximourl=""
v_emailto=emaillist
v_emailsubject=emailsubject
v_emailcomments=emailbody
v_emailfiletype="PDF"
v_paramstring=""
v_paramdelimiter=""

#               set a schedule for the report
c = Calendar.getInstance()
#               add 300 seconds to current time to allow preparing REPORTSCHED cron task instance
c.add(Calendar.SECOND,300)
d = c.getTime()
thisassetset = mbo.getThisMboSet()
if thisassetset is not None:
         locale = thisassetset.getClientLocale()
         userinfo = thisassetset.getUserInfo()
schedule = ReportUtil.convertOnceToSchedule(d,locale,c.getTimeZone())
print "Schedule we have to set into REPORTSCHED Cron task is: " + str(schedule)
if schedule is not None:
                        reportschedset = MXServer.getMXServer().getMboSet("REPORTSCHED",userinfo)
                        if reportschedset is not None:
                                 print "Obtained REPORTSCHED set"
                                 reportsched = reportschedset.add()
                                 reportsched.setValue("REPORTNAME",v_reportname)
                                 reportsched.setValue ("appname",v_appname)
                                 reportsched.setValue ("USERID",userinfo.getUserName())
                                 reportsched.setValue ("TYPE","once")
                                 reportsched.setValue("EMAILTYPE",v_emailtype)
                                 reportsched.setValue("MAXIMOURL",v_maximourl)
                                 reportsched.setValue("EMAILUSERS",v_emailto)
                                 reportsched.setValue("EMAILSUBJECT",v_emailsubject)
                                 reportsched.setValue("EMAILCOMMENTS",v_emailcomments)
                                 reportsched.setValue("EMAILFILETYPE",v_emailfiletype)
                                 reportsched.setValue("COUNTRY",locale.getCountry())
                                 reportsched.setValue("LANGUAGE",locale.getLanguage())
                                 reportsched.setValue("VARIANT",locale.getVariant())
                                 reportsched.setValue("TIMEZONE",thisassetset.getClientTimeZone().getID())
                                 reportsched.setValue("LANGCODE",userinfo.getLangCode())
                                 print "About to work with REPORTSCHEDULE cron task"
                                 crontaskdef = reportsched.getMboSet("$parent","crontaskdef","crontaskname='REPORTSCHEDULE'").getMbo(0)
                                 if crontaskdef is not None:
                                           crontaskinstset = crontaskdef.getMboSet("CRONTASKINSTANCE")
                                           if crontaskinstset is not None:
                                                       print "About to work with Cron task instance of REPORTSCHEDULE cron task"
                                                       crontaskinst = crontaskinstset.add(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                       if crontaskinst is not None:
                                                                   d = Date()
                                                                   crontaskinstname = str(d.getTime())
                                                                   crontaskinst.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                   crontaskinst.setValue("INSTANCENAME",crontaskinstname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                   crontaskinst.setValue("SCHEDULE",schedule,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                   crontaskinst.setValue("ACTIVE",1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                   crontaskinst.setValue("RUNASUSERID",userinfo.getUserName(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                   crontaskinst.setValue("HASLD",0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                   crontaskinst.setValue("AUTOREMOVAL",True,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                   print "have set all cron task instance values for REPORTSCHEDULE cron task"
                                 reportsched.setValue("CRONTASKNAME",crontaskinst.getString("CRONTASKNAME"))
                                 reportsched.setValue("INSTANCENAME",crontaskinst.getString("INSTANCENAME"))
                                 print "Now going to work with Cron task PARAMETERS"
                                 cronparamset = crontaskinst.getMboSet("PARAMETER")
                                 if cronparamset is not None:
                                              sqf = SqlFormat(cronparamset.getUserInfo(),"reportname=:1")
                                              sqf.setObject(1,"REPORTPARAM","REPORTNAME",v_reportname)
                                              reportparamset = MXServer.getMXServer().getMboSet("REPORTPARAM",cronparamset.getUserInfo())
                                              if reportparamset is not None:
                                                            print "working with REPORTPARAM mbo set"
                                                            reportparamset.setWhere(sqf.format())
                                                            reportparamset.reset()
                                 i=reportparamset.count()
                                 reportparammbo = None
                                 for j in range(i):
                                                                          reportparam = reportparamset.getMbo(j)
                                                                          cronparam = cronparamset.add(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                          if cronparam is not None:
                                                                                             print "going to copy values from REPORTPARAM into CRONTASKPARAM"
                                                                                             cronparam.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             cronparam.setValue("INSTANCENAME",crontaskinstname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             cronparam.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             paramname = reportparam.getString("PARAMNAME")
                                                                                             cronparam.setValue("PARAMETER",paramname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             if paramname=="where":
#                                                                                                          prepare dynamic where clause for report params
                                                                                                            uniqueidname = mbo.getUniqueIDName()
                                                                                                            uniqueidvalue = mbo.getUniqueIDValue()
                                                                                                            uniquewhere = uniqueidname + "=" + str(uniqueidvalue)
                                                                                                            cronparam.setValue("VALUE",uniquewhere,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             elif paramname=="paramstring":
                                                                                                            print 'If condition for v_paramstring'
                                                                                                            cronparam.setValue("VALUE",v_paramstring,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             elif paramname=="paramdelimiter":
                                                                                                            print 'If condition for v_paramdelimiter'
                                                                                                            cronparam.setValue("VALUE",v_paramdelimiter,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             elif paramname=="appname":
                                                                                                            cronparam.setValue("VALUE",v_appname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             elif paramname=="metername":
                                                                                                            cronparam.setValue("VALUE",TEXTPARAM1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
											     elif paramname=="assetnum":
                                                                                                            cronparam.setValue("VALUE",TEXTPARAM2,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
											     elif paramname=="compartment":
                                                                                                            cronparam.setValue("VALUE",TEXTPARAM3,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
											     elif paramname=="source":
                                                                                                            cronparam.setValue("VALUE",TEXTPARAM4,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
											     elif paramname=="labid":
                                                                                                            cronparam.setValue("VALUE",TEXTPARAM5,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
											     elif paramname=="condition":
                                                                                                            cronparam.setValue("VALUE",TEXTPARAM6,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
                                                                                             
                                                                                             else:
                                                                                                            continue
                        reportschedset.save()