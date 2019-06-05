# AUTOSCRIPT NAME: ONCALLASSIGN
# CREATEDDATE: 2012-04-02 13:08:32
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2012-12-06 10:59:36
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
# * (C) COPYRIGHT IBM CORP. 2012
# * 
# * The source code for this program is not published or otherwise
# * divested of its trade secrets, irrespective of what has been 
# * deposited with the U.S. Copyright Office.
# * 
# ***************************** End Standard Header ****************************
#==============================================================================
from psdi.server import MXServer
from psdi.mbo import Mbo
from psdi.mbo import SqlFormat
from psdi.mbo import MboSetEnumeration
from psdi.app.common import AvailCalc

from java.util import GregorianCalendar
from java.util import Calendar
from java.util import TimeZone
from java.lang import Integer

import sys

#------------------------ getPersonGroupMbo--------------------------------
#
# getPersonGroupMbo
#
# Inputs:
#     personGroup
#           - name of the person group
# Outputs:
#     Returns
#           - mbo for the specified person group
#           - null if the person group is not found
#
# Description
# Gets the mbo for the specified group name. Uses the userInfo global variable
# set by the main function. Returns null if the person group is not found
#
#------------------------------------------------------------------------------
def getPersonGroupMbo(personGroup):
    # This will return a named mboset which is cached at the server
    personGroupMboSet = mbo.getMboSet("$" + personGroup, "PERSONGROUP", "persongroup='" + personGroup + "'")    
    personGroupMbo = personGroupMboSet.getMbo(0)
    if (personGroupMbo is None):
        print ticketid + ": getPersonGroupMbo: Invalid Person Group: " + personGroup    
    return personGroupMbo

#------------------------ isAssignGroupOnly--------------------------------
#
# isAssignGroupOnly
#
# Inputs:
#     personGroup
#           - name of the person group 
# Outputs:
#     Returns
#           - True if the group is to be assigned as owner group
#           - False if the group members are to be assigned as owner
#
# Description
# Gets the person group mbo and checks the ONCALLASSIGNMETHOD attribute. 
# Returns True if the group is to be assigned as the owner group on the ticket. 
# Else, returns False if a group member from the person group is to be 
# assigned as the owner of the ticket
#
# This value can be set on the person group in Person Groups application under 
# the On Call tab
#-----------------------------------------------------------------------------
def isAssignGroupOnly(personGroup):
    assignGroupOnly = False
    onCallMethod = getOnCallAssignMethod(personGroup)
    if (onCallMethod != None and onCallMethod == 'ONCALL_GROUPONLY'):
        assignGroupOnly = True
    #print ticketid + ": isAssignGroupOnly: personGroup = " + personGroup + ", assignGroupOnly = ", assignGroupOnly
    return assignGroupOnly

#------------------------ setPrevNewTktOwner--------------------------------
#
# setPrevNewTktOwner
#
# Inputs:
#     personGroup
#           - name of the person group
#     currentOwner
#           - name of the owner
#     primaryPerson
#           - name of the unavailable primary person if this is an alternate
#
# Description
# Checks if the on call assignment method is rotation and if so
# sets the previous new ticket owner field on the group. 
# The attribute ONCALLPREVNEWTKTOWNER contains the last person
# who was assigned a new ticket. This is used to determine who should
# be next person to own the next new ticket for rotation. Since the
# rotation is not applied to alternates, this stores the primary person
# if an alternate is assigned a new ticket. The ONCALLPREVNEWTKTOWNER is set if 
# the ticket is new to the person group (meaning this is the first owner assigned 
# from this person group) 
# If a group belonging to a on call frequency contains a next group 
# with a different on call frequency, it is possible that the escalation 
# handling that frequency may try to update the person group at the same. 
# To reduce the contention, get the person group mbo in a separate transaction
# and save it immediately. (ie. Get the person group mbo from the server instead of a 
# using the relationship from the ticket). Also, if the attempt to save fails,
# we catch the exception and try once more.
#------------------------------------------------------------------------------
def setPrevNewTktOwner(personGroup, currentOwner, primaryPerson):
    
    prevNewTktOwner = None
    onCallMethod = getOnCallAssignMethod(personGroup)
    
    if (onCallMethod != None and onCallMethod == 'ONCALL_ROTATION'):        
        personGroupMboSet = MXServer.getMXServer().getMboSet("PERSONGROUP", userInfo)
        sqf = SqlFormat(userInfo, "persongroup=:1") 
        sqf.setObject(1, "PERSONGROUP", "PERSONGROUP", personGroup) 
        personGroupMboSet.setWhere(sqf.format())
        personGroupMbo = personGroupMboSet.getMbo(0)
        
        # if alternate. use the primary for the prevNewTktOwner        
        if (primaryPerson != None):               
            prevNewTktOwner = primaryPerson
        else:
            prevNewTktOwner = currentOwner
        personGroupMbo.setValue("ONCALLPREVNEWTKTOWNER", prevNewTktOwner) 
                
        try:    
            personGroupMbo.getThisMboSet().save()
        except:
            print "setPrevNewTktOwner: The following exception occurred on updating the first rotation assign person on the person group: " + personGroup
            print sys.exc_info()
            print "setPrevNewTktOwner: Attempting to save again since it is possible that another escalation was updating this group at the same time"
            personGroupMboSet.reset()
            personGroupMbo = personGroupMboSet.getMbo(0) 
            personGroupMbo.setValue("ONCALLPREVNEWTKTOWNER", prevNewTktOwner) 
            try: 
                personGroupMbo.getThisMboSet().save()
            except:
                print "setPrevNewTktOwner: The following exception occurred on updating the first rotation assign person on the person group: " + personGroup
                print sys.exc_info() 
                      

#------------------------ getOnCallAssignMethod------------------------------
#
# getOnCallAssignMethod
#
# Inputs:
#     personGroup
#           - name of the person group 
# Outputs:
#     Returns
#           - the algorithm for choosing the next available person in the person group
#           
#
# Description
# Gets the value of the ONCALLASSIGNMETHOD attribute from the person 
# group which is of type ONCALLASSIGNMETHOD domain.
# Currently, the supported values are: Group Only, Sequence, Workload, Rotation
#
# Sequence - This algorithm assigns the ticket to the available 
# member with the lowest sequence number
# Workload - This algorithm assigns the ticket to the available member
# with the least number of active tickets
# Rotation - This algorithm assigns the ticket to the available member with the 
# next highest sequence number to the previous owner. This is the round-robin 
# version of the sequence algorithm. 
#-----------------------------------------------------------------------------
def getOnCallAssignMethod(personGroup):
    
    onCallAssignMethod = None
    
    personGroupMbo = getPersonGroupMbo(personGroup) 
    if (personGroupMbo != None): 
        onCallAssignMethod = personGroupMbo.getString("ONCALLASSIGNMETHOD")
     
    # ONCALLASSIGNMETHOD attribute maps to the value column of the alndomain. 
    # Since the value column is translated, need to get the 
    # internal value (valueid column from the alndomain)
    if (onCallAssignMethod != None and onCallAssignMethod != ''):    
        sqf = SqlFormat(userInfo, "domainid=:1 and value = :2")    
        sqf.setObject(1, "ALNDOMAIN", "DOMAINID", "ONCALLASSIGNMETHOD") 
        sqf.setObject(2, "ALNDOMAIN", "VALUE", onCallAssignMethod)
        domainSet = MXServer.getMXServer().getMboSet("ALNDOMAIN", userInfo)
        domainSet.setWhere(sqf.format())
        domain = domainSet.getMbo(0)        
        if (domain != None):
            onCallAssignMethod = domain.getString("valueid")
    #print ticketid + ": getOnCallAssignMethod: personGroup = " + personGroup + ",  onCallAssignMethod = ", onCallAssignMethod           
    return onCallAssignMethod

#----------------------------------getNextGroup -----------------------------
#
# getNextGroup
#
# Identifies the next group to use.
#
# Inputs:
#     personGroup
#           - name of the current person group
# Outputs:
#     Returns
#           - name of the next person group
#           - null if there is no next group
#
# Description
# Returns the attribute NEXTGROUP which contains the next group for the specified group
#-----------------------------------------------------------------------------------
def getNextGroup(personGroup):
    nextGroup = None
    personGroupMbo = getPersonGroupMbo(personGroup)
    if (personGroupMbo != None):
        nextGroup = personGroupMbo.getString("NEXTGROUP")       
    print ticketid + ": getNextGroup: nextGroup for personGroup: " + personGroup + " = " + nextGroup
    return nextGroup

