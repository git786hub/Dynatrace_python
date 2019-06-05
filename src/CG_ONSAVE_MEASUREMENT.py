# AUTOSCRIPT NAME: CG_ONSAVE_MEASUREMENT
# CREATEDDATE: 2012-04-23 22:42:07
# CREATEDBY: UHD0
# CHANGEDATE: 2017-01-18 07:34:58
# CHANGEBY: U1LJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.app.asset import AssetMeterRemote
from java.lang import String
from java.lang.Math import pow

def getGRValue ( newValue, oldValue, ndays) :
    grValue = None
    if newValue is not None and newValue > 0 and oldValue is not None and oldValue > 0 :
        grValue = ( ( newValue - oldValue ) * ( 100 / oldValue ) ) / ndays
    return grValue 

def getObs(ownertable,notifymeasureid,nsource) :
    mbo.setValue("OBSERVATION",meterconmbo.getString("OBSERVATION"))
    mbo.setValue("CONDITION",meterconmbo.getString("CONDITION"))
    if isinstance(ownermbo,AssetMeterRemote):
        #ownermbo.setValue("NEWREADING",meterconmbo.getString("OBSERVATION"))
        print 'NEWREADING'
    else :
        ownermbo.setValue("OBSERVATION",meterconmbo.getString("OBSERVATION"))
#                break
    oilnotifyset = mbo.getMboSet("CG_OILNOTIFICATION")
#    if mbo.getString("OWNERTABLE") == "MEASUREMENT" :
    oilnotify = oilnotifyset.add()
    print 'oilnotify'
    ncomp = mbo.getString("COMPARTMENT")
    
    if (ncomp == "SELECTOR" or ncomp == "V-LTC") :
        oilnotify.setValue("METERNAME","DGALTC2")
    if (ncomp == "TRANSFER" or ncomp == "LTC" or ncomp == "REG") :
        oilnotify.setValue("METERNAME","DGALTC")
    if (ncomp == "MAIN") :
        oilnotify.setValue("METERNAME","DGAMAIN")

    oilnotify.setValue("ASSETNUM",mbo.getString("ASSETNUM"))
    oilnotify.setValue("LABID", notifymeasureid )
    oilnotify.setValue("SOURCE", nsource)
    oilnotify.setValue("SITEID",mbo.getString("RECORDSITEID"))
    oilnotify.setValue("COMPARTMENT",ncomp)
    oilnotify.setValue("OBSERVATION",meterconmbo.getString("OBSERVATION"))
    oilnotify.setValue("CONDITION",meterconmbo.getString("CONDITION"))
    oilnotify.setValue("DISP_CONDITION",meterconmbo.getString("DISP_CONDITION"))

source = mbo.getString("SOURCE")
if  source is None or source == "" :
    mbo.setValue("SOURCE","MANUAL")

ownertable = mbo.getString("OWNERTABLE")
ownmbo = mbo.getOwner()
mbo.setValue("ASSETNUM",ownmbo.getString("ASSETNUM"))
mbo.setValue("METERNAME",ownmbo.getString("METERNAME"))
mbo.setValueNull("LASTLABID") 
notifymeasureid = mbo.getString("LABID")
measureid = mbo.getString("RECORDID")
nsource = mbo.getString("SOURCE")
OLDC2H2 = ""
watersat_var = ""
oiltemp_var = ""
watervar = ""

print 'measureid'
print measureid
print 'nsource'
print nsource

