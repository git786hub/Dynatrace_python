# AUTOSCRIPT NAME: EX2VCSC
# CREATEDDATE: 2014-03-16 18:01:25
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-02-20 13:24:43
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
from psdi.iface.mic import InvokeChannelCache
#from java.util import HashMap
#from java.util import WeakHashMap
from java.util import Date

if mbostatus == 'APPR'  and mbo.getString("DOCUMENTTYPE") not in ['REVINVOICE','REVCREDIT'] :
    #metaData = WeakHashMap() 
    #metaData['CUSTOM'] = 'EX2VC'
    invokeEngine = InvokeChannelCache.getInstance()
    print "########################################"
    print user
    print "########################################"
    invokeCh = invokeEngine.getInvokeChannel('EX2VC')

    if invokeCh != None :
        try:
            #invokeCh.invoke(metaData, mbo, mbo, None)
            invokeCh.invoke(None, mbo, mbo, None)
        except Exception, e:
            global errorkey, errorgroup
            errorkey="FailedPSCommunication"
            errorgroup="invoice"
        print "Error Count"
        iverrset = mbo.getMboSet('EX2IVERRORSIF')
        errorcount = iverrset.count()
        print errorcount 

        parms=[]
        psreject = False
        psvalidate = False 
        for i in range (errorcount) :
            iverr = iverrset.getMbo(i)
            parms.append(iverr.getString('EX2ERRDESC'))
            if iverr.toBeAdded() and iverr.getString('EX2MSGID') in ['0','5'] and psreject == False :
                psvalidate = True
            if iverr.toBeAdded() and iverr.getString('EX2MSGID') not in ['0','5'] and psreject == False :
                psreject = True
                psvalidate = False

        if  psreject == True :
            mbostatus = 'PSREJ'
            mbo.setValue('HISTORYFLAG', False, MboConstants.NOACCESSCHECK)

            if user=='MXINTADM' :
            	global errorkey, errorgroup, params
            	errorkey="FailedPSValidation"
            	errorgroup="invoice"
            	params=parms
    #metaData.clear() 		
#Added to clear the Mismatch flag on approval and bupend
if mbostatus not in ['MISMATCH']:
	invoiceLine = mbo.getMboSet('INVOICELINE')
	for i in range(invoiceLine.count()):
		ivl = invoiceLine.getMbo(i)
		ivl.setValue('ex2qtymismatch',False,MboConstants.NOACCESSCHECK)
		ivl.setValue('ex2pricemismatch',False,MboConstants.NOACCESSCHECK)


#Script code to restrict the paid date being updated to system date on PAID status change				
if mbo.getTranslator().toInternalString('IVSTATUS', mbostatus) == 'PAID':
 prevpdt=mbo.getMboValue('paiddate').getPreviousValue()
 if prevpdt is not None and prevpdt.asString()!='':
  mbo.setValue('paiddate',prevpdt,MboConstants.NOACCESSCHECK)