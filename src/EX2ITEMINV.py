# AUTOSCRIPT NAME: EX2ITEMINV
# CREATEDDATE: 2017-11-30 04:21:26
# CREATEDBY: U3LO
# CHANGEDATE: 2018-10-11 06:39:11
# CHANGEBY: U3LO
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, e, p):
        global errorgroup, errorkey, params
        errorgroup = g
        errorkey = e
        params= p

if (launchPoint in ('EX2POITEMINV','EX2ITEMINVITEM','EX2POITEMSTORELOCINV','EX2ITEMINV') and interactive):
  invset=mbo.getMboSet('INVENTORY')
  iteminv=invset.getMbo(0)
  item=mbo.getString('ITEMNUM')
  storeloc=mbo.getString('STORELOC')
  linetype=mbo.getString('LINETYPE')
  if (storeloc !='' and linetype=='ITEM' and item !=''):
    if(iteminv is None):
      setError("EX2ITEMINV","noninventoryitem", [item, storeloc])

if (launchPoint=='EX2ITEMINVCHKPR'):
  initStatus = mbo.getMboValue("STATUS").getInitialValue().asString()
  currStatus=mbo.getString("STATUS")
  if  ((onupdate and (initStatus in ["WAPPR","BWAPPR","HOLD","IWAPPR","RWAPPR"] or currStatus in ["APPR"]) and interactive) or (not interactive and currStatus in ["WAPPR"]) ) :
    prlineset=mbo.getMboSet('PRLINE') 
    prline1=''
    i=0
    count=prlineset.count()
    if (prlineset is not None ):
      for i in range(count):
	prline=prlineset.getMbo(i)
        prlinenum=prline.getInt('PRLINENUM')
        prlineiteminvcheck =prline.getMboSet('INVENTORY')
	if (prline.getString('ITEMNUM') !='' and prline.getString('STORELOC') !='' and prline.getString('LINETYPE') =='ITEM' and not prline.toBeDeleted()):
	  if (prlineiteminvcheck.count()==0):
	    if (prline1==''):
	      prline1 = str(prlinenum)
            else:
              prline1 = prline1 + ", " + str(prlinenum)
    if (prline1 !=''):
      setError('EX2ITEMINV','prnoninventoryitem',[prline1])

if (launchPoint=='EX2ITEMINVCHCKPO'):
  initStatus = mbo.getMboValue("STATUS").getInitialValue().asString()
  currStatus=mbo.getString("STATUS")
  if  ((onupdate and (initStatus in ["PNDREV","BUPEND","WAPPR","BUREJ","REVIEW","REVREJ"] ) and interactive) or (not interactive and currStatus in ["WAPPR"]) ) :
    polineset=mbo.getMboSet('POLINE')
    poline1=''
    i=0
    count=polineset.count()
    if(polineset is not None ):
      for i in range(count):
        poline=polineset.getMbo(i)
        polinenum=poline.getInt('POLINENUM')
        polineiteminv=poline.getMboSet('INVENTORY')
        if (poline.getString('ITEMNUM') !='' and poline.getString('STORELOC') !='' and poline.getString('LINETYPE')=='ITEM' and not poline.toBeDeleted()):
            if(polineiteminv.count()==0):
              if(poline1==''):
                poline1=str(polinenum)
              else:
                poline1=poline1 + ", " + str(polinenum)
    if (poline1 !=''):
      setError('EX2ITEMINV','pononinventoryitem',[poline1])