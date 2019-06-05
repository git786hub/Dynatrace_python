# AUTOSCRIPT NAME: EX2POLNGDESC
# CREATEDDATE: 2015-05-21 05:22:58
# CREATEDBY: UVX3
# CHANGEDATE: 2017-01-29 23:03:58
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.util import HTML
from java.util.regex import Pattern

# for PO.DESCRIPTION
podesc= mbo.getString("DESCRIPTION")
podesc= HTML.toPlainText(podesc)
replace = Pattern.compile("[^\\p{ASCII}]")
matcher2 = replace.matcher(podesc.strip());
podesc=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]")
matcher2 = replace.matcher(podesc.strip());
podesc=matcher2.replaceAll("")

# for PO.DESCRIPTION_LONGDESCRIPTION
ldtext = mbo.getString("DESCRIPTION_LONGDESCRIPTION")
ldtext = HTML.toPlainText(ldtext)
replace = Pattern.compile("[^\\p{ASCII}]")
matcher2 = replace.matcher(ldtext .strip());
ldtext=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]")
matcher2 = replace.matcher(ldtext .strip());
ldtext=matcher2.replaceAll("")

# for REVCOMMENTS_LONGDESCRIPTION
ldrevtext= mbo.getString("REVCOMMENTS_LONGDESCRIPTION")
ldrevtext= HTML.toPlainText(ldrevtext)
replace = Pattern.compile("[^\\p{ASCII}]")
matcher2 = replace.matcher(ldrevtext.strip());
ldrevtext=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]")
matcher2 = replace.matcher(ldrevtext.strip());
ldrevtext=matcher2.replaceAll("")