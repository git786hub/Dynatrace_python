# AUTOSCRIPT NAME: CG_CHK_FLCD
# CREATEDDATE: 2013-08-21 02:54:36
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-01-25 04:35:02
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

def setError(g, k):
    global errorkey, errorgroup, params
    errorgroup = g
    errorkey = k

astladmboset = None
failreppresent = None	
dumfaillist = None

savstatus = mbo.getString("STATUS")
wotyp = mbo.getString("CG_WORKTYPE")
subworktype = mbo.getString("CG_SUBWORKTYPE")

if savstatus == 'COMP' :
        if (wotyp == 'CORRECTIVE' and  (subworktype <> 'NOFAILRPT' and subworktype <> 'RSR'   and subworktype <> 'SPR' and subworktype <> 'SA' and subworktype <> 'CAP' ) ):
		
            astladmboset = mbo.getMboSet("WOFAILLIST")
            #astladmboset.setFlag(MboConstants.DISCARDABLE, true)
    	    if (astladmboset.count() > 0) :
		failreppresent = mbo.getMboSet("FAILUREREPORT")
		#failreppresent.setFlag(MboConstants.DISCARDABLE, true)

		if (failreppresent.count() == 0) :
			setError("FAILURECODE", " Please Enter Problem,Cause and Remedy as applicable for Selected Failurecode")
                else :

                        if (failreppresent.count() == 1) :
                                CODE = 'PROBLEM'
                                
                        if (failreppresent.count() == 2) :
                                CODE = 'CAUSE'
                                                
                        if (failreppresent.count() <> 3) :       # If no of records in failurereport is 3, all level of failure hierarchy has been entered 
                                                               
                                lastrecbef2 = failreppresent.getMbo(0)        
                                type1 = lastrecbef2.getString("TYPE")
                                if (type1 == CODE) :                               # identify which record to point at within failurereport
                                    recno = 0
                                else :
                                    recno = 1
                                lastrecbef2 = failreppresent.getMbo(recno)
                                lineno = lastrecbef2.getString("LINENUM")

                                lineno = lineno.replace(',', '')                 # remove commas in fetched data
                                whereclause = "parent = '" + lineno +"'"
                                dumfaillist = mbo.getMboSet("CG_WO_FALLIST_DUMMY")     #dummy relationship fetches all the failurelist table
                                #dumfaillist.setFlag(MboConstants.DISCARDABLE, true)
                                dumfaillist.setWhere(whereclause)    # where clause to further filter data to fetch if lineno is any records parent
                              
                                if ( dumfaillist.count() <> 0 ) :
                                        setError("FAILURECODE", " Please enter all levels of failure codes")

	

if (astladmboset is not None and not astladmboset.isEmpty()) :
   astladmboset.close()
   
if (failreppresent is not None and not failreppresent.isEmpty()) :
   failreppresent.close()

if (dumfaillist is not None and not dumfaillist.isEmpty()) :
   dumfaillist.close()