#------------------------ getNextPrimary-----------------------------
#
# getNextPrimary
#
# Inputs:
#     currentPerson 
#           - name of the current person 
#     personGroup
#           - name of the person group from which the next primary should be 
#             selected
#     firstRotationAssnPerson
#           - name of the person who was initially assigned the ticket 
#             by the on call escalation rotation among this group 
# Outputs:
#     Returns
#           - next primary person from the specified person group
#             null if there are no more person in the specified group
#
#           - PersonGroupTeamMbo associated with the next primary person
#             null if there are no more person in the specified group
# Description
# Gets all the primary members of the person group and checks if the 
# currentPerson is a primary member of the person group. If so, it gets the next 
# primary person in the sequence after the currentPerson.
# If the currentPerson is not a member of personGroup, or is null, 
# then it returns the first person in the group. 
#-----------------------------------------------------------------------------
def getNextPrimary(currentPerson, personGroup, firstRotationAssnPerson):    
    nextPerson = None
    pgtMbo = None
    member = False    
    
    primaryMboSet = getPrimaryMembers(personGroup)
    
    if (primaryMboSet == None or primaryMboSet.isEmpty()):
        print ticketid + ": getNextPrimary: The group " + personGroup + " does not have any members"
    else:         
        if (currentPerson != None and len(currentPerson) > 0):
            primaryIter = MboSetEnumeration(primaryMboSet)            
            while (primaryIter.hasMoreElements()):
                mbo = primaryIter.nextMbo()
                primary = mbo.getString("resppartygroup")
                if (primary == currentPerson):
                    print ticketid + ": getNextPrimary: Person " + currentPerson + " is a primary member of group: " + personGroup
                    member = True
                    break        
           
            if (member == False):
                print ticketid + ": getNextPrimary: Person: " + currentPerson + " not a primary member of group: " + personGroup
                currentPerson = None              

        isPrimary = True
        nextPerson, pgtMbo = getNextPersonFromMemberList(primaryMboSet, currentPerson, personGroup, isPrimary, firstRotationAssnPerson)
 
    return nextPerson, pgtMbo

#-------------------------getNextAlternate---------------------------------
#
# getNextAlternate
#
# Inputs:
#     currentAlternate
#           - name of the current alternate person  
#     personGroup
#           - name of the person group from which the next alternate person 
#             should be selected
#     primaryPerson
#           - name of the primary person for the current alternate
# Outputs:
#     Returns
#           - next alternate person for the primaryPerson
#             null if there are no more alternates for primaryPerson
#
#           - PersonGroupTeamMbo for the next alternate person
#             null if there are no more alternates for primaryPerson 
#
# Description
# Gets all the alternate members of the person group for the given
# primary and checks if the current alternate is a member of the person 
# group. If so, then it gets the next alternate person in the  
# sequence after the currentAlternate. If the currentAlternate is not a 
# member of personGroup, or is null, then it returns the first alternate
# person in the group
#--------------------------------------------------------------------------
def getNextAlternate(currentAlternate, personGroup, primaryPerson):
    nextPerson = None
    pgtMbo = None
    member = False   

    alternateMboSet = getAlternateMembers(personGroup, primaryPerson)

    if (alternateMboSet == None or alternateMboSet.isEmpty()):
        print ticketid + ": getNextAlternate: The group: " + personGroup + " does not have any alternate members"
    else:  
        if (currentAlternate != None and len(currentAlternate) > 0):
            altIter = MboSetEnumeration(alternateMboSet)            
            while (altIter.hasMoreElements()):
                mbo = altIter.nextMbo()
                alternate = mbo.getString("respparty")
                if (alternate == currentAlternate):
                    print ticketid + ": getNextAlternate: Person: " + currentAlternate + " is an alternate member for the primary: " + primaryPerson
                    member = True
                    break        
           
            if (member == False):
                print ticketid + ": getNextAlternate: Person: " + currentAlternate + " is not an alternate for the primary: " + primaryPerson
                currentAlternate = None 
            
                                    
        isPrimary = False  
        nextPerson, pgtMbo = getNextPersonFromMemberList(alternateMboSet, currentAlternate, personGroup, isPrimary, None)                

    return nextPerson, pgtMbo 

#------------------------------getNextPersonFromMemberList-------------------------
#
# getNextPersonFromMemberList
#
#
# Inputs:
#      pgtMboSet
#           - mbo set of the members (primary or alternate) of the person group
#      currentPerson
#           - name of the current person 
#      personGroup
#           - name of the person group
#      isPrimary
#           - flag indicating if the pgtMboSet consists of primary members
#      firstRotationAssnPerson
#           - name of the person who was initially assigned the ticket 
#             by the on call escalation rotation among this group 
#             
# Outputs:
#      Returns
#           - first person if currentPerson is null 
#           - next person if currentPerson is not null 
#
# Description
# Calls the corresponding algorithm based on the value of the ONCALLASSIGNMETHOD 
# attribute. Default behavior is to get the next person by the sequence number  
#
# This function would be the place to add any additional logic to use some 
# other algorithm for identifying the next person
#-----------------------------------------------------------------------------
def getNextPersonFromMemberList(pgtMboSet, currentPerson, personGroup, isPrimary, firstRotationAssnPerson):

    onCallMethod = getOnCallAssignMethod(personGroup)
    
    if (onCallMethod != None and onCallMethod == 'ONCALL_ROTATION'):            
        return getNextPersonByRotation(pgtMboSet, currentPerson, personGroup, isPrimary, firstRotationAssnPerson)
    
    # Workload algorithm is handled directly by the main routine
        
    # default to sequence    
    return getNextPersonBySequence(pgtMboSet, currentPerson)
            

#------------------------------getNextPersonBySequence-------------------------
#
# getNextPersonBySequence
#
#
# Inputs:
#      pgtMboSet
#           - mbo set of the members (primary or alternate) of the person group
#      currentPerson
#           - name of the current person    
#             
# Outputs:
#      Returns
#           - next person in the specified member list
#             null if there are no more members in the member list
#
#           - PersonGroupTeamMbo associated with the next person
#             null if there are no more members in the member list
#
# Description
# Starts from currentPerson and finds the next sequential person in the 
# member list.  If currentPerson is null, it returns the first person 
# from the member list. The determination of next is by the member sequence number.
#-----------------------------------------------------------------------------   
def getNextPersonBySequence(pgtMboSet, currentPerson): 
    nextPerson = None    
    pgtMbo = None
    count = pgtMboSet.count()
    i = 0; 
    for i in range(count):
        pgtMbo = pgtMboSet.getMbo(i)         
        if (currentPerson == None):           
            break
        else:
            person = pgtMbo.getString("RESPPARTY")
            if (person == currentPerson):
                if (i + 1) < count:
                    pgtMbo = pgtMboSet.getMbo(i + 1)
                else:
                    pgtMbo = None
                break

    if (pgtMbo != None):
        nextPerson = pgtMbo.getString("RESPPARTY")

    print ticketid + ": getNextPersonBySequence: nextPerson = " , nextPerson
    return nextPerson, pgtMbo
#------------------------------getNextPersonByWorkload-------------------------
#
# getNextPersonByWorkload
#
#
# Inputs:
#      currentPerson
#           - name of the current person
#      personGroup
#           - name of the person group
#             
# Outputs:
#      Returns
#           - next person with minimum active tickets
#             null if there are no more members in the group
#
#           - PersonGroupTeam Mbo associated with the next person
#             null if there are no more members in the group
#
# Description
# Finds the next person in the group with the least number of active tickets 
# from the member list (excluding the current person and the previous owners
# assigned by the on call escalation).
# 
# This method does the following:  
#  1. First gets all the primary group members and stores in the workload cache.
#  2. Removes the current owner if he is in the primary member list and also
#     removes the members who were previously assigned to this ticket 
#     by the on call escalation.
#  3. Then, checks the availability of these primary members. 
#  4. If unavailable, replaces the primary with alternates 
#     (provided that alternates can be used and are available). 
#  5. Again, remove the alternate members who were previously assigned to this 
#     ticket by the on call escalation.  
#  6. From the resulting list of members, the person with the 
#     least number of active tickets is selected as the next person.
#
# The previous owners are calculated as follows:  
# The ONCALLSTARTTIME attribute on the ticket stores the time at which this 
# ticket was first assigned by the on call escalation for the current group. 
# Any person who owned this ticket at or after this time are considered as 
# previous owners.
#
# Active tickets includes tickets in QUEUED and INPROG states.  
# If this needs to include any other states, modify the script parameter,
# activeTicketStatus. The value of this parameter should be 
# comma separated internal values of the synonym domain INCIDENTSTATUS.   
# By default, only the INPROG,QUEUED states are considered as active states. 
#
# If the ticket status is changed from QUEUED status, the
# ONCALLSTARTTIME attribute is reset by another script, ONCALLRESETATTRS. 
# For example, if the ticket was assigned to person P1, and then to P2 by the 
# on call escalation and P2 took ownership of it, the ticket status is changed 
# to INPROG. The ONCALLSTARTTIME attribute is reset. Therefore, if the ticket 
# status is changed to QUEUED, it is treated as if it was put back in the queue 
# and the previous owners are ignored           
#--------------------------------------------------------------------------------   
def getNextPersonByWorkload(currentPerson, personGroup): 
    nextPerson = None    
    pgtMbo = None
    
    pgtMboSet = getPrimaryMembers(personGroup)
    
    if (pgtMboSet == None or pgtMboSet.isEmpty()):
        print ticketid + ": getNextPersonByWorkload: The group " + personGroup + " does not have any members"        
    else:         
        addPrimaryMembersToWorkLoadCache(pgtMboSet)
        removePrevOwnersFromWorkloadCache(personGroup)
            
        i = 0    
        pgtMbo = pgtMboSet.getMbo(i)
        
        while (pgtMbo is not None):            
            primaryPerson = pgtMbo.getString("RESPPARTY")
            
            # if the primary was one of the previous owners, he would have been removed from workload cache.
            # check if he is in cache                    
            if (primaryPerson in workLoadCache):
                available = isPersonAvailable(pgtMbo, primaryPerson)            
                if (available == False):
                    # remove the primary since he is not available
                    workLoadCache.remove(primaryPerson) 
                    
                    if (useAlternate(primaryPerson, pgtMbo)):                              
                        addAlternateMembersToWorkLoadCache(personGroup, primaryPerson)
                        removePrevOwnersFromWorkloadCache(personGroup)
            i = i + 1 
            pgtMbo = pgtMboSet.getMbo(i)
                        
                            
        nextPerson, pgtMbo = getPersonWithMinimumTickets(personGroup)                           
    
    print ticketid + ": getNextPersonByWorkload: nextPerson = " , nextPerson
    return nextPerson, pgtMbo

