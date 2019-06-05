# AUTOSCRIPT NAME: VALIDATEDATERANGE
# CREATEDDATE: 2010-09-03 08:33:59
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2010-09-03 10:25:51
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

# Check that end date comes after start date

from java.text import SimpleDateFormat
fmt = SimpleDateFormat('MM/d/yy')

rc = 1
errmsg = ''
startdatestr = offeringAttributes.getValue("PMSCSTARTDATE");
#startdatestr="12/1/10"

enddatestr = offeringAttributes.getValue("PMSCENDDATE");
#enddatestr = "11/1/10" 

if len(startdatestr) > 0 and len(enddatestr) > 0: 
   startdate = fmt.parse(startdatestr)
   enddate = fmt.parse(enddatestr)
   if enddate.before(startdate):
      rc =0
      errmsg = 'The Start Date must occur before the End Date'

print rc
print errmsg