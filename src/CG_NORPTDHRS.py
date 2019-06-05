# AUTOSCRIPT NAME: CG_NORPTDHRS
# CREATEDDATE: 2012-03-26 14:05:21
# CREATEDBY: UHD0
# CHANGEDATE: 2013-02-01 08:04:19
# CHANGEBY: UM7V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants

def setError(g, k):
    global errorkey, errorgroup, params
    errorgroup = g
    errorkey = k

if app in ["LABREPTRN", "WOT_TRN", None]:

    if launchPoint == "CG_NORPTDHRS":
        isNegHrs = mbo.getBoolean("CG_NEGATIVEHRS")
        if premiumpayhours is not None and premiumpayhours < 0 and not isNegHrs:
            setError("LABREPTRN", "negativehours")
        elif premiumpayhours is not None and premiumpayhours > 24:
            setError("labreptrn", "greaterThan24Hrs")
    elif launchPoint == "CG_LABTOOLHRS":
        if toolhrs is not None and toolhrs > 24:
            setError("labreptrn", "greaterThan24Hrs")

    mHours = None
    mFieldName = None
    if launchPoint == "CG_NORPTDHRS":
        mHours = premiumpayhours
        mFieldName = "PREMIUMPAYHOURS"
    elif launchPoint == "CG_LABTOOLHRS":
        mHours = toolhrs
        mFieldName = "TOOLHRS"

    if mHours is not None and mFieldName is not None:
        remainder = abs(mHours) % 0.25
        sign = 1
        if mHours < 0:
            sign = -1
        if remainder > 0:
            mbo.setValue(mFieldName, (abs(mHours) + 0.25 - remainder) * sign, MboConstants.NOACCESSCHECK)
        else:
            mbo.setValue(mFieldName, (abs(mHours) - remainder) * sign, MboConstants.NOACCESSCHECK)