#------------------------------addPrimaryMembersToWorkLoadCache-------------------------
#
# addPrimaryMembersToWorkLoadCache
#
#
# Inputs:
#      pgtMboSet
#           - mbo set of primary members of the person group
#             
#
# Description
# Stores the primary members in the workload cache. 
#----------------------------------------------------------------------------   
def addPrimaryMembersToWorkLoadCache(pgtMboSet):  
       
    i = 0
    pgtMbo = pgtMboSet.getMbo(i)
       
    while (pgtMbo is not None):           
        workLoadCache.append(pgtMbo.getString("RESPPARTY"))
        i = i + 1
        pgtMbo = pgtMboSet.getMbo(i)      
                

#------------------------------addAlternateMembersToWorkloadCache-------------------------
#
# addAlternateMembersToWorkLoadCache
#
#
# Inputs:
#      personGroup
#           - name of the person group
#      currentPerson
#           - name of the current primary person    
#             
#
# Description# 
# This method gets the alternate members for the current primary person
# and adds them to the workload cache if they are available
#----------------------------------------------------------------------------   
def addAlternateMembersToWorkLoadCache(personGroup, currentPerson):
        
    alternateMboSet = getAlternateMembers(personGroup, currentPerson)
    i = 0
    pgtMbo = alternateMboSet.getMbo(i)
       
    while (pgtMbo is not None):        
        alternatePerson = pgtMbo.getString("RESPPARTY")
        if (alternatePerson in workLoadCache):
            print ticketid + ": addAlternateMembersToWorkLoadCache: Alternate " + alternatePerson + " is already in workload cache"
        else:    
            available = isPersonAvailable(pgtMbo, alternatePerson)
            if (available == True):         
                workLoadCache.append(alternatePerson)
        i = i + 1
        pgtMbo = alternateMboSet.getMbo(i)                           
    
#------------------------------removePrevOwnersFromWorkloadCache-------------------------
#
# removePrevOwnersFromWorkloadCache
#
#
# Inputs:
#      personGroup
#           - name of the person group
#             
#
# Description
# Removes the previous owners of the ticket from the workload cache.
# The previous owners are obtained from the TKOWNERHISTORY table.
#
# This method gets all the records from the TKOWNERHISTORY table for the
# ticket using the relationship OWNERHISTORY. It checks the value of the  
# script parameter, onCallStartTime (which maps to the attribute ONCALLSTARTTIME).
#
# If the onCallStartTime is null, this is a new ticket to the on call 
# escalation for the current person group. Therefore, only the current 
# owner is removed from the member list if he is a member of the owner group. 
# If the onCallStartTime is not null, this ticket is already processed by the 
# escalation for the current group. Therefore, it removes all the previous 
# owners from the member list (assigned after this time). 
# 
# To get all of the previous owners assigned by escalation, the OWNDATE attribute 
# on the TKOWNERHISTORY table is checked. If the OWNDATE is equal to or 
# after the onCallStartTime - it is assumed that it was assigned by the escalation.      
#---------------------------------------------------------------------------------
def removePrevOwnersFromWorkloadCache(personGroup):
    
    historySet = mbo.getMboSet("OWNERHISTORY")     
    sql = None
    
    if (onCallStartTime != None and onCallStartTime != ''):    
        sql = "ASSIGNEDOWNERGROUP=:1 and OWNDATE >= " + SqlFormat.getTimestampFunction(onCallStartTime)
    else:
        # if the last owner is a member of the current owner group,
        # remove him from the list
        sql = "ASSIGNEDOWNERGROUP=:1 and rowstamp = (select max(rowstamp) from TKOWNERHISTORY where TICKETID=:2)"
          
    sqf = SqlFormat(userInfo, sql)
    sqf.setObject(1, "TKOWNERHISTORY", "ASSIGNEDOWNERGROUP", personGroup)
    sqf.setObject(2, "TKOWNERHISTORY", "TICKETID", ticketid)
    historySet.setWhere(sqf.format())
    historySet.reset()                          
    
    
    i = 0  
    personMbo = historySet.getMbo(i)
    
    while (personMbo is not None):
        person = personMbo.getString("OWNER")        
        if (person in workLoadCache):
            workLoadCache.remove(person)
            print ticketid + ": removePrevOwnersFromWorkloadCache: removed = ", person
        i = i + 1
        personMbo = historySet.getMbo(i)
                            
#------------------------------getPersonWithMinimumTickets-------------------------
#
# getPersonWithMinimumTickets
#
#
# Inputs:
#      personGroup
#           - name of the person group    
#             
# Outputs:
#      Returns
#           - first person with minimum active tickets assigned
#           - null if there are no more members available
#
#           - PersonGroupTeam Mbo associated with the next person
#             null if there are no more members available
#
# Description
# Finds the person with the least number of active tickets from the member 
# list. The workload cache contains the list of members who are available. 
# This method queries the database to get the person with the least 
# number of active tickets.  
#
# The list of the active ticket status is specified in the script parameter, 
# activeTicketStatus, as comma separated internal values of the synonym 
# domain, INCIDENTSTATUS. The default is to include any tickets in the 
# following states: INPROG, QUEUED 
#----------------------------------------------------------------------------    
def getPersonWithMinimumTickets(personGroup):
    
    nextPerson = None
    pgtMbo = None 
      
    memberCount = len(workLoadCache)
    if (memberCount == 0):
        print ticketid + ": getPersonWithMinimumTickets: There are no more members left"
        return nextPerson, pgtMbo
   
    # construct an sql to get the person with least number of active tickets    
      
    personSql = "("
    for i in range(memberCount):
        personSql = personSql + "'" + workLoadCache[i] + "'"
        if  i < (memberCount - 1):
            personSql = personSql + ","       
    personSql = personSql + ")"
    print ticketid + ": getPersonWithMinimumTickets: personSql = ", personSql  
    
    # get list of synonym values that can be used in the sql query 
    # for example, the values are specifed in the GUI as INPROG, QUEUED
    # need to convert it to 'INPROG', 'QUEUED' to use it in the sql query
    statusValues = ":&synonymlist&_incidentstatus[" + activeTicketStatus + "]"   
    sqlStatusValues = Mbo.getSynonymValueWhere(statusValues)
    print ticketid + ": getPersonWithMinimumTickets: sqlStatusValues ", sqlStatusValues
       
    sql = "select p.personid, count(incident.owner) as count "
    sql = sql + "from person p full outer join incident incident on (incident.owner=p.personid and "
    sql = sql + "incident.status in ("
    sql = sql + sqlStatusValues + ")) "
    sql = sql + "where p.personid in " + personSql
    sql = sql + " group by p.personid order by count, p.personid"    
        
    print ticketid + ": getPersonWithMinimumTickets: sql = ", sql           
        
    s = None
    rs = None
    conn = None
    connKey = None
    try:
        connKey = MXServer.getMXServer().getDBManager().getSystemConnectionKey()
        conn = MXServer.getMXServer().getDBManager().getConnection(connKey)
           
        s = conn.createStatement()
        rs = s.executeQuery(sql)
        

        if (rs.next()):
            nextPerson = rs.getString(1)
            count = rs.getInt(2)
            print ticketid + ": getPersonWithMinimumTickets: nextPerson : count = " + nextPerson + " : " , count            
            pgtMboSet = getPersonGroupMbo(personGroup).getMboSet("ALLPERSONGROUPTEAM")            
            pgtMboSet.setWhere("respparty = '" + nextPerson + "'")
            pgtMboSet.reset()
            pgtMbo = pgtMboSet.getMbo(0)
    
    finally:
        try:
            if (rs != None):
                rs.close()
            if (s != None):
                s.close()
            if (conn != None):
                MXServer.getMXServer().getDBManager().freeConnection(connKey); 
        except:
            print "Exception Caught: ", sys.exc_info()
     
    return nextPerson, pgtMbo

