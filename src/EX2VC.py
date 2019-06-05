# AUTOSCRIPT NAME: EX2VC
# CREATEDDATE: 2014-03-05 07:11:43
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-02-21 03:05:28
# CHANGEBY: U1HQ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
from psdi.iface.mic import InvokeChannelCache
#from java.util import HashMap
#from java.util import WeakHashMap
from java.util import Date

evalresult=False

mbo.setValue('EX2EVALUVATE',True)

if mbo.getString("DOCUMENTTYPE") != 'REVINVOICE' : 
 #metaData = WeakHashMap() 
 #metaData['CUSTOM'] = 'EX2VC'
 invokeEngine = InvokeChannelCache.getInstance()
 invokeCh = invokeEngine.getInvokeChannel('EX2VC')

 if invokeCh != None :
    try :
        #invokeCh.invoke(metaData, mbo, mbo, None)
        invokeCh.invoke(None, mbo, mbo, None)
    except Exception, e:
        global errorkey, errorgroup
        errorkey="FailedPSCommunication"
        errorgroup="invoice"        

    iverrset = mbo.getMboSet('EX2IVERRORSIF')
    errorcount = iverrset.count()

    psreject = False
    psvalidate = False 
    for i in range (errorcount) :
        iverr = iverrset.getMbo(i)
        if iverr.toBeAdded() and iverr.getString('EX2MSGID') in ['0','5'] and psreject == False :
            psvalidate = True

        if iverr.toBeAdded() and iverr.getString('EX2MSGID') not in ['0','5'] and psreject == False :
            psreject = True
            psvalidate = False


#    if  psreject == True and mbo.getString('STATUS') != 'PSREJ' :
#        mbo.changeStatus('PSREJ',Date(),'Changed By PeopleSoft Validation')

    if psvalidate == True and mbo.getString('STATUS') != 'PSVAL' :
#        mbo.changeStatus('PSVAL',Date(),'Changed By PeopleSoft Validation')
        evalresult = True