if nsource == "MANUAL" :
    mbo.setValue("COMBUSTIBLEGAS",mbo.getDouble("H2")+mbo.getDouble("CH4")+mbo.getDouble("C2H2")+mbo.getDouble("C2H4")+mbo.getDouble("C2H6")+mbo.getDouble("CO") )
    mbo.setValue("TOTALGAS",mbo.getDouble("H2")+mbo.getDouble("CH4")+mbo.getDouble("C2H2")+mbo.getDouble("C2H4")+mbo.getDouble("C2H6")+mbo.getDouble("CO")+mbo.getDouble("CO2")+mbo.getDouble("N2")+mbo.getDouble("O2") )
    if (((mbo.getDouble("OILTEMP") is not None) or (mbo.getDouble("OILTEMP") <> "")) and ((mbo.getDouble("WATER") is not None) or (mbo.getDouble("WATER")<> ""))) :
        if ( (mbo.getDouble("OILTEMP") > 0) and (mbo.getDouble("WATER") > 0)) :
            mbo.setValue("WATERSAT",((mbo.getDouble("WATER")*100)/pow(10,((-1567/(mbo.getDouble("OILTEMP")+273)+7.0895)))))
    combgas = ((mbo.getDouble("H2")/0.059)+(mbo.getDouble("CH4")/0.34)+(mbo.getDouble("CO")/0.09)+(mbo.getDouble("C2H6")/1.65)+(mbo.getDouble("C2H4")/1.18)+(mbo.getDouble("C2H2")/0.958))
    denominator = (combgas + (mbo.getDouble("O2")/0.188)+ (mbo.getDouble("N2")/0.107)+(mbo.getDouble("CO2")/0.798))
    if denominator > 0 :
        mbo.setValue("TCG",((combgas/denominator)*100))


if source <> "ONLINE" :  
    mbo.setValueNull("GR_H2")
    mbo.setValueNull("GR_CH4")
    mbo.setValueNull("GR_C2H6")
    mbo.setValueNull("GR_C2H4")
    mbo.setValueNull("GR_C2H2")
    mbo.setValueNull("GR_CO")
    mbo.setValueNull("GR_COMBUSTIBLEGAS")

labidmboset = mbo.getMboSet("CG_LABID")
lbcnt = labidmboset.count()
if lbcnt == 0:
    lastladmboset = mbo.getMboSet("CG_LASTLABREC")
    cnt = lastladmboset.count()

    for x in range(cnt):
        lastlabmbo = lastladmboset.getMbo(x)
        mbo.setValue("LASTLABID",lastlabmbo.getString("LABID"))
else:
    for y in range(lbcnt):
        labmbo = labidmboset.getMbo(y)
        mbo.setValue("LASTLABID",labmbo .getString("LASTLABID"))


previouslabresultmboset = mbo.getMboSet("CG_LASTOILANALYSISDATA")
num = previouslabresultmboset.count()

previousc2h2mboset = mbo.getMboSet("CG_LASTC2H2")
print 'Fetching OLDC2H2....'
cnum = previousc2h2mboset.count()
print 'cnum'
print cnum
for i in range(cnum):
    previousc2h2mbo = previousc2h2mboset.getMbo(i)
    print '!!!!!!BEFORE OLDC2H2 !!!!!!!!!!!!'
    OLDC2H2 = previousc2h2mbo.getString("C2H2")
    print '@@@@OLDCH2@@@'
    print OLDC2H2

if source <> "ONLINE" :   
    for i in range(num):
        previouslabresultmbo = previouslabresultmboset.getMbo(i)
        if mbo.getDate("SAMPLEDATE") is not None and  previouslabresultmbo.getDate("SAMPLEDATE") is not None and   previouslabresultmbo.getDate("SAMPLEDATE") < mbo.getDate("SAMPLEDATE")  :
            ndays = mbo.getDate("SAMPLEDATE").getTime() -  previouslabresultmbo.getDate("SAMPLEDATE").getTime()
            diffdays = (ndays.longValue() + ( 60*60* 1000 ) )/( 24 * 60 * 60 * 1000)

            mbo.setValue("GR_H2",getGRValue(mbo.getDouble("H2"),previouslabresultmbo.getDouble("H2"),diffdays.longValue()))
            mbo.setValue("GR_CH4",getGRValue(mbo.getFloat("CH4"),previouslabresultmbo.getFloat("CH4"),diffdays.longValue()))
            mbo.setValue("GR_C2H6",getGRValue(mbo.getFloat("C2H6"),previouslabresultmbo.getFloat("C2H6"),diffdays.longValue()))
            mbo.setValue("GR_C2H4",getGRValue(mbo.getFloat("C2H4"),previouslabresultmbo.getFloat("C2H4"),diffdays.longValue()))
            mbo.setValue("GR_C2H2",getGRValue(mbo.getFloat("C2H2"),previouslabresultmbo.getFloat("C2H2"),diffdays.longValue()))
            mbo.setValue("GR_CO",getGRValue(mbo.getFloat("CO"),previouslabresultmbo.getFloat("CO"),diffdays.longValue()))
            mbo.setValue("GR_COMBUSTIBLEGAS",getGRValue(mbo.getFloat("COMBUSTIBLEGAS"),previouslabresultmbo.getFloat("COMBUSTIBLEGAS"),diffdays.longValue()))