#------------------------------isOnCallFirstRotationAssnPersonValid-------------------------
#
# isOnCallFirstRotationAssnPersonValid
#
#
# Inputs:
#    personGroup
#           - name of the current on call person group
#    currentOwner
#           - name of the current owner
#    firstRotationAssnPerson
#           - name of the person who was initially assigned the ticket 
#             by the on call escalation rotation among this group 
#
# Outputs:
#     Returns
#           - True if the firstRotationAssnPerson is a member of the personGroup
#           - False if the firstRotationAssnPerson is not a member of the personGroup
#
# Description
# This method checks if the firstRotationAssnPerson specified on the
# ticket is a member of the person group. This check is necessary to catch the 
# scenario where the ticket could be manually changed from one owner group 
# to another while the first rotation assigned person is still pointing to the
# previous group. Also, if the person who was assigned ownership, removes his 
# ownership manually (by changing assigning it to a owner group), the 
# firstRotationAssnPerson is no longer valid. 
# Returns True if the firstRotationAssnPerson is a member of the personGroup 
# and if the current owner is not null. Else, returns False.
#-----------------------------------------------------------------------------------
def isOnCallFirstRotationAssnPersonValid(personGroup, currentOwner, firstRotationAssnPerson):
    valid = False   
    
    if (firstRotationAssnPerson != None):
        onCallMethod = getOnCallAssignMethod(personGroup)
        
        if (onCallMethod != None and onCallMethod == 'ONCALL_ROTATION'):
            primaryMboSet = getPrimaryMembers(personGroup)
            
            if (primaryMboSet == None or primaryMboSet.isEmpty()):
                print ticketid + ": isOnCallFirstRotationAssnPersonValid: The group " + personGroup + " does not have any members"
            else:
                primaryIter = MboSetEnumeration(primaryMboSet)
                while (primaryIter.hasMoreElements()):
                    mbo = primaryIter.nextMbo()
                    primary = mbo.getString("resppartygroup")
                    if (primary == firstRotationAssnPerson):
                        print ticketid + ": isOnCallFirstRotationAssnPersonValid: onCallFirstRoationAssnPerson: " + firstRotationAssnPerson + " is a member of the " + personGroup
                        if (currentOwner != None):    
                            valid = True
                        break          
                                    
    print ticketid + ": isOnCallFirstRotationAssnPersonValid: valid = ", valid                      
    return valid    
    
#------------------------------getNextPersonByRotation-------------------------
#
# getNextPersonByRotation
#
#
# Inputs:
#      pgtMboSet
#           - mbo set of the members (primary or alternate) of the person group
#      currentPerson
#           - name of the current person 
#      personGroup
#           - name of the person group
#      isPrimary
#           - flag indicating if the pgtMboSet consists of primary members
#      firstRotationAssnPerson
#           - name of the person in the personGroup who was initially assigned the 
#             ticket by the on call escalation rotation              
#             
# Outputs:
#      Returns
#           - next person based on the rotation algorithm
#             null if there are no more members in the member list
# 
#           - PersonGroupTeamMbo associated with the next person
#             null if there are no more members in the member list
#
#
# Description
# Two new attributes for this algorithm are: 
#      ONCALLPREVNEWTKTOWNER    - on persongroup object, stores the last 
#                                 member who was assigned a new ticket.
#      ONCALLFIRSTROTASSNPERSON - on ticket object, stores the initial member 
#                                 of the owner group, who was assigned this ticket.
# 
# This algorithm checks the value of the ONCALLPREVNEWTKTOWNER attribute on the 
# person group. If null (i.e., no one is assigned any ticket), it assigns the ticket 
# to the member with the lowest sequence number. For example, if a group contains 
# person1, person2, person3 as the members in the ascending order of sequence numbers, 
# the first new ticket t1 will be assigned to person1.
#
# The algorithm updates the ONCALLPREVNEWTKTOWNER attribute in the persongroup object 
# (with person1 in this case) and also stores this member on the ticket in the attribute, 
# ONCALLFIRSTROTASSNPERSON.
#
# When the next ticket appears in the queue, the algorithm assigns the ticket to the
# member with the next highest sequence number to the ONCALLPREVNEWTKTOWNER and updates
# this attribute. Thus, second new ticket t2 will be assigned to person2 and third new
# ticket t3 will be assigned to person3 and so on.
#
# If the ownership is not claimed and say, ticket t1 is processed by escalation again,
# the algorithm assigns it to person2, i.e., the person with the next highest sequence 
# number than the current owner. If it reaches the end of the list, it wraps around
# and starts with the person with the lowest sequence number.  
#
# This continues until the iteration has cycled through all members of the group, 
# indicated by matching the value in ONCALLFIRSTROTASSNPERSON. It returns null when there 
# are no members left. 
#    
# The algorithm is applied only to primary members. For alternate members, 
# the sequence algorithm is used.
#  
# When the ownership is claimed on the ticket, the ticket status changes from 
# QUEUED state to some other state (for example: INPROG). If for some reason, 
# the owner changes the status back to QUEUED, the ticket will appear in the 
# queue again, it needs to be processed as a new ticket.
#
# For this to happen, an attribute launch point is defined on the STATUS attribute 
# to clear the ONCALLFIRSTROTASSNPERSON on the incident when the status is changed 
# from QUEUED.  This is handled by the automation script, ONCALLRESETATTRS
#----------------------------------------------------------------------------   
def getNextPersonByRotation(pgtMboSet, currentPerson, personGroup, isPrimary, firstRotationAssnPerson):
    
    nextPerson = None
    pgtMbo = None     
    
    # use the sequence algorithm for alternates 
    if (isPrimary == False):
        return getNextPersonBySequence(pgtMboSet, currentPerson)
         
    prevNewTktOwner = getPersonGroupMbo(personGroup).getString("ONCALLPREVNEWTKTOWNER")
    print ticketid + ": getNextPersonByRotation: prevNewTktOWner = ", prevNewTktOwner
        
    if (firstRotationAssnPerson == None or firstRotationAssnPerson == '' or currentPerson == None):
        if (prevNewTktOwner == ''): 
            # no one in the group has been assigned any tickets 
            nextPerson, pgtMbo = getNextPersonBySequence(pgtMboSet, currentPerson)           
        else:                          
            count = pgtMboSet.count()            
            i = 0
            newIndex = -1
              
            # locate the previous new ticket owner in the mboset in order to select the next person
            # if we did not find the previous new ticket owner in the group or if he is the last person
            # in the group, we need to start from the beginning.       
            prevNewTktOwnerIndex = -1                      
                                    
            while (i < count):         
                person = pgtMboSet.getMbo(i).getString("RESPPARTY")
                print ticketid + ": getNextPersonByRotation: person = ", person                                
                if (person == prevNewTktOwner):
                    prevNewTktOwnerIndex = i           
                    break
                else:
                    i = i + 1                   
                                              
            if (prevNewTktOwnerIndex + 1) < count:
                newIndex = prevNewTktOwnerIndex + 1
            else:
                # wrapped around or prevNewTktOwner not found. start from zero
                newIndex = 0
            print ticketid + ": getNextPersonByRotation: newIndex = ", newIndex    
            pgtMbo = pgtMboSet.getMbo(newIndex)                     
    else:           
        # This is not a new ticket as it is already being assigned by the on call escalation 
        # Find the current person in the mboset and increment by 1 to get the next person
        count = pgtMboSet.count()
        for i in range(count):
            pgtMbo = pgtMboSet.getMbo(i)
            person = pgtMbo.getString("RESPPARTY")
            if (person == currentPerson):
                if (i + 1) < count:
                    pgtMbo = pgtMboSet.getMbo(i + 1)
                else:
                    pgtMbo = pgtMboSet.getMbo(0)
                break   
            
        # stop if the next person matches the initial person who was assigned this ticket   
        if (pgtMbo.getString("RESPPARTY") == firstRotationAssnPerson):
            # no more person left 
            pgtMbo = None                        
            
    if (pgtMbo != None):
        nextPerson = pgtMbo.getString("RESPPARTY")                        
          
    print ticketid + ": getNextPersonByRotation: nextPerson = " , nextPerson
    return nextPerson, pgtMbo

