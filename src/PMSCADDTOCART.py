# AUTOSCRIPT NAME: PMSCADDTOCART
# CREATEDDATE: 2012-10-02 08:33:59
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2012-10-02 10:25:51
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

# used as an add to cart script

rc=1
errmsg=''

# get the sr
srSet=scriptHome.getMboSet("SR");
sr=srSet.getMbo(0);

# get the complex item set
complexItemSet = sr.getMboSet("PMSCBLDACCESS");
complexItem =complexItemSet.getMbo(0);
count= complexItemSet.count();

# Initialisation of the Array
complexItemSet1= []
for i in range(count):
   complexItemSet1.append(complexItemSet.getMbo(i));

numItems = len(complexItemSet1)
# verify all the aomplex item rows building num not null
for i in range(numItems):
   complexitem  = complexItemSet1[i]
   if complexitem !=None:
      if len(complexitem.getString("BUILDINGNUM"))  == 0:
         rc=0
         errmsg='Building bumber is null in row ',i+1, ' Please provide valid building number'
         break;
                                                     
print rc
print errmsg