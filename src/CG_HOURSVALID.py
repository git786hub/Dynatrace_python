# AUTOSCRIPT NAME: CG_HOURSVALID
# CREATEDDATE: 2012-07-07 10:38:23
# CREATEDBY: UHD0
# CHANGEDATE: 2013-04-01 00:45:34
# CHANGEBY: UM1R
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, k):
    global errorkey, errorgroup, params
    errorgroup = g
    errorkey = k

site = mbo.getString("SITEID")

noerrgen = True

if mHours is not None and site == "TRN" :

    if launchPoint in  ["CG_HOURSVALID"] :
       if mHours > 12 :
	   setError("labreptrn","cannotExceed8Hrs")

    if launchPoint in  ["CG_HOURSVALID","CG_LABPRHRS"] :	   
       reghours = mbo.getDouble("REGULARHRS")
       premhours = mbo.getDouble("PREMIUMPAYHOURS")
       sumofhrs = reghours + premhours
       if sumofhrs > 24 :
            setError("labreptrn","totalHrsCannotExceed24")
            
    if mHours < 0 and noerrgen and not mbo.getBoolean("CG_NEGATIVEHRS") :
        setError("labreptrn", "noNegativeHrs")
        noerrgen = False

    remainder = abs(mHours) % 0.25
    sign = 1

    if mHours < 0:
        sign = -1
    if remainder > 0:
        mHours = (abs(mHours) + 0.25 - remainder) * sign
    else:
        mHours = (abs(mHours) - remainder) * sign