#------------------------------getPrimaryMembers-------------------------
#
# getPrimaryMembers
#
# Inputs:
#      personGroup
#           - name of the person group
# Outputs:
#      Returns
#           - mbo set of PersonGroupTeam sorted by respartygroupseq 
#     
#Description
# Gets the list of primary members for the person group sorted by sequence number
#-----------------------------------------------------------------------------
def getPrimaryMembers(personGroup):
    personGroupMbo = getPersonGroupMbo(personGroup) 
    if (personGroupMbo != None):   
        return personGroupMbo.getResponsibleParty()
    
#------------------------------getAlternateMembers-------------------------
#
# getAlternateMembers
#
#
# Inputs:
#     personGroup
#         - name of the person group
#     primaryPerson
#         - primary person for whom the alternates are to be obtained
#
# Outputs:
#     Returns
#         - mbo set of PersonGroupTeam representing the alternate
#           members for the specified primary person 
#
# Description
# Returns the mbo set of alternate members for the given primary person
# The mbo list is sorted by sequence number
#-----------------------------------------------------------------------------
def getAlternateMembers(personGroup, primaryPerson):
    personGroupMbo = getPersonGroupMbo(personGroup)
    if (personGroupMbo != None): 
        alternateMboSet = personGroupMbo.getMboSet("PERSONGROUP_ALTERNATEMEMBERS")
        pgtSqf = SqlFormat(userInfo, "resppartygroup = :1")    
        pgtSqf.setObject(1, "PERSONGROUPTEAM", "RESPPARTYGROUP", primaryPerson)
        alternateMboSet.setWhere(pgtSqf.format())
        alternateMboSet.setOrderBy("resppartyseq")
        alternateMboSet.reset()        
        return alternateMboSet

#-----------------------------isPersonAvailable-------------------------------
#
# isPersonAvailable
#
# Inputs:
#     person
#           - name of the person to be checked for availability
#     pgtMbo 
#           - PersonGroupTeamMbo for the person           
# Outputs:
#     Returns
#           - True if the person is available
#           - False if the person is unavailable
#
# Description
# This method returns True or False based on the calendar entries. 
# If the person does not have a calendar, it checks the value of the script variable, 
# useModAvailRecordWorkTime. If modification availability 
# entries are used to record the work time, then this variable
# should be set to 1. In that case, the person is available only if there is a 
# work entry in the modavail mbo for the given period. If the modavail entries
# are not used to record work time, then the variable should be set to 0. 
# In the absence of a calendar, if the variable is 0, it checks 
# if there are any non-work entries in the modavail mbo. If so, returns False 
# since the person is unavailable. Else, returns True. If the variable is set to 1, 
# it checks if there are any work entries. If so, returns True. 
# 
# The useModAvailRecordWorkTime value can be changed in the Automation Scripts 
# application under the Variables tab. The values can be 0 or 1. Default 
# value is 0 which means the work entries are not recorded in the modification
# availability mbo. Therefore, the person is available if he does not have a 
# calendar and no modavail entries.
#
# PersonGroupTeamMbo contains the useForSite/useForOrg attributes. 
# Normally, these values are not used because a person typically has only one
# calendar. If the person has multiple calendars, the orgID is used to select 
# the calendar to be used to check the availability.
# 
# Need to convert the current time to the person's time zone before checking
# the availability since the calendar entries are in the user's time zone. 
#-----------------------------isPersonAvailable-----------------------------------
def isPersonAvailable(pgtMbo, person):    
    siteID = pgtMbo.getString("USEFORSITE")
    orgID = pgtMbo.getString("USEFORORG")
    
    curDate = getDateInPersonTimeZone(pgtMbo)
    considerBreaks = True
    
    if (hasCalendar(pgtMbo, orgID)):
        available = pgtMbo.isAvailableByCalendar(curDate, orgID, siteID, None, considerBreaks, endOfShiftBuffer)   
        print ticketid + ": isPersonAvailable: pgtMbo.isAvailableByCalendar: person = " + person + " : available = ", available
    else:
        if (useModAvailRecordWorkTime == '1'):
            available = hasWorkModAvailEntry(person, pgtMbo)
            print ticketid + ": isPersonAvailable: hasWorkModAvailEntry: available = ", available  
        else:
            if (hasNonWorkModAvailEntry(person, pgtMbo)):
                print ticketid + ": isPersonAvailable: hasNonWorkModAvailEntry: True" 
                available = False
            else:
                print ticketid + ": isPersonAvailable: hasNonWorkModAvailEntry: False" 
                available = True

    print ticketid + ": isPersonAvailable: person = " + person + " : available = ", available
    return available

#-----------------------------getDateInPersonTimeZone ------------------------
#
# getDateInPersonTimeZone
#
#
# Inputs:
#     pgtMbo
#           - PersonGroupTeam mbo for the person
# Outputs:
#     Returns
#           - date in person's time zone
#
# Description
# Returns the current date in the person's time zone as specified in the person 
# object. If no time zone is specified for the person, the server date is returned.
#-----------------------------------------------------------------------------------
def getDateInPersonTimeZone(pgtMbo):
    currentDate = MXServer.getMXServer().getDate()
    personMboSet = pgtMbo.getMboSet("RESPPARTY_PERSONS")
    personMbo = personMboSet.getMbo(0)

    if (personMbo != None): 
        timeZoneStr = personMbo.getTimezoneStr()
        if (timeZoneStr != None and timeZoneStr != ''):
            print ticketid + ": getDateInPersonTimeZone: Time zone specified = ", timeZoneStr
            tzCal = GregorianCalendar(TimeZone.getTimeZone(timeZoneStr))
            tzCal.setTimeInMillis(currentDate.getTime())
            cal = Calendar.getInstance();
            cal.set(Calendar.YEAR, tzCal.get(Calendar.YEAR));
            cal.set(Calendar.MONTH, tzCal.get(Calendar.MONTH));
            cal.set(Calendar.DAY_OF_MONTH, tzCal.get(Calendar.DAY_OF_MONTH));
            cal.set(Calendar.HOUR_OF_DAY, tzCal.get(Calendar.HOUR_OF_DAY));
            cal.set(Calendar.MINUTE, tzCal.get(Calendar.MINUTE));
            cal.set(Calendar.SECOND, tzCal.get(Calendar.SECOND));
            cal.set(Calendar.MILLISECOND, tzCal.get(Calendar.MILLISECOND));
            currentDate = cal.getTime()
        else:
            print ticketid + ": getDateInPersonTimeZone: No time zone specified. Server time will be used"
    else:
        print ticketid + ": getDateInPersonTimeZone: Unable to get personMbo: returning server date"

    
    print ticketid + ": getDateInPersonTimeZone: Time in person time zone = ", currentDate
    return currentDate
        
#-----------------------------hasCalendar-------------------------------
#
# hasCalendar
#
# Inputs:
#      pgtMbo
#           - PersonGroupTeam mbo for the person
#      orgID
#           - orgID - if this is null, will use the person's primary calendar
#
# Outputs:
#      Returns
#           - True if the person has a calendar associated with
#           - False if the person has no calendar associated with
# 
# Description
# If the orgID is null, it checks for the primary calendar for that person.
# Else, it checks if there is a calendar associated with that person for
# the orgID.
#-----------------------------hasCalendar-------------------------------
def hasCalendar(pgtMbo, orgID):

    personMboSet = pgtMbo.getMboSet("RESPPARTY_PERSONS")
    personMbo = personMboSet.getMbo(0)

    if (personMbo != None):
        personCal = None
        #if orgid is null use the primary calendar
        if (orgID == None or orgID == ""):
            sqf = SqlFormat(userInfo, "personid=:1 and isprimary=:yes")
            sqf.setObject(1, "PERSONCAL", "PERSONID", personMbo.getString("PERSONID"))
            personCalSet = MXServer.getMXServer().getMboSet("PERSONCAL", userInfo)
            personCalSet.setWhere(sqf.format())
            personCal = personCalSet.getMbo(0)
            if (personCal != None):
                print ticketid + ": hasCalendar: The person has primary calendar"
                return True    
        else:
            sqf = SqlFormat(userInfo, "personid=:1 and orgid=:2")
            sqf.setObject(1, "PERSONCAL", "PERSONID", personMbo.getString("PERSONID"));
            sqf.setObject(2, "PERSONCAL", "ORGID", orgID);
            personCalSet = MXServer.getMXServer().getMboSet("PERSONCAL", userInfo)
            personCalSet.setWhere(sqf.format())
            personCal = personCalSet.getMbo(0)
            if (personCal != None):
                print ticketid + ": hasCalendar: The person has a calendar"
                return True

    print ticketid + ": hasCalendar: The person has no calendar"
    return False
