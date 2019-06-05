# AUTOSCRIPT NAME: INSTALLDB2
# CREATEDDATE: 2009-04-17 11:48:13
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2011-02-02 14:14:14
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

if (newValue == '1'):
   dbdir = offeringAttributes.getValue("DBDIR")
   dbadmin = offeringAttributes.getValue("DBADMIN")
   if len(dbdir) == 0:
      offeringAttributes.setNewValue("DBDIR", "c:/ibm/db2")
   if len(dbadmin) == 0:
      offeringAttributes.setNewValue("DBADMIN", "db2admin")
print 1