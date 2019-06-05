# AUTOSCRIPT NAME: EX2POTERMRICHTOPLAIN
# CREATEDDATE: 2015-05-21 05:48:28
# CREATEDBY: UVX3
# CHANGEDATE: 2017-01-29 23:04:06
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.util import HTML
from java.util.regex import Pattern

# for POTERM.DESCRIPTION
potermdesc= mbo.getString("DESCRIPTION")
potermdesc= HTML.toPlainText(potermdesc)
replace = Pattern.compile("[^\\p{ASCII}]");
matcher2 = replace.matcher(potermdesc.strip());
potermdesc=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]");
matcher2 = replace.matcher(potermdesc.strip());
potermdesc=matcher2.replaceAll("")

# for POTERM.DESCRIPTION_LONGDESCRIPTION
ldtext = mbo.getString("DESCRIPTION_LONGDESCRIPTION")
ldtext = HTML.toPlainText(ldtext)
replace = Pattern.compile("[^\\p{ASCII}]");
matcher2 = replace.matcher(ldtext .strip());
ldtext=matcher2.replaceAll("")
replace = Pattern.compile("[&`~!?#?Y???[??<?-?}\\\\??]?{????????>????\\[\\]]");
matcher2 = replace.matcher(ldtext .strip());
ldtext=matcher2.replaceAll("")