#----------------------------hasWorkModAvailEntry----------------------------
#
# hasWorkModAvailEntry
#
# Inputs:
#     person
#           - check this person's mod avail work entry
#     pgtMbo 
#           - PersonGroupTeamMbo for the person           
# Outputs:
#     Returns
#           - True if there is a matching work mod avail entry
#           - False if there are no matching work entries
#          
# Description
# This method calls the hasModAvailEntry method which
# gets the modAvail records for the person and checks if there are any
# entries for the current date. Compares the reason code to see if this is 
# a Work entry. If so, returns True. Else returns False. 
#------------------------------------------------------------------------
def hasWorkModAvailEntry(person, pgtMbo):
    return hasModAvailEntry(person, pgtMbo, "WORK")    
  

#----------------------------hasNonWorkModAvailEntry----------------------------
#
# hasNonWorkModAvailEntry
#
# Inputs:
#     person
#           - check this person's mod avail non work entry
#     pgtMbo 
#           - PersonGroupTeamMbo for the person           
# Outputs:
#     Returns
#           - True if there is a matching non-work mod entry
#           - False if there are no matching non-work entries
#          
# Description
# This method calls the hasModAvailEntry method which
# gets the modAvail records for the person and checks if there are any
# entries for the current date. Compares the reason code to see if this is 
# a Non-work entry. If so, returns True. Else returns False. 
#------------------------------------------------------------------------
def hasNonWorkModAvailEntry(person, pgtMbo):
    return hasModAvailEntry(person, pgtMbo, "NON-WORK")   

#----------------------------hasModAvailEntry----------------------------
#
# hasModAvailEntry
#
# Inputs:
#     person
#           - check this person's mod avail entry
#     pgtMbo 
#           - PersonGroupTeam mbo for the person 
#
#     reason
#           - reason Code (WORK or NON-WORK) to look for in the mod avail 
#             entries 
#          
# Outputs:
#     Returns
#           - True if matching entries found
#           - False if no matching entries found
#          
# Description
# Gets the modAvail records for the person and checks if there are any
# entries for the current date with the reason code specified. The reason 
# codes are: WORK and NON-WORK. Returns True if there is a matching entry
# for the person with the reason code for the current period. Else, returns 
# False. Also, it caches the personid, and the reason code so that 
# it could be used by useAlternate() function later (to optimize the
# performance). Therefore, it first checks for the entry in the cache. 
# If not found in the cache, retrieves from the database and
# stores in the cache. If there is no matching entry - it is still
# cached with a reason code of "NONE" so that we don't need to search for
# this person again in the database for the current execution of the script. 
#-------------------------------------------------------------------------------
def hasModAvailEntry(person, pgtMbo, reason):

    foundEntry = False
    cachedEntry = False

    # Check if the cache contains an entry for this person
    if (person in modAvailCache):
        if (modAvailCache[person] == reason):
            print ticketid + ": hasModAvailEntry: found cache Entry: True"
            foundEntry = True
        else:
            print ticketid + ": hasModAvailEntry: Cache entry did not match the reason code"            
    else:
        # Not found in cache
        curDate = getDateInPersonTimeZone(pgtMbo)        
        availcalc = AvailCalc()
        modAvailSet = getModAvailMboSet(person, curDate)
        
        i = 0
        modAvailMbo = modAvailSet.getMbo(i)        
 
        while (modAvailMbo is not None):            
            startTime = modAvailMbo.getDate("STARTTIME")
            endTime = modAvailMbo.getDate("ENDTIME")
            workDate = modAvailMbo.getDate("WORKDATE")
         
            # concatenate the date and time to get the actual time
            startDateTime = availcalc.getDateTime(workDate, startTime)
            endDateTime = availcalc.getDateTime(workDate, endTime)

            if (curDate > startDateTime) and (curDate < endDateTime):
                print ticketid + ": hasModAvailEntry: Current date is in the range of a modavail entry"
                #check if the modavail is indicating if this is a non-work time or not
                reasonCode = modAvailMbo.getString("reasoncode")
                internalValue = modAvailMbo.getTranslator().toInternalString("RSNCODE", reasonCode)
            
                #add it to the cache
                modAvailCache[person] = internalValue.upper()
                cachedEntry = True
                print ticketid + ": hasModAvailEntry: looking for reason = ", reason
                print ticketid + ": hasModAvailEntry: reason in database = ", internalValue
                if (internalValue.upper() == reason):                               
                    print ticketid + ": hasModAvailEntry: found entry for reason", reason            
                    foundEntry = True
                    break
                
            i = i + 1
            modAvailMbo = modAvailSet.getMbo(i)
            
        # no entry found for this person cache with "NONE" as the 
        # reason code so we don't need to search again 
        if (cachedEntry == False):            
            modAvailCache[person] = "NONE"
            print ticketid + ": hasModAvailEntry: cached entry with NONE reason code"
                  
    print ticketid + ": hasModAvailEntry: foundEntry = ", foundEntry
    return foundEntry

#----------------------------getModAvailMboSet----------------------------
#
# getModAvailMboSet
#
# Inputs:
#     person
#           - person for whom the modification availability set is to be obtained
#     curDate
#           - current date in the person's time zone
#
# Outputs:
#     Returns
#           - mbo set of modification availability entries for the person
#          
# Description
# Returns the list of modification availability entries for the given person  
# for today
#----------------------------------------------------------------------------
def getModAvailMboSet(person, curDate):
    sqf = SqlFormat(userInfo, "WORKDATE=:1 AND PERSONID=:2")
    sqf.setDate(1, curDate)    
    sqf.setObject(2, "MODAVAIL", "PERSONID", person)

    modAvailSet = MXServer.getMXServer().getMboSet("MODAVAIL", userInfo)
    modAvailSet.setWhere(sqf.format())                    
    return modAvailSet 

#-----------------------------useAlternate-------------------------------
#
# useAlternate
#
# Inputs:
#     person
#           - check if alternate can be used
#     pgtMbo
#           - PersonGroupTeam Mbo of the person
#
# Outputs:
#     Returns
#           - True if alternate can be used
#           - False if alternate cannot be used
#
# Description
# The alternates are used only if the primary person has a non-work entry 
# in the modification availability table for the period since they are 
# unavailable. Checks if the modify availability contains a non-work entry 
# for the period. If so, returns True. Else, returns False
#------------------------------------------------------------
def useAlternate(person, pgtMbo):
    useAlternate = False 
 
    useAlternate = hasNonWorkModAvailEntry(person, pgtMbo)                         
    
    print ticketid + ": useAlternate = ", useAlternate    
    return useAlternate 

#-----------------------------noMoreAssignments-------------------------------
#
# noMoreAssignments
#
# Inputs:
#     curOwner
#           - name of the current owner
#     curOwnerGroup
#           - name of the current owner group
#     curOnCallOwnerGroup
#           - name of the current on call owner group
#     curAssignedOwnerGroup
#           - name of the current assigned owner group
#     curUnavailablePrimaryPerson
#           - name of the current primary owner who was unavailable
#     curOnCallFirstRotationAssnPerson
#           - name of the person who was first assigned this ticket from the owner group
# Outputs:
#     Returns
#           - owner, ownergroup, assignedownergroup, unavailableprimaryperson, onCallFirstRotationAssnPerson, reassignTime
#             attributes
#              
#
# Description
# if there is no more person or person group that can be assigned to the ticket, reset the 
# ownerGroup and other attributes to their original values so that the ticket ownership 
# is unchanged. 
#
# Also, this method returns a parameter reassigntime that should be set on the ticket 
# (ONCALLREASSIGNTIME attribute) to a future date (year 3000). Now the ticket will not be 
# processed again by the on call escalation the next time it runs (since the escalation 
# checks the ONCALLREASSIGNTIME attribute to determine the next reassignment time).
# 
# If the ticket needs to be assigned again automatically, set the new owner group  
# on the ticket. This will clear the ONCALLREASSIGNTIME attribute on the ticket
# since the assignment was made manually (not by the on call escalation). 
# If the ONCALLREASSIGNTIME is null, it will be picked up by the escalation. 
#
# This function would be the place to modify the logic to handle
# the case where there are no more owners or ownergroups that can be assigned to the ticket. 
#
#----------------------------------------------------------------------------------
def  noMoreAssignments(curOwner, curOwnerGroup, curOnCallOwnerGroup, curAssignedOwnerGroup, curUnavailablePrimaryPerson, curOnCallFirstRotationAssnPerson):

    owner = curOwner
    ownerGroup = curOwnerGroup
    
    # The onCallOwnerGroup should match OwnerGroup. Otherwise, during save, the 
    # the onCallReassignTime will be reset if they don't match. 
    onCallOwnerGroup = curOwnerGroup
    
    assignedOwnerGroup = curAssignedOwnerGroup    
    unavailablePrimaryPerson = curUnavailablePrimaryPerson
    onCallFirstRotationAssnPerson = curOnCallFirstRotationAssnPerson
    
    # set the ONCALLREASSIGNTIME to Year 3000) 
    cal = Calendar.getInstance()
    cal.set(Calendar.YEAR, 3000)
    cal.set(Calendar.MONTH, 0)
    cal.set(Calendar.DAY_OF_MONTH, 1)
    cal.set(Calendar.HOUR_OF_DAY, 0)
    cal.set(Calendar.MINUTE, 0)
    cal.set(Calendar.SECOND, 0)
    cal.set(Calendar.MILLISECOND, 0)
    onCallReassignTime = cal.getTime()
     
    return owner, ownerGroup, onCallOwnerGroup, assignedOwnerGroup, unavailablePrimaryPerson, onCallFirstRotationAssnPerson, onCallReassignTime      