notifydelmboset = mbo.getMboSet ("CG_DELOILNOTIFY")
num = notifydelmboset.count()

for i in range(num) :
    notifydelmbo = notifydelmboset.getMbo(i)
    notifydelmbo.delete()


strsql = ""
ownermbo = mbo.getOwner()
meterconsmboset = ownermbo.getMboSet("CG_NOTIFYASCONS")
numl = meterconsmboset.count()

maxattroildatamboset = mbo.getMboSet("MAXATTRIBUTE")
ncol = maxattroildatamboset.count()

try :
    ck = mbo.getUserInfo().getConnectionKey()
    conn = mbo.getMboServer().getDBConnection(ck)
    stmt = conn.createStatement()

    for j in range(numl):
        print '###j###'
        print j
        meterconmbo = meterconsmboset.getMbo(j)

        if meterconmbo :
            strcondition = meterconmbo.getString("CONDITION")
            strcondition = strcondition.replace(":","")
            strcondition = strcondition.upper()
            if OLDC2H2 is None or OLDC2H2 == "" :
                strcondition = strcondition.replace ("OLDC2H2", "NULL")
            else :
                strcondition = strcondition.replace("OLDC2H2",OLDC2H2)
                print '--------------------------------!!!!!strcondition after OLDC2H2!!!!--------------------------------'
                print strcondition

            for k in range(ncol):
                
                maxattrmbo = maxattroildatamboset.getMbo(k)

                if maxattrmbo :
                    strcolname = maxattrmbo.getString("ATTRIBUTENAME")
                    strcolname = strcolname.upper()
                    strcolvalue = mbo.getString(strcolname)
                    if  strcolvalue is None or strcolvalue == "" :
                        strcondition = strcondition.replace(strcolname, "NULL")
                        print '------------------------strcondition in IF-------------------------------------'
                        print strcondition
                    else:
                        strcondition = strcondition.replace(strcolname, mbo.getString(strcolname))
                        strcondition = strcondition.replace(',', '')
                        print '----------------------------strcondition---------------------------------------------'
                        print strcondition

        rs = stmt.executeQuery("select 1 from dual where " + strcondition )
        print '-------------------------------------------Result set---------------------------------------------'
        print rs
        if rs.next():
            observation = meterconmbo.getString("OBSERVATION")
            metername = meterconmbo.getString("METERNAME")
	    vclass = meterconmbo.getString("VOLTAGECLASS")

	    print vclass
				#or (metername =="DGALTC") or (metername == "DGALTC2")
				#Removing FREE BREATHER check for DGALTC and DGALTC2
	    assetspecset = meterconmbo.getMboSet("CG_ASSPEC") 
	    count = assetspecset.count() 
            for c in range(count) : 
                assetspec = assetspecset.getMbo(c) 
		alnval = assetspec.getString("ALNVALUE") 
                if (((observation == "DIELECTRIC_TRK" and vclass=="") or (observation ==  "MOISTURE_TRK") or (observation == "CAUTION_O2")) and (metername =="DGAMAIN") ):
					print '@@@@@ If loop test'
					if (alnval <> "FREE BREATHER") :
						print 'Checking Free Breather------------------------------------------------------------------------------------------------------------'
						if observation == "MOISTURE_TRK" and metername == "DGAMAIN"  and vclass<>"":
							oiltemp_var=mbo.getInt("OILTEMP")
							watersat_var=mbo.getInt("WATERSAT")
							watervar=mbo.getInt("WATER")
							print "*************************inside if observation == moisture_trk******************"
							print watervar
							assetspecset_new = meterconmbo.getMboSet("CG_ASSPEC_HV_NOM_KV") 
							count_new = assetspecset_new.count() 
							print "------------------------------------outside if count_new----------------------------------------------"
							if(count_new>0) :         
								assetspec_new = assetspecset_new.getMbo(0) 
								alnval_new = assetspec_new.getInt("NUMVALUE") 
								print "----------------------------------inside if count_new---------------------------------------------------"
								print "---------------------------------alnval_new---------------------------------------------------"
								print alnval_new
								print "----------------------------------watersat---------------------------------------------------"
								print watersat_var
								print "---------------------------------oiltemp_var---------------------------------------------------"
								print oiltemp_var
								print "---------------------------------watervar---------------------------------------------------"
								print watervar
								if((oiltemp_var>=40) and (watersat_var>=9) and (alnval_new>=300)):
									print '----------@@@@@ for loop inside If Moisture_Trk----------------------------------------------------------------------'
									getObs(ownertable,notifymeasureid,nsource)
								elif((alnval_new>=300) and (watervar>20)):
									print '-----------------------------------@@@@@ for loop inside If Moisture_Trk Clause 1-----------------------------------------'
									getObs(ownertable,notifymeasureid,nsource)
								#Clause-2-Req-1
								elif((alnval_new<=300) and (alnval_new>=101) and (watersat_var>15) and (oiltemp_var>=40)):
									print '@@@@@ for loop inside If Moisture_Trk Clause 2'
									getObs(ownertable,notifymeasureid,nsource)
									print "---------------------------------------Clause 2 completed--------------------------------------------------------------"
								elif((alnval_new<=300) and (alnval_new>=101) and (watervar>25)) :
									print '@@@@@ for loop inside If Moisture_Trk Clause 2 elseif#2'
									getObs(ownertable,notifymeasureid,nsource)   
									print "------------------------------------------Clause 2 completed-----------------------------------------------------------" 
								#Clause-3-Req-1
								elif((alnval_new<=100) and (watersat_var>25.5) and (oiltemp_var>=40)):
									print '@@@@@ for loop inside If Moisture_Trk Clause 3'
									getObs(ownertable,notifymeasureid,nsource)
									print "------------------------------------------Clause 3 completed-------------------------------------------------"
								elif((alnval_new<=100) and (watervar>35)):
									print '@@@@@ for loop inside If Moisture_Trk Clause 3 #elseif2'
									getObs(ownertable,notifymeasureid,nsource)
									print "-------------------------------------------Clause 3 completed-----------------------------------------------"
							
						elif (observation == "CAUTION_O2" and metername == "DGAMAIN" and vclass=="") :
							print 'CAUTIONO2'
							print 'Executing Obs1'
							getObs(ownertable,notifymeasureid,nsource)
						
								#Clause-4-Req-1

					elif ((metername == "DGAMAIN")and(observation=="MOISTURE_TRK") and (vclass=="")):
                                                oiltemp_var=mbo.getInt("OILTEMP")
					        watersat_var=mbo.getInt("WATERSAT")
					        watervar=mbo.getInt("WATER")
						if((watersat_var>40) and (oiltemp_var>=40)):
							print '@@@@@ for loop inside If Moisture_Trk Clause 4 #elseif'
                                                        print oiltemp_var
							getObs(ownertable,notifymeasureid,nsource)
							print "-----------------------------------------Clause 4 completed----------------------------------------------------------"	
						elif((watervar>55)):
							print '@@@@@ for loop inside If Moisture_Trk Clause 4 #elseif2'
							getObs(ownertable,notifymeasureid,nsource)		
							print "-------------------------------------------Clause 4 completed--------------------------------------------------------"				
					else :
						if ((observation == "DIELECTRIC_TRK") and ((metername == "DGAMAIN")) and (vclass == "")):
						  print '-----------------------------Executing Obs2------------------------------------------------------' 
						  print '----------------------------------------DM------------------------------------------'
						  getObs(ownertable,notifymeasureid,nsource)
						  print "---------------------------------------------Done with the clauses------------------------------------"
		elif ((observation == "DIELECTRIC_TRK") and ((metername =="DGAMAIN")) and (vclass<>"")):  
					if alnval <> "FREE BREATHER" :
						getObs(ownertable,notifymeasureid,nsource) 
		else :
					print '------------------$$Not in 3---------------------------------------------------------------------------------------'
					print '------------------------Executing Obs3--------------------------------------------------------------------------------------'
					getObs(ownertable,notifymeasureid,nsource) 
					print '--------------------------@@@@@Executing FOR-----------------------------------------------------------------------------------'
		
finally :
    try :
        mbo.getMboServer().freeDBConnection(ck)
        stmt.close()
        rs.close()
    except :
        print "------------------------------Onsave Measurement error:------------------------------------------"