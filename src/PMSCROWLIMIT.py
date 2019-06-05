# AUTOSCRIPT NAME: PMSCROWLIMIT
# CREATEDDATE: 2012-10-02 08:33:59
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2012-10-02 10:25:51
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

# used as row limitation in add to cart script

rc=1
errmsg=''

# get the sr
srSet=scriptHome.getMboSet("SR");
sr=srSet.getMbo(0);

customMbosSet = offering.getMboSet("PMSCCUSTOMMBOS");
customMbo = customMbosSet.getMbo(0);
minimum = customMbo.getInt("MIN");
maximum = customMbo.getInt("MAX");

# get the complex item set
complexItemSet = sr.getMboSet("PMSCBLDACCESS");
complexItem =complexItemSet.getMbo(0);
count= complexItemSet.count();
rows=0 
for a in range(count):
   if not complexItemSet.getMbo(a).toBeDeleted():
      rows=rows+1
if(minimum!=None):
   if rows < minimum:
      rc=0
      errmsg='Minimum number of records should be  ',minimum
if(maximum!=None):
   if rows > maximum:
      rc=0
      errmsg='Maximum number of records should be :',maximum
                                         
print rc
print errmsg