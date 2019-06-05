# AUTOSCRIPT NAME: EX2POLINEDESC
# CREATEDDATE: 2015-05-21 05:32:24
# CREATEDBY: UVX3
# CHANGEDATE: 2017-01-29 23:04:21
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.util import HTML
from java.util.regex import Pattern

# for POLINE.DESCRIPTION
polinedesc= mbo.getString("DESCRIPTION")
polinedesc= HTML.toPlainText(polinedesc)
replace = Pattern.compile("[^\\p{ASCII}]");
matcher2 = replace.matcher(polinedesc.strip());
polinedesc=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]");
matcher2 = replace.matcher(polinedesc.strip());
polinedesc=matcher2.replaceAll("")

# for POLINE.DESCRIPTION_LONGDESCRIPTION
ldtext = mbo.getString("DESCRIPTION_LONGDESCRIPTION")
ldtext = HTML.toPlainText(ldtext)
replace = Pattern.compile("[^\\p{ASCII}]");
matcher2 = replace.matcher(ldtext .strip());
ldtext=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]");
matcher2 = replace.matcher(ldtext .strip());
ldtext=matcher2.replaceAll("")


# for EX2EXTREMARKS_LONGDESCRIPTION
ldrevtext= mbo.getString("EX2EXTREMARKS_LONGDESCRIPTION")
ldrevtext= HTML.toPlainText(ldrevtext)
replace = Pattern.compile("[^\\p{ASCII}]");
matcher2 = replace.matcher(ldrevtext.strip());
ldrevtext=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]");
matcher2 = replace.matcher(ldrevtext.strip());
ldrevtext=matcher2.replaceAll("")