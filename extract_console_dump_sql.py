#print('HEllo World')

# extract output from console

# read line from console:

# check the logic first char starts with '['

# read that line

# split by ' : '

# connect with the sql server (link sent)

# dump data to he database: ot_data

# within ot_data database , push data to the agc_table

import subprocess, datetime
import mysql.connector

table = 'agc_table'
db = 'pythonlogin'

cnx = mysql.connector.connect(user='leen',password='leen',host='127.0.0.1',database=db)
cursor = cnx.cursor()

cursor.execute("TRUNCATE TABLE agc_table")

cmd = "python3 /home/vboxuser/Desktop/pydnp3/examples/pydnp3_master.py 1 10.19.144.2"

p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
counter = 0
first_time = True

insert_stmt = (
   "INSERT INTO agc_table (id, time, gen2, gen3, ACEgen2, ACEgen3, spGen2, spGen3)"
   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
)
index_db = 1
#sql connector
items=[]

items_new = []
bias = -5
ACE_Gen3 = 0
ACE_Gen2 = 0

def AGC_setpoint(gen, ACE, part):
	AGC_setpoint = gen - 2*ACE*part
	return AGC_setpoint

for line in iter(p.stdout.readline, b''):
	line = line.decode('utf-8')
	#print(line)
	if line[0] == '[':
		value = line.split(' : ') #splits list by the :
		#print(value)
		if len(value) > 3:
			value_float = float(value[1]) #obtains second val needed
			#print(value_float)
			items.append(value_float)
			#print(line)
		counter = counter + 1
		
	if first_time and counter == 9:
		now = datetime.datetime.now()
		print('Date and Time:')
		print(str(now))
		counter = 0
		first_time = False
		
		initial_tie_flow_gen3 = items[2]+items[3] #initial vals set here only
		nominal_freq_bus3 = items[1] #initial vals set here only
		ACE_Gen3 = (items[1] - nominal_freq_bus3)*10*bias + (items[2]+items[3] - initial_tie_flow_gen3) 
		initial_tie_flow_gen2 = items[6]+items[7]
		nominal_freq_bus2 = items[5]
		ACE_Gen2 = (items[5] - nominal_freq_bus2)*10*bias + (items[6]+items[7] - initial_tie_flow_gen2)
		AGC_Gen3 = AGC_setpoint(items[0],ACE_Gen3,1)
		AGC_Gen2 = AGC_setpoint(items[4],ACE_Gen2,1)
		items_new = [items[4], items[0], ACE_Gen2, ACE_Gen3, AGC_Gen2, AGC_Gen3]
		items = []
		print(items_new)
		
		data_to_insert = tuple([index_db])+tuple([now.strftime('%H:%M:%S')])+tuple(items_new)
		
		# insert first row into the database
		cursor.execute(insert_stmt, data_to_insert)
		cnx.commit()
		items=[]
		index_db+=1
	
	if counter == 8 and not first_time:
		now = datetime.datetime.now()
		print('Date and Time:')
		print(str(now))
		counter = 0
		
		nominal_freq_bus3 = items[1]
		ACE_Gen3 = (items[1] - nominal_freq_bus3)*10*bias + (items[2]+items[3] - initial_tie_flow_gen3) 
		#initial_tie_flow_gen2 = items[6]+items[7]
		nominal_freq_bus2 = items[5]
		ACE_Gen2 = (items[5] - nominal_freq_bus2)*10*bias + (items[6]+items[7] - initial_tie_flow_gen2)
		AGC_Gen3 = AGC_setpoint(items[0],ACE_Gen3,1)
		AGC_Gen2 = AGC_setpoint(items[4],ACE_Gen2,1)
		items_new = [items[4], items[0], ACE_Gen2, ACE_Gen3, AGC_Gen2, AGC_Gen3]
		items = []
		print(items_new)
		
		data_to_insert = tuple([index_db])+tuple([now.strftime('%H:%M:%S')])+tuple(items_new)
		cursor.execute(insert_stmt, data_to_insert)
		cnx.commit()
		items=[]
		index_db+=1
		# insert further rows into the databse
		
p.stdout.close()
p.wait()



		
		


                
