# AUTOSCRIPT NAME: IEMSWDHELPER
# CREATEDDATE: 2014-11-12 18:10:01
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-12-18 17:11:00
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

##==============================================================================
# * 
# * IBM Confidential
# * 
# * OCO Source Materials
# * 
# * 5725-E24
# * 
# * (C) COPYRIGHT IBM CORP. 2014
# * 
# * The source code for this program is not published or otherwise
# * divested of its trade secrets, irrespective of what has been 
# * deposited with the U.S. Copyright Office.
# * 
# ***************************** End Standard Header ******************************
#=================================================================================
from psdi.mbo import Mbo
from psdi.mbo import SqlFormat
from psdi.server import MXServer
from psdi.util import MXApplicationException;
from psdi.util import MXException

from psdi.iface.router import HTTPHandler
from java.util import HashMap

from psdi.iface.mic import EndPointCache
from psdi.iface.router import Router

from com.ibm.ism.iemswd.app.license import LicReservHelper
import java.util.ArrayList as ArrayList
import java.lang.Long as Long

import sys

foundJython = False
propName = "pmsc.iem.jythonlib"
jythonLibPath = MXServer.getMXServer().getProperty(propName)
for path in sys.path:
    if (path.find(jythonLibPath) != -1) :
        foundJython = True
if (foundJython == False):
    sys.path.append(jythonLibPath)   

import httplib
from xml.etree import ElementTree as ET
import base64
import string  

