# AUTOSCRIPT NAME: PMSCPREPOPULATE
# CREATEDDATE: 2012-10-02 08:33:59
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2012-10-02 10:25:51
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

# used as an prepopulate script

rc = 1
errmsg=''
# get the sr
srSet=scriptHome.getMboSet("SR");
sr=srSet.getMbo(0);

# get the complex item set
complexItemSet = sr.getMboSet("PMSCBLDACCESS");

# create 3 rows in complex item and fill the building num with RTP 500
if complexItemSet.count()==0:
   for a in range(3):
      try:
         complexItem =complexItemSet.addAtEnd();
         complexItem.setValue("BUILDINGNUM","RTP 500");
      except:
         rc = 0
         errmsg = 'PrePopulate script failed while adding new record'
print rc
print errmsg