# AUTOSCRIPT NAME: EX2ITEMPARTCATALOG
# CREATEDDATE: 2016-09-01 05:48:02
# CREATEDBY: UXHD
# CHANGEDATE: 2016-10-16 06:10:45
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 

if onadd and launchPoint =='EX2PRCATALOGPART':
	mbo.setValueNull("MANUFACTURER",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("MODELNUM",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("CATALOGCODE",MboConstants.NOACCESSCHECK)
if  launchPoint in ('EX2PRITEMPARTCAT','EX2CONTITEMPARTCAT'):
	mbo.setValueNull("MANUFACTURER",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("MODELNUM",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("CATALOGCODE",MboConstants.NOACCESSCHECK)
	
appli = mbo.getThisMboSet().getParentApp()

if  appli =='PO' and launchPoint =='EX2POCATALOGPART':
	mbo.setValueNull("MANUFACTURER",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("MODELNUM",MboConstants.NOACCESSCHECK)
	mbo.setValueNull("CATALOGCODE",MboConstants.NOACCESSCHECK)