class IEMSWDHelper: 
    scriptName = "IEMSWDHELPER: "
       
    # Note: Mbo must be the workorder mbo
    def __init__(self, mbo):
        self.mbo = mbo        
        
    def setJythonPath(self):
        foundJython = False
        propName = "pmsc.iem.jythonlib"
        jythonLibPath = MXServer.getMXServer().getProperty(propName)        
        for path in sys.path:
            if (path.find(jythonLibPath) != -1) :
                foundJython = True
        if (foundJython == False):
            sys.path.append(jythonLibPath)        

    def getMsg(self, msgKey):
        msgGrp = "pmscoffering"
        msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgGrp, msgKey)
        if msg == None:
            raise "Invalid message arguments" + msgGrp + ":" + msgKey
        #else:
            #return msg.getMessage(parms)
        return msg.getMessage()
    
    # this function returns the message for the give message key, message group and parameters
    def getMsgWithParams(self, msgKey, params):
        msgGrp = "pmscoffering"
        msg = MXServer.getMXServer().getMaxMessageCache().getMessage(msgGrp, msgKey)
        if msg == None:
            raise "Invalid message arguments" + msgGrp + ":" + msgKey
        else:
            return msg.getMessage(params)      

    
    def addToSRWorkLog(self, key1, key2):
        originatingTicketSet = self.mbo.getMboSet("SR")
        originatingTicket = originatingTicketSet.getMbo(0)
        if (originatingTicket != None):
            srWorklogSet = originatingTicket.getMboSet("MODIFYWORKLOG")
            srWorklogMbo = srWorklogSet.addAtEnd()
            srWorklogMbo.setValue("clientviewable", 1)            
            srWorklogMbo.setValue("description", self.getMsg(key1))
            srWorklogMbo.setValue("description_longdescription", self.getMsg(key2))    


    def addToSRWorkLogWithParams(self, key1, key2, params):
        originatingTicketSet = self.mbo.getMboSet("SR")
        originatingTicket = originatingTicketSet.getMbo(0)
        if (originatingTicket != None):
            srWorklogSet = originatingTicket.getMboSet("MODIFYWORKLOG")
            srWorklogMbo = srWorklogSet.addAtEnd()
            srWorklogMbo.setValue("clientviewable", 1)            
            srWorklogMbo.setValue("description", self.getMsg(key1))
            srWorklogMbo.setValue("description_longdescription", self.getMsgWithParams(key2, params))    
        
    # Write messages to Workorder set
    def addToWorkLog (self, key1, key2):
        worklogSet = self.mbo.getMboSet("MODIFYWORKLOG")
        worklogMbo = worklogSet.addAtEnd()
        worklogMbo.setValue("clientviewable", 0)
        worklogMbo.setValue("description", self.getMsg(key1))
        worklogMbo.setValue("description_longdescription", self.getMsg(key2))
        
    #write the error message to worklog
    def addErrorToWorkLog (self, key1, errMsg):
        worklogSet = self.mbo.getMboSet("MODIFYWORKLOG")
        worklogMbo = worklogSet.addAtEnd()
        worklogMbo.setValue("clientviewable", 0)
        worklogMbo.setValue("description", self.getMsg(key1))
        worklogMbo.setValue("description_longdescription", errMsg)
        
    # update the status fieed on the IEMSWDMboSet(Custom Mbo)
    def updateStatus(self, iemswdMboSet, status, statusDetail):
        iemswdMbo = iemswdMboSet.moveFirst()
        while iemswdMbo != None:
            self.updateMboStatus(iemswdMbo, status, statusDetail)
            iemswdMbo = iemswdMboSet.moveNext()
            
    # update the status fieed on the IEMSWD (Custom Mbo)
    def updateMboStatus(self, iemswdMbo, status, statusDetail):
        #iemstatus is an alndomain. if the customer change the value, they need to modify the script
        self.setTranslatedIEMStatus(iemswdMbo, status)
        iemswdMbo.setValue("STATUSDETAIL", self.getMsg(statusDetail))
        iemswdMbo.setValue("INITIATETIME", MXServer.getMXServer().getDate())
        
    def setTranslatedIEMStatus(self, iemswdMbo, status):
        # get the translated value from the IEMSTATUS domain 
        statusStr = MXServer.getMXServer().getMaximoDD().getTranslator().toExternalList("IEMSTATUS", status)
        if (statusStr == None):
            statusStr = status
        iemswdMbo.setValue("STATUS", statusStr)
        
    def isStatusEqualSuccess(self, status, mbo):
        # get the internal value from the IEMSTATUS domain        
        sqf = SqlFormat(mbo.getUserInfo(), "domainid=:1 and value = :2")    
        sqf.setObject(1, "ALNDOMAIN", "DOMAINID", "IEMSTATUS") 
        sqf.setObject(2, "ALNDOMAIN", "VALUE", status)
        domainSet = MXServer.getMXServer().getMboSet("ALNDOMAIN", mbo.getUserInfo())
        domainSet.setWhere(sqf.format())
        domain = domainSet.getMbo(0)        
        if (domain != None):
            valueId = domain.getString("valueid") 
            if (valueId == 'IEMSTATUS|SUCCESS'):
                return True
            
        return False        
    
    def getIEMSWDMboWithSourceID(self, iemswdMboSet, computerId):
        iemswdMbo = iemswdMboSet.moveFirst()         
        while (iemswdMbo != None):
            if (iemswdMbo.getString("SOURCEID2") == (computerId)):
                return iemswdMbo
            else:
                iemswdMbo = iemswdMboSet.moveNext()
        return None
    
            
    def updateIEMStatusForMultiAsset(self, iemswdMboSet, actionResults):
        rc = '0'
        done = False
        count = 0
        
        # Potentially filter by a particular computer result from the passed in asset, This only looks for one response for the whole action
        for computer in actionResults.getiterator("Computer"):            
            computerId = computer.attrib.get("ID")          
            state = computer.find('State')     
            actionStatus = computer.find('State').text
            isError = state.get('IsError')
            status = computer.find("Status").text          
            
            print self.scriptName + "updateIEMStatusForMultiAsset: computerId: actionStatus =  " + computerId + ":" + actionStatus
            print self.scriptName + "updateIEMStatusForMultiAsset: error: ", isError
            
            iemswdMbo = self.getIEMSWDMboWithSourceID(iemswdMboSet, computerId)
            
            if (int(isError) != 0):                
                rc = "-1"
                done = True
                self.updateIEMSWDMboWithFailedStatus(iemswdMbo, isError, None)                                
            else:            
                if (int(actionStatus) == 3):
                    count = count  + 1
                    self.updateIEMSWDMboWithSuccessStatus(iemswdMbo)
                elif (int(actionStatus) == 0):
                    count = count + 1
                    self.updateIEMSWDMboWithFailedStatus(iemswdMbo, isError, status)                    
                else:
                    print self.scriptName + " actionStatus = ", actionStatus
                    iemswdMbo.setValue("STATUSDETAIL", status) 
                    
                    
        if (count == iemswdMboSet.count()):            
            return rc
        elif (done == True):
            return rc # failed
        else:
            return None  # in progress
        

    def updateIEMStatus(self, iemswdMbo, actionResults):
        rc = '0'
        done = False        
        # Potentially filter by a particular computer result from the passed in asset, This only looks for one response for the whole action
        for computer in actionResults.getiterator("Computer"):            
            computerId = computer.attrib.get("ID")          
            state = computer.find('State')     
            actionStatus = computer.find('State').text
            isError = state.get('IsError')
            status = computer.find("Status").text                    
            
            print self.scriptName + "updateIEMStatus: computerId: actionStatus =  " + computerId + ":" + actionStatus
            print self.scriptName + "updateIEMStatus: error: ", isError            
            
            if (int(isError) != 0):                
                rc = "-1"
                done = True
                self.updateIEMSWDMboWithFailedStatus(iemswdMbo, isError, None)            
            else:            
                if (int(actionStatus) == 3):
                    done = True
                    self.updateIEMSWDMboWithSuccessStatus(iemswdMbo)                    
                elif (int(actionStatus) == 0):
                    done = True
                    rc = '1'
                    self.updateIEMSWDMboWithFailedStatus(iemswdMbo, isError, status)        
                else:
                    print self.scriptName + " actionStatus = ", actionStatus
                    iemswdMbo.setValue("STATUSDETAIL", status)            
                    
        if (done == True):
            return rc
        else:
            return None  # in progress   
    
    def updateIEMSWDMboWithFailedStatus(self, iemswdMbo, isError, status):        
        print self.scriptName + "received an error deploying software for asset : " + iemswdMbo.getString("ASSETNUM") + " : Error = " + isError
        if (int(isError) != 0):
            params = [isError]
            status = self.getMsgWithParams("iem_invoke_fail_isError", params)                       
            print self.scriptName + "Failed for Asset: " + iemswdMbo.getString("ASSETNUM") +  " : for Software: " +  iemswdMbo.getString("SWNAME") + "  is Error = " + isError
            
        else:            
            print self.scriptName + "Failed for Asset: " + iemswdMbo.getString("ASSETNUM") + " : for Software: " + iemswdMbo.getString("SWNAME") + " : status = " + status
                                 
        self.setTranslatedIEMStatus(iemswdMbo, "FAILED")            
        iemswdMbo.setValue("STATUSDETAIL", status)    

    def updateIEMSWDMboWithSuccessStatus(self, iemswdMbo):
        print self.scriptName + "Deployment success: for assetNum = " + iemswdMbo.getString("ASSETNUM") + " : for Software: " + iemswdMbo.getString("SWNAME")        
        self.setTranslatedIEMStatus(iemswdMbo, "SUCCESS")
        iemswdMbo.setValue("STATUSDETAIL", self.getMsg("iem_deploy_success_sum"))       
            
    def getAssetMboSet(self, iemswdMboSet):
        iemswdMbo = iemswdMboSet.moveFirst()
        whereClause = None
  
        while (iemswdMbo != None):
            if (whereClause == None):
                whereClause = "((assetnum = '" + iemswdMbo.getString("ASSETNUM") + "'" + " and siteid = '"  + iemswdMbo.getString("SITEID") + "')"
            else:
                whereClause = whereClause + " or (assetnum = '" + iemswdMbo.getString("ASSETNUM") + "'" + " and siteid = '" + iemswdMbo.getString("SITEID") + "')"
            iemswdMbo = iemswdMboSet.moveNext()
 
        whereClause = whereClause + ")"
        print "whereclause = ", whereClause
          
        sqlFormat = SqlFormat(iemswdMboSet.getUserInfo(), whereClause)  
        assetMboSet = MXServer.getMXServer().getMboSet("ASSET", self.mbo.getUserInfo())  
        assetMboSet.setWhere(sqlFormat.format())
        assetMboSet.reset()   
        return assetMboSet
    
    def getLicenseInfo(self, iemswdMboSet):
        iemswdMbo = iemswdMboSet.moveFirst()        
        licenseNumList = ArrayList()
        orgList = ArrayList()
        tloamsoftwareList = ArrayList()
        while (iemswdMbo != None):
            licenseNumList.add(iemswdMbo.getString("LICENSENUM"))
            orgList.add(iemswdMbo.getString("ORGID"))
            tloamsoftwareList.add(Long(iemswdMbo.getLong("TLOAMSOFTWAREID")))            
            iemswdMbo = iemswdMboSet.moveNext() 
        return licenseNumList, orgList, tloamsoftwareList
    
    

    def getDeployableSoftwareTaskMbo(self, iemswdMbo):     
        tloamsoftwareId = iemswdMbo.getInt("TLOAMSOFTWAREID")  
        sqlFormat = SqlFormat(self.mbo.getUserInfo(), "tloamsoftwareid = :1")
        sqlFormat.setObject(1, "TLOAMSOFTWARE", "TLOAMSOFTWAREID", str(tloamsoftwareId))
        swMboSet = MXServer.getMXServer().getMboSet("TLOAMSOFTWARE", self.mbo.getUserInfo())
        swMboSet.setWhere(sqlFormat.format())
        swMboSet.reset()
        swMbo = swMboSet.getMbo(0)
      
        if (swMbo != None):
            # we need to get install as the task type exists for a given software package    
            deployableSoftwareSet = swMbo.getMboSet("TAMITDEPLOYSWTASK")
            taskType = MXServer.getMXServer().getMaximoDD().getTranslator().toExternalList("DPASWTASKTYPE", "INSTALL")    
            deployableSoftwareSet.setWhere("tasktype in (" + taskType + ")");
            deployableSoftwareSet.reset()       
            if (deployableSoftwareSet.isEmpty()):
                swName = iemswdMbo.getString("SWNAME")
                print self.scriptName + "Unable to find deployable software of type Install for the software : " + swName  
                self.addToSRWorkLog("iem_swctg_missing_deploytask_sum", "iem_swctg_missing_deploytask_desc")
                self.addErrorToWorkLog("iem_swctg_missing_deploytask_sum", "Unable to find deployable software of type Install for the software : " + swName)
                return None
            else:
                return deployableSoftwareSet.getMbo(0)
        else:
            return None
            
            
    def getFixletId(self, deploySwTaskMbo):
        fixletId = deploySwTaskMbo.getString("TASKID")  
        # strip the comma from the fixletId
        fixletId = fixletId.replace(",", "")    
        print self.scriptName + "fixletId: ", fixletId
        return fixletId
    
    
    def getSiteElement(self, deploySwTaskMbo):
        siteElement = None
    
        siteId = deploySwTaskMbo.getString("SITEID")
        if (siteId != ''):
            siteId = siteId.replace(",", "")
        
        siteName =  deploySwTaskMbo.getString("SITENAME")
      
        print self.scriptName + "siteID: ", siteId
        print self.scriptName + "siteName: ", siteName
      
        if (siteId == '' and siteName == ''):      
            # use master action site.    
            siteElement = "<Sitename></Sitename>"
        elif (siteId != ''):
            siteElement = "<SiteID>" + siteId + "</SiteID>"     
        else:
            siteElement =  "<Sitename>" + siteName + "</Sitename>"
        
        print self.scriptName + "script: siteElement = ", siteElement        
        return siteElement
    
    
    def getComputerIdElement(self, iemswdMboSet, singleAsset):
    
        computerIdElement = None
        iemswdMbo = iemswdMboSet.moveFirst();
        
        while iemswdMbo != None:
            assetSet = iemswdMbo.getMboSet("ASSET")     
            asset = assetSet.moveFirst();
        
            #loop through all the asset and get the computer id from the deployed asset
            while asset != None:        
                dpAssetSet = asset.getMboSet("DEPLOYEDASSET")
                if (dpAssetSet.isEmpty()):
                    self.addToSRWorkLog("iem_missing_deployed_asset_sum", "iem_missing_deployed_asset_desc")
                    self.updateMboStatus(iemswdMbo, "FAILED", "iem_missing_deployed_asset_sum")
                    print self.scriptName + "Unable to get the deployed Asset for the asset: assetNum = ", asset.getString("ASSETNUM")
                    return None 
                else:
                    computerId = dpAssetSet.getMbo(0).getString("SOURCEID2")
                    computerId = computerId.replace(",", "")
                    iemswdMbo.setValue("sourceid2", computerId)     
                    
                    if (computerIdElement == None):                       
                        computerIdElement = "<ComputerID>%s</ComputerID>" % (computerId)
                    else:
                        computerIdElement = computerIdElement + "<ComputerID>%s</ComputerID>" % (computerId)
                        
                asset = assetSet.moveNext()
                
            if (singleAsset == False):
                iemswdMbo = iemswdMboSet.moveNext()
            else:
                break
          
        if (computerIdElement == None):
            print self.scriptName + "Unable to find any computer IDs for the asset"        
            
        print self.scriptName + "computerIdElement = ", computerIdElement              
        return computerIdElement
    
    
    def getRequestPayloadXmlForMultiAssets(self, siteElement, fixletId, computerIdElement):
        takeActionRestPacket =  """<BES xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BES.xsd">
          <SourcedFixletAction>
    
            <SourceFixlet>
            %s
            <FixletID>%s</FixletID>
            <Action>Action1</Action>
            </SourceFixlet>
            <Target>
            %s
            </Target>
    
            <Settings>
              <ActionUITitle>Distribute A Software</ActionUITitle>
              <PreActionShowUI>true</PreActionShowUI>
              <PreAction>
                  <Text>Preaction description</Text>
                  <AskToSaveWork>false</AskToSaveWork>
                  <ShowActionButton>false</ShowActionButton>
                  <ShowCancelButton>false</ShowCancelButton>
                  <DeadlineBehavior>RunAutomatically</DeadlineBehavior>
                  <DeadlineType>Interval</DeadlineType>
                  <DeadlineInterval>PT4M</DeadlineInterval>
                  <ShowConfirmation>false</ShowConfirmation>
              </PreAction>
              <HasRunningMessage>true</HasRunningMessage>
              <RunningMessage>
                  <Text>Distributing A Software</Text>
              </RunningMessage>
              <HasTimeRange>false</HasTimeRange>
              <HasStartTime>false</HasStartTime>
              <HasEndTime>true</HasEndTime>
              <EndDateTimeLocalOffset>P2D</EndDateTimeLocalOffset>
              <HasDayOfWeekConstraint>false</HasDayOfWeekConstraint>
              <ActiveUserRequirement>NoRequirement</ActiveUserRequirement>
              <ActiveUserType>AllUsers</ActiveUserType>
              <HasWhose>false</HasWhose>
              <PreActionCacheDownload>false</PreActionCacheDownload>    
              <Reapply>false</Reapply>
              <HasReapplyLimit>true</HasReapplyLimit>
              <ReapplyLimit>3</ReapplyLimit>
              <HasReapplyInterval>false</HasReapplyInterval>
              <HasRetry>false</HasRetry>
              <HasTemporalDistribution>false</HasTemporalDistribution>
              <PostActionBehavior Behavior="Nothing"></PostActionBehavior>
              <IsOffer>false</IsOffer>
            </Settings>
    
          </SourcedFixletAction>
        </BES>
        """ %  (siteElement, fixletId, computerIdElement)
  
        print self.scriptName + "request = ", takeActionRestPacket
        return takeActionRestPacket      
  
    def getEndpointName(self, deploySwTaskMbo): 
        endPointName = deploySwTaskMbo.getString("ENDPOINTNAME")
        if (endPointName == ''):
            # default to IEMSWDSERVER
            endPointName = "IEMSWDSERVER"    
            print self.scriptName + "Defaulting to IEMSWDSERVER end point"
        else:
            print self.scriptName + "EndPointName = ", endPointName
            
        return endPointName 
    
        
    def getBasicAuth(self, endPointName):        
        # Get EndPoint data - username, password, and hostname
        handler = Router.getHandler(endPointName)
        
        endPointInfo = EndPointCache.getInstance().getEndPointInfo(endPointName)
        iemPassword  = endPointInfo.getProperty("PASSWORD").getValue()
        
        iemUserName = handler.getUserName()
        iemServer = handler.getUrl()
        
        #Parse the url from the TEMServer
        if (iemServer != None):
            urlarray = iemServer.split(":")
            hostName = str(urlarray[1])
            portStr = urlarray[2]
            # if the url ends with / remove it
            if (portStr.endswith('/')):
                port = int(portStr[:-1])
            else:
                port = int(portStr)
            hostName = hostName.replace("/","")
            print "hostName: port = ", hostName, port
        
        if (iemServer == '' or iemUserName == '' or iemPassword == '' or hostName == None or port == None):
            self.addToSRWorkLog("iem_missing_endpoint_info_sum", "iem_missing_endpoint_info_desc")
            print self.scriptName + "Endpoint Information missing for the IEM Server"
            return None, None, None
        
        auth = 'Basic ' + string.strip(base64.encodestring(iemUserName + ':' + iemPassword))
        return auth, hostName, port
                
    def invokeIEMAction(self, endPointName, takeActionRestPacket):
        auth, hostName, port = self.getBasicAuth(endPointName)
        if (auth == None):
            return auth
        
        try:                        
            webservice = httplib.HTTPSConnection(hostName, port)
            print self.scriptName + "invokeIEMAction: after httplib.HTTPSConnection to /api/actions"
            webservice.putrequest('POST', "/api/actions")
            webservice.putheader('Authorization', auth)
            webservice.putheader("Content-Length", str(len(takeActionRestPacket)))
            webservice.endheaders()
        except:
            print self.scriptName + "Unable to connect to the IEM Server: exception: ", sys.exc_info()
            errMsg = str(sys.exc_info()[1])
            self.addErrorToWorkLog("iem_invoke_fail_sum", "Unable to connect to the IEM Server. " + errMsg)
            raise MXApplicationException("pmscoffering", "iem_server_connect_failed", [errMsg])
        
        print self.scriptName + "invokeIEMAction: after endHeaders = ", takeActionRestPacket
        
        webservice.send(takeActionRestPacket)
        print self.scriptName + "invokeIEMAction: after webservice:send"
        # get the response
        res = webservice.getresponse()
        print self.scriptName + "invokeIEMAction: after getresponse"
        return res
    
    
    def getActionStatus(self, endPointName, iemActionId):
        auth, hostName, port = self.getBasicAuth(endPointName)
        if (auth == None):
            return auth
        try:
            webservice = httplib.HTTPSConnection(hostName, port)
            print self.scriptName + "getActionStatus: after httplib.HTTPSConnection to /api/actions/%s/status" %iemActionId
            webservice.putrequest('GET', "/api/action/%s/status" % iemActionId)
            webservice.putheader('Authorization', auth)
            webservice.endheaders()
        except:
            print self.scriptName + "Unable to connect to the IEM Server: exception: ", sys.exc_info()
            errMsg = str(sys.exc_info()[1])
            self.addErrorToWorkLog("iem_check_status_fail_sum", "Unable to connect to the IEM Server. " + errMsg)
            raise MXApplicationException("pmscoffering", "iem_server_connect_failed", [errMsg])
        
        # get the response
        res = webservice.getresponse()
        print self.scriptName + "getActionStatus: after get response"
        return res
    
    def getAllDeploymentStatusReturnCode(self, iemswdMboSet):
        rba_rc = '0'
        iemswdMbo = iemswdMboSet.moveFirst()
        while iemswdMbo != None:
            statusStr = iemswdMbo.getString("STATUS")
            if (self.isStatusEqualSuccess(statusStr, iemswdMbo) == False):            
                rba_rc = '1'                
                params = [iemswdMbo.getString("SWNAME"), iemswdMbo.getString("ASSETNUM"), iemswdMbo.getString("IEMACTIONID"), iemswdMbo.getString("STATUSDETAIL")]
                self.addToSRWorkLogWithParams("iem_invoke_fail_sum", "iem_invoke_fail_desc_params_with_status", params) 
            iemswdMbo = iemswdMboSet.moveNext()
        if (rba_rc == '0'):
            self.addToSRWorkLog("iem_deploy_success_sum", "iem_deploy_success_desc")
        return rba_rc