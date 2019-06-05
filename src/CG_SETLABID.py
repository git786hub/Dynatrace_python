# AUTOSCRIPT NAME: CG_SETLABID
# CREATEDDATE: 2014-12-18 09:19:13
# CREATEDBY: UVX3
# CHANGEDATE: 2014-12-20 03:04:21
# CHANGEBY: U047
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 
from java.util import Date
from java.lang import String

if interactive:
  sysdate = Date()
  tempdate=sysdate.toString()
  tempyear=tempdate[-2:]
  tempmonth=tempdate[4:-21]
  if tempmonth=="Jan":
    tempmonth="01"
  elif tempmonth== "Feb":
    tempmonth="02"
  elif tempmonth== "Mar":
    tempmonth="03"
  elif tempmonth== "Apr":
    tempmonth="04"
  elif tempmonth== "May":
    tempmonth="05"
  elif tempmonth== "Jun":
    tempmonth="06"
  elif tempmonth== "Jul":
    tempmonth="07"
  elif tempmonth== "Aug":
    tempmonth="08"
  elif tempmonth== "Sep":
    tempmonth="09"
  elif tempmonth== "Oct":
    tempmonth="10"
  elif tempmonth== "Nov":
    tempmonth="11"
  elif tempmonth== "Dec":
    tempmonth="12"

  tedate=tempdate[8:-18]
  temphr=tempdate[11:-15]
  tempmin=tempdate[14:-12]
  tempsec=tempdate[17:-9]
  templabid="M"+tempmonth+tedate+tempyear+temphr+tempmin+tempsec
  if mbo.getString("COMPARTMENT") <> "" and  mbo.getString("COMPARTMENT") is not None : 
    mbo.setValue("LABID", templabid,MboConstants.NOACCESSCHECK)