#-----------------------------calculateOnCallReassignTime-------------------------------
#
# calculateOnCallReassignTime
#
# Inputs:     
#     personGroup
#           - name of the current owner group
#
#     useHistory
#           - boolean indicating if the history should be looked at
#           - to calculate the next reassign time
# Outputs:
#     Returns
#           - the reassignTime for the ticket                         
#
# Description
# This calculates the time at which the next automatic assignment 
# should be made if the current owner does not accept the ticket.
# The reassign time is based on the owner group's on call frequency 
# attribute.
# 
# This method calls getReassignInterval() to get the interval for the
# person group. 
# 
# If the useHistory is False, gets the current time and adds the interval 
# to get the new time for the next reassignment. Else, it gets the last time 
# the owner group was assigned from the history table and adds 
# the interval to that value.
#  
#----------------------------------------------------------------------------------
def calculateOnCallReassignTime(personGroup, useHistory):       
    
    interval = getReassignInterval(personGroup)
    reassignTime = Calendar.getInstance()     

    if (useHistory == True):    
        # get the last modification time from the history table
        historySet = mbo.getMboSet("OWNERHISTORY")             
        sql = "OWNERGROUP=:1 and OWNER is null and rowstamp = (select max(rowstamp) from TKOWNERHISTORY where TICKETID=:2)"
          
        sqf = SqlFormat(userInfo, sql)
        sqf.setObject(1, "TKOWNERHISTORY", "OWNERGROUP", personGroup)
        sqf.setObject(2, "TKOWNERHISTORY", "TICKETID", ticketid)
        historySet.setWhere(sqf.format())
        historySet.reset()                                 
        historyMbo = historySet.getMbo(0)
        if (historyMbo != None):
            ownDate = historyMbo.getDate("OWNDATE")
            reassignTime.setTimeInMillis(ownDate.getTime())             
        else:
            print ticketid + ": calculateOnCallReassignTime: no entry found in tkownerhistory"
              
    reassignTime.add(Calendar.MINUTE, interval)                             
    return reassignTime.getTime()  

#-----------------------------getReassignInterval-------------------------------
#
# getReassignInterval
#
# Inputs:     
#     personGroup
#           - name of the current owner group
#
# Outputs:
#     Returns
#           - the reassign interval for the group               
#
# Description
# This returns the reassign interval time in minutes for automatic assignment 
# for the current personGroup. The reassign interval is the value of the owner 
# group's on call frequency attribute. 
# 
# If the on call frequency is not specified on the group, it defaults to
# 15 minutes. 
# 
#----------------------------------------------------------------------------------
def getReassignInterval(personGroup):       

    interval = 0
    
    personGroupMbo = getPersonGroupMbo(personGroup) 
    if (personGroupMbo != None): 
        interval = personGroupMbo.getInt("ONCALLASSIGNFREQUENCY")    
        
    # default to low frequency interval
    if (interval == 0):
        print ticketid + "getReassignInterval: Defaulting to 15 minutes"
        interval = DEFAULT_REASSIGN_INTERVAL
        
    print ticketid + ": getReassignInterval: interval = ", interval
    
    return interval 

#-----------------------------sendEmail-------------------------------
#
# sendEmail
#
# Inputs:     
#     person
#           - name of the current owner
# 
#     personGroup
#           - name of the current owner group
#               
#
# Description
# This method selects a communication template based on the owner or 
# owner group assignment. If the ticket is assigned to a owner, 
# the communication template to send a  email to the owner is selected. 
# If the owner is null, then the ticket is assigned to a owner group. 
# Therefore, the communication template to send email to the owner 
# group is selected. Then, calls the sendMessage() method on the 
# communication template to send the email.  
#----------------------------------------------------------------------------------
def sendEmail(person, personGroup):
    
    commTemplate = None
    
    # if the person is not null, select the owner template  
    if (person != None):
        commTemplate = "ONCALLASGNOWNINC"        
    else:
        # select the owner group template since the ticket is assigned to the group
        commTemplate = "ONCALLASGNGRPINC"
        
    print ticketid + ": sendEmail: using communication template = ", commTemplate    
        
    commTemplateSet = MXServer.getMXServer().getMboSet("COMMTEMPLATE", userInfo)
    commTemplateSet.setWhere("templateid='" + commTemplate + "'")    
    commTemplateSet.reset()
    
    if (commTemplateSet.isEmpty()):
        print ticketid + ": sendEmail: Unable to get communication template"
    else:
        commTemplateMbo = commTemplateSet.getMbo(0)       
         
        # The role uses the owner or ownergroup value of the ticket in memory to find the 
        # email address. Since the owner and ownergroup are script parameters,
        # they are not in memory until the script is completed.
        # Therefore, set the value on the mbo so that the role can get the new owner/ownergroup
        
        if (person != None):
            mbo.setValue("OWNER", person)
        else:
            mbo.setValue("OWNERGROUP", personGroup)
             
        commTemplateMbo.sendMessage(mbo, None)
             
#----------------------------------MAIN  -----------------------------------
#
# main 
#
# Input:  
#     ticketid
#           - unique ID of the incident. This is printed in all the debug statements
#
#     useModAvailRecordWorkTime 
#           - This variable indicates that people may not have a calendar entry
#             and the work time is to be obtained from the ModAvailMbo.   
#             The value is set to 0 by default. It can be changed to 
#             1 in the Variables tab of the Automation Scripts 
#             application if the ModAvailMbo is to be used to record the work time.
#
#     activeTicketStatus
#          - This variable contains the list of ticket statuses that
#            are to be considered as active status by the workload algorithm
#            to calculate the person with minimum active tickets. By default, 
#            the ticket in status, INPROG, QUEUED are considered as active status.
#            This can be modified in the Variables tab to include other status.             
#  
# Inputs/Outputs:
#     The script reads and modifies the variables. The values are set on the 
#     on the attributes that they are bound to. 
#
#
#     ownerGroup
#           - attribute OWNERGROUP
#
#     owner
#           - attribute OWNER 
#
#     unavailablePrimaryPerson
#           - attribute REPLACEDOWNER
#
#     assignedOwnerGroup
#           - attribute ASSIGNEDOWNERGROUP
#
#     onCallStartTime
#           - attribute ONCALLSTARTTIME. This time corresponds to the time at which the 
#             initial owner was assigned to this ticket by the on call escalation for 
#             the current person group. If the ticket ownership is not claimed and 
#             if it comes back to the queue, the workload algorithm can get the 
#             previous owners for the current owner group using this time.            
#
#     onCallFirstRotationAssnPerson
#           - attribute ONCALLFIRSTROTASSNPERSON. The person who was assigned this ticket 
#             initially by the on call rotation algorithm in the current owner group.
#
# Description
# This automation script is invoked by the action associated with the escalation
# that is assigning owners to the tickets based on the status and the 
# ownerGroup field and the assignment method.
#
# This function checks the on call assignment method specified on the 
# person group to decide if the ownerGroup is configured to assign the group 
# itself as owner group or if the members of the group should be assigned as 
# ticket owners. 
#
# Currently, we support 4 methods: The first 3 methods mentioned below support group member 
# assignment and the last method supports group assignment. 
#
# Set Owner By Sequence: 
# This algorithm assigns the tickets to group members by sequence number, 
# starting with the lowest sequence number.
# For example, if the group contains person1, person2 and person3 as the 
# members of the group with sequence numbers 1, 2 and 3 respectively. 
# This function first assigns person1 as the owner if he is available. 
# If person1 does not claim ownership, person2 is assigned and if person2 does 
# not claim ownership, person3 is assigned. If there are no more persons available,
# it leaves the ticket ownership unchanged.
#
# Set Owner by Rotation:
# This algorithm assigns tickets to group members by rotating the initial 
# assignment among the group members starting with the lowest sequence number.
# For example, if a group contains person1, person2, person3 as the 
# members in the ascending order of sequence numbers, the first new 
# ticket t1 will be assigned to person1 and second new ticket t2 
# will be assigned to person2 and third new ticket t3 will be assigned 
# to person3.
# If the ownership is not claimed and ticket t1 is processed by escalation 
# again, the algorithm assigns it to person2, i.e., the person with the 
# next highest sequence number than the current owner. The rotation is 
# applied to primary group members only.      
# Refer to getNextPersonByRotation() method for more details.
#  
# Set Owner By Workload:
# This algorithm assigns tickets to group members with the fewest 
# number of active tickets. Active tickets include tickets that 
# are in INPROG and QUEUED status. 
# Refer to getNextPersonByWorkload() method for more details
# 
# For all the above 3 methods, a person is considered available if he is 
# available as per the calendar. If there is no calendar, by default, the person is 
# considered available. The modification available records can be used to 
# indicate the unavailability. 
# 
# If they are unavailable, the alternates for that person will be considered. 
# Alternates will be checked only if the person is unavailable  
# as per the modification availability record.
# 
# Set as Owner Group: 
# This method assigns the group to be the ticket owner group.  
# It assigns the ticket to the next group (if any) pointed to by the owner group
#
# If no method is specified, the default is to use Set Owner by Sequence
#------------------------------------------------------------------------------

