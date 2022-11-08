import mysql.connector
import pandas as pd

cnx = mysql.connector.connect(
    user = 'root',
    password = 'rootpass',
    host = '127.0.0.1',
    database = 'pythonlogin',
    auth_plugin='mysql_native_password'
)
print(cnx)

my_cursor = cnx.cursor(buffered=True)
print('Creating table....')
my_cursor.execute("DROP TABLE IF EXISTS test_substation;")
my_cursor.execute("CREATE TABLE IF NOT EXISTS test_substation("
    # "id INT AUTO_INCREMENT PRIMARY KEY,"
    "time TIME,"
    "gen2Val FLOAT,"
    "gen3val FLOAT,"
    "ACE_part_for_gen2 FLOAT,"
    "ACE_part_for_gen3 FLOAT,"
    "set_point_for_gen2 FLOAT,"
    "set_point_for_gen3 FLOAT);")
print('table substaion created')
my_cursor.execute("SELECT * FROM substation")

data = pd.read_csv('dummy_AGC_data.csv')

for i,row in data.iterrows():
    sql = "INSERT INTO pythonlogin.test_substation VALUES (%s,%s,%s,%s,%s,%s,%s)"
    my_cursor.execute(sql, tuple(row))
    print("Record inserted")
    cnx.commit()


