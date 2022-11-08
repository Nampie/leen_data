import pandas as pd
import mysql.connector

table = 'agc_table'
db = 'ot_data'
file_all_data = "exported_sql_data_rev2.csv"

cnx = mysql.connector.connect(user='leen',password='leen',host='127.0.0.1',database=db)
cursor = cnx.cursor()

query_cmd = "SELECT * FROM "

for result in cursor.execute(query_cmd + table, multi=True):
    if result.with_rows:
        raw_result = result.fetchall()
        print("Rows produced by statement '{}':".format(
            result.statement))
        print(raw_result)
    else:
        print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))
            

# sql_query = pd.read_sql_query(query_cmd + table, cnx)

data_frame = pd.DataFrame(raw_result, columns=["id", "time", "gen2val", "gen3val",
                                               "ACE_part_for_gen2", "ACE_part_for_gen3",
                                               "set_point_for_gen2", "set_point_for_gen3"])
print(data_frame)
data_frame.to_csv(file_all_data, index=False)
cnx.close()
