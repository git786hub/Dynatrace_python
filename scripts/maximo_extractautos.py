import configparser
from cryptography.fernet import Fernet
import base64
import os
import cx_Oracle
import re

config = configparser.ConfigParser()
config.read('../config/PRE/MaximoDBProperties.ini')
DBConfig = config['DataBaseConnection']
user=DBConfig['User']
host=DBConfig['Hostname']
port=DBConfig['Port']
SID=DBConfig['SID']


key = DBConfig['Key'].encode('utf-8')
ciphered_text = DBConfig['CipherPassword'].encode('utf-8')
cipher_suite = Fernet(key)
unciphered_text = (cipher_suite.decrypt(ciphered_text))
pwd = unciphered_text.decode("utf-8")

DBString = user+'/'+pwd+'@'+host+':'+port+'/'+SID
print(DBString)

path=DBConfig['Dir']
print(path)


print(os.path.isdir(path))
if(os.path.isdir(path)==False):	
	try:  
		os.mkdir(path)
	except OSError:  
		print ("Creation of the directory %s failed" % path)
	else:  
		print ("Successfully created the directory %s " % path)

# open db connection and query for automation scripts
try:
	
    SQL="select AUTOSCRIPT, CREATEDDATE, CREATEDBY, CHANGEDATE, CHANGEBY, SCRIPTLANGUAGE, STATUS, SOURCE from MXRADS.autoscript where status in ('Active', 'Draft') order by AUTOSCRIPT"
    print(SQL)
    connection = cx_Oracle.connect(DBString)
		
    cursor = connection.cursor()	
    cursor.execute(SQL)
    print('DB Query executed')
  #  except:
#	    print('Database Error during execution of script')
		
#loop through db results and write to individual files	
    for row in cursor:
        print(str(cursor.rowcount) + ": " + row[0])
  #set extension based on language type
        if row[5]=="jython" or row[5]=="python":
            extension=".py"
        else:
            if row[5]=="javascript" or row[5]=="js":
                extension=".js"
            else:
                extension=".txt"
        print(extension)
        try:
                f = open(path +re.sub('[^A-Za-z0-9_.]+','',row[0])+extension,'w')
                try:
                        f.write('# AUTOSCRIPT NAME: '+row[0]+'\n')
                        f.write('# CREATEDDATE: '+str(row[1])+'\n')
                        f.write('# CREATEDBY: '+row[2]+'\n')
                        f.write('# CHANGEDATE: '+str(row[3])+'\n')
                        f.write('# CHANGEBY: '+row[4]+'\n')
                        f.write('# SCRIPTLANGUAGE: '+row[5]+'\n')
                        f.write('# STATUS: '+row[6]+'\n\n')
                        source = str(row[7])
                        f.write(source)
                finally:
                        f.close()
        except:
            print("IOError")
			
			
#close resources
finally:
    cursor.close()
    connection.close()