# The following global variables are used
userInfo = mbo.getUserInfo()

#how long to wait before reassigning a ticket - default is 15 minutes
DEFAULT_REASSIGN_INTERVAL = 15

# cache the personid and reason code in jython dictionary from modAvailEntry  
modAvailCache = { }
# cache person with the active tickets in jython dictionary 
workLoadCache = []
# flag to indicate if the previous new ticket owner is to be set on the person group
setNewTktOwner = False

# save the current owner, assignerOwnerGroup, ownerGroup etc. so that if 
# the current person is the last person and no more person available, 
# we need to set these values back on the mbo. otherwise, they will all be null
curAssignedOwnerGroup = assignedOwnerGroup
curOwner = owner
curOwnerGroup = ownerGroup
curOnCallOwnerGroup = onCallOwnerGroup
curUnavailablePrimaryPerson = unavailablePrimaryPerson
curOnCallStartTime = onCallStartTime
curOnCallFirstRotationAssnPerson = onCallFirstRotationAssnPerson
curOnCallReassignTime = onCallReassignTime


print "################### Parameters ##############################"
print "ticketid = ", ticketid
print "useModAvailRecordWorkTime = ", useModAvailRecordWorkTime
print "assignedOwnerGroup = ", assignedOwnerGroup
print "onCallFirstRotationAssnPerson = ", onCallFirstRotationAssnPerson
print "onCallStartTime = ", onCallStartTime
print "owner = ", owner
print "ownerGroup = ", ownerGroup
print "unavailablePrimaryPerson = ", unavailablePrimaryPerson
print "activeTicketStatus = ", activeTicketStatus
print "onCallOwnerGroup = ", onCallOwnerGroup
print "onCallReassignTime = ", onCallReassignTime
print "################### End of Parameters ##############################"

# check to ensure onCallFirstRotAssnPerson is valid for the group
# this could happen if the ticket was owned and the owner group got modified
# and put back in the queue 
validateOnCallFirstRotAssnPerson = True

while (ownerGroup is not None and len(ownerGroup) > 0):    
    # check if the group is configured to assign group as owner group
    if (isAssignGroupOnly(ownerGroup) == False): 
        # unavailablePrimaryPerson will be null if he himself is a primary. 
        # Only for alternate members, there will be a unavailablePrimaryPerson entry
        onCallAssignMethod = getOnCallAssignMethod(ownerGroup)
        
        if (onCallAssignMethod != None and onCallAssignMethod == 'ONCALL_WORKLOAD'):
            owner, pgtMbo = getNextPersonByWorkload(owner, ownerGroup)
            if (onCallStartTime == None):
                currentDate = MXServer.getMXServer().getDate()
                onCallStartTime = currentDate            
            if (owner != None):
                assignedOwnerGroup = ownerGroup
                break
            else:
                ownerGroup = getNextGroup(ownerGroup)
                # reset onCallStartTime since we are starting with a new group
                onCallStartTime = None
                continue  
        else:
            if (validateOnCallFirstRotAssnPerson):
                if (not isOnCallFirstRotationAssnPersonValid(ownerGroup, owner, onCallFirstRotationAssnPerson)):
                    onCallFirstRotationAssnPerson = None
                validateOnCallFirstRotAssnPerson = False
            if  unavailablePrimaryPerson is None:
                owner, pgtMbo = getNextPrimary(owner, ownerGroup, onCallFirstRotationAssnPerson)                                       
                if owner is None:
                    # go to the next group as there are no more members in this group                
                    ownerGroup = getNextGroup(ownerGroup)
                    if (ownerGroup != None and len(ownerGroup) > 0):
                        onCallFirstRotationAssnPerson = None
                        setNewTktOwner = True
                    # reset the primary owner since we are starting with a new group
                    unavailablePrimaryPerson = None
                    continue
                elif (onCallAssignMethod == 'ONCALL_ROTATION' and onCallFirstRotationAssnPerson == None):
                    onCallFirstRotationAssnPerson = owner
                    setNewTktOwner = True                   
            else:
                # current owner is an alternate. get the next alternate for 
                # the primary member             
                owner, pgtMbo = getNextAlternate(owner, ownerGroup, unavailablePrimaryPerson)
                if owner is None:
                    # no more alternates exist. get the next primary member of the group
                    owner = unavailablePrimaryPerson
                    unavailablePrimaryPerson = None
                    continue
    
            available = isPersonAvailable(pgtMbo, owner)
            if (available): 
                assignedOwnerGroup = ownerGroup
                if (setNewTktOwner == True):                
                    setPrevNewTktOwner(ownerGroup, owner, unavailablePrimaryPerson)            
                break
            else:
                # if the primary member is not available, check for alternates   
                if (unavailablePrimaryPerson is None):
                    # This person is primary member and so check for alternates
                    if (useAlternate(owner, pgtMbo)):
                        unavailablePrimaryPerson = owner
                        owner = None
                        continue    
    else:
        # if the owner group is configured to be assigned as group only,
        # assign the next group only after the reassignInterval time has
        # exceeded since it was originally assigned. When the ticket
        # is first processed by the escalation, the onCallReassignTime is not 
        # set. Therefore, we need to calculate the onCallReassignTime first to avoid
        # reassigning too soon.
        onCallFirstRotationAssnPerson = None
        unavailablePrimaryPerson = None         
        if (onCallReassignTime is None):
            if (owner is None):
                useHistory = True
                onCallReassignTime = calculateOnCallReassignTime(ownerGroup, useHistory)            
                if (onCallReassignTime.after(Calendar.getInstance().getTime())):
                    break            
                else:
                    # clear the onCallReassignTime to calculate later 
                    onCallReassignTime = None
            else:
                # since the owner has a value, the ticket owner/ownergroup values  
                # don't match the algorithm specified on the person group. Therefore 
                # remove the owner and start the timer from the beginning.
                print ticketid + ": main: removing the owner and starting the timer again"                
                owner = None
                break
        if (ownerGroup == curOwnerGroup):
            ownerGroup = getNextGroup(ownerGroup)
            # reset the owner since we are starting with a new group            
            owner = None
            continue
        else:
            break               

# if there is no more person or group that can be assigned to the ticket, leave
# ticket attributes (owner, ownergroup ...) unchanged 
if (len(ownerGroup) == 0):        
    owner, ownerGroup, onCallOwnerGroup, assignedOwnerGroup, unavailablePrimaryPerson, onCallFirstRotationAssnPerson, onCallReassignTime = noMoreAssignments(curOwner, curOwnerGroup, curOnCallOwnerGroup, curAssignedOwnerGroup, curUnavailablePrimaryPerson, curOnCallFirstRotationAssnPerson)
else:
    # set the onCallGroup attribute to indicate that the ownergroup 
    # was assigned by the on call escalation and set the next reassign time    
    onCallOwnerGroup = ownerGroup
    
    # check to see if the onCallReassignTime is already calculated (in the group only case)
    if (curOnCallReassignTime == onCallReassignTime):
        onCallReassignTime = calculateOnCallReassignTime(ownerGroup, False)
        
    # send email to notify the ticket assignment
    try :
        sendEmail(owner, ownerGroup)
    except:
        print ticketid + ": main: Unable to send Email: Exception: ",  sys.exc_info()