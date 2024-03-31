
#pakages
import os
import pandas as pd
import numpy as np
import json
import mysql.connector as sql


mydb=sql.connect(host="localhost",user="root",password="root",database= "phonepe_pulse",port = "3306")
cursor=mydb.cursor()

#aggre_transaction
def aggre_trans():
    path = "C:/Users/raji/guvi/pulse/data/aggregated/transaction/country/india/state/"

    agg_tran_list = os.listdir(path)

    agg_trans ={"States":[], "Year":[], "Quarter":[], "Transaction_type":[], "Transaction_count":[],"Transaction_amount":[] }

    for state in agg_tran_list:
        cur_states =path+state+"/"
        agg_year_list = os.listdir(cur_states)

        for year in agg_year_list:
            cur_years = cur_states+year+"/"
            agg_file_list = os.listdir(cur_years)

            for file in agg_file_list:
                cur_files = cur_years+file
                data = open(cur_files,"r")
                trans = json.load(data)

                for i in trans["data"]["transactionData"]:
                    name = i["name"]
                    count = i["paymentInstruments"][0]["count"]
                    amount = i["paymentInstruments"][0]["amount"]
                    agg_trans["Transaction_type"].append(name)
                    agg_trans["Transaction_count"].append(count)
                    agg_trans["Transaction_amount"].append(amount)
                    agg_trans["States"].append(state)
                    agg_trans["Year"].append(year)
                    agg_trans["Quarter"].append(int(file.strip(".json")))

    aggregated_transaction = pd.DataFrame(agg_trans)

    aggregated_transaction["States"] = aggregated_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    aggregated_transaction["States"] = aggregated_transaction["States"].str.replace("-"," ")
    aggregated_transaction["States"] = aggregated_transaction["States"].str.title()
    aggregated_transaction['States'] = aggregated_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return aggregated_transaction

a_t=aggre_trans()  # calling function

#aggre trans table
def agg_trans_table():
    cursor.execute("""
                    CREATE TABLE if not exists aggregated_transaction (States varchar(100),Year int,Quarter int,Transaction_type varchar(100),
                    Transaction_count bigint,Transaction_amount bigint)""")
    cursor.execute("""SELECT COUNT(*) FROM aggregated_transaction """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False
    for index,row in a_t.iterrows():
        cursor.execute("""
                        INSERT INTO aggregated_transaction (States, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
                                                            values(%s,%s,%s,%s,%s,%s)""",

                (row["States"],row["Year"],row["Quarter"],row["Transaction_type"],row["Transaction_count"],row["Transaction_amount"]))

    mydb.commit()

agg_trans_table()  #calling table name

#aggre_user
def aggre_user():
    path2 = "C:/Users/raji/guvi/pulse/data/aggregated/user/country/india/state/"

    agg_user_list = os.listdir(path2)

    agg_user = {"States":[], "Year":[], "Quarter":[], "Brands":[],"Transaction_count":[], "Percentage":[]}

    for state in agg_user_list:
        curr_states = path2+state+"/"
        aggr_year_list = os.listdir(curr_states)

        for year in aggr_year_list:
            curr_years = curr_states+year+"/"
            agg_fileu_list = os.listdir(curr_years)

            for file in agg_fileu_list:
                curr_files = curr_years+file
                data1 = open(curr_files,"r")
                auser = json.load(data1)

                try:

                    for j in auser["data"]["usersByDevice"]:
                        brand = j["brand"]
                        count = j["count"]
                        percentage = j["percentage"]
                        agg_user["Brands"].append(brand)
                        agg_user["Transaction_count"].append(count)
                        agg_user["Percentage"].append(percentage)
                        agg_user["States"].append(state)
                        agg_user["Year"].append(year)
                        agg_user["Quarter"].append(int(file.strip(".json")))

                except:
                    pass

    aggregated_user = pd.DataFrame(agg_user)

    aggregated_user["States"] = aggregated_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    aggregated_user["States"] = aggregated_user["States"].str.replace("-"," ")
    aggregated_user["States"] = aggregated_user["States"].str.title()
    aggregated_user['States'] = aggregated_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return aggregated_user

a_u=aggre_user() #calling function

# aggre user table
def agg_user_table():
    cursor.execute("""
                    CREATE TABLE if not exists aggregated_user (States varchar(100),Year int,Quarter int,Brands varchar(100),
                    Transaction_count bigint,Percentage float)""")
    cursor.execute("""SELECT COUNT(*) FROM aggregated_user """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False
    for index,row1 in a_u.iterrows():
        cursor.execute("""
                        INSERT INTO aggregated_user (States, Year, Quarter, Brands, Transaction_count, Percentage)
                                                            values(%s,%s,%s,%s,%s,%s)""",

                (row1["States"],row1["Year"],row1["Quarter"],row1["Brands"],row1["Transaction_count"],row1["Percentage"]))

    mydb.commit()

agg_user_table()  #calling table name

#map_transaction
def map_trans():
    path3 = "C:/Users/raji/guvi/pulse/data/map/transaction/hover/country/india/state/"
    map_tran_list = os.listdir(path3)

    map_t = {"States":[], "Year":[], "Quarter":[],"District":[], "Transaction_count":[],"Transaction_amount":[]}

    for state in map_tran_list:
        map_states = path3+state+"/"
        map_year_list = os.listdir(map_states)

        for year in map_year_list:
            map_years = map_states+year+"/"
            map_file_list = os.listdir(map_years)

            for file in map_file_list:
                map_files = map_years+file
                data2 = open(map_files,"r")
                tran_map = json.load(data2)

                for i in tran_map['data']["hoverDataList"]:
                    name = i["name"]
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]
                    map_t["District"].append(name)
                    map_t["Transaction_count"].append(count)
                    map_t["Transaction_amount"].append(amount)
                    map_t["States"].append(state)
                    map_t["Year"].append(year)
                    map_t["Quarter"].append(int(file.strip(".json")))

    map_transaction = pd.DataFrame(map_t)

    map_transaction["States"] = map_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    map_transaction["States"] = map_transaction["States"].str.replace("-"," ")
    map_transaction["States"] = map_transaction["States"].str.title()
    map_transaction['States'] = map_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return map_transaction

m_t=map_trans()  #calling fuction

#map trans table
def map_trans_table():
    cursor.execute("""
                    CREATE TABLE if not exists map_transaction (States varchar(100),Year int,Quarter int,District varchar(100),
                    Transaction_count bigint,Transaction_amount float)""")
    cursor.execute("""SELECT COUNT(*) FROM map_transaction """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False
    for index,row2 in m_t.iterrows():
        cursor.execute("""
                        INSERT INTO map_transaction (States, Year, Quarter, District, Transaction_count, Transaction_amount)
                                                            values(%s,%s,%s,%s,%s,%s)""",

                (row2["States"],row2["Year"],row2["Quarter"],row2["District"],row2["Transaction_count"],row2["Transaction_amount"]))

    mydb.commit()

map_trans_table()   #calling fuction

#map_user
def map_users():
    path4 = "C:/Users/raji/guvi/pulse/data/map/user/hover/country/india/state/"
    map_user_list = os.listdir(path4)

    map_u = {"States":[], "Year":[], "Quarter":[], "Districts":[], "RegisteredUser":[], "AppOpens":[]}

    for state in map_user_list:
        map_user_states = path4+state+"/"
        mapu_year_list = os.listdir(map_user_states)

        for year in mapu_year_list:
            map_user_years = map_user_states+year+"/"
            mapu_file_list = os.listdir(map_user_years)

            for file in mapu_file_list:
                map_user_files = map_user_years+file
                data3 = open(map_user_files,"r")
                user_map = json.load(data3)

                for i in user_map["data"]["hoverData"].items():
                    district = i[0]
                    registereduser = i[1]["registeredUsers"]
                    appopens = i[1]["appOpens"]
                    map_u["Districts"].append(district)
                    map_u["RegisteredUser"].append(registereduser)
                    map_u["AppOpens"].append(appopens)
                    map_u["States"].append(state)
                    map_u["Year"].append(year)
                    map_u["Quarter"].append(int(file.strip(".json")))

    map_user = pd.DataFrame(map_u)

    map_user["States"] = map_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    map_user["States"] = map_user["States"].str.replace("-"," ")
    map_user["States"] = map_user["States"].str.title()
    map_user['States'] = map_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return map_user

m_u=map_users()    #calling fuction

# map user table
def map_user_table():
    cursor.execute("""
                    CREATE TABLE if not exists map_user (States varchar(100),Year int,Quarter int,Districts varchar(100),
                    RegisteredUser bigint,AppOpens bigint)""")
    cursor.execute("""SELECT COUNT(*) FROM map_user """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False
    for index,row3 in m_u.iterrows():
        cursor.execute("""
                        INSERT INTO map_user (States, Year, Quarter, Districts, RegisteredUser, AppOpens)
                                                            values(%s,%s,%s,%s,%s,%s)""",

                (row3["States"],row3["Year"],row3["Quarter"],row3["Districts"],row3["RegisteredUser"],row3["AppOpens"]))

    mydb.commit()

map_user_table()   #calling fuction

#top_transaction_district
def top_dist_trans():
    path5 = "C:/Users/raji/guvi/pulse/data/top/transaction/country/india/state/"
    top_tran_list = os.listdir(path5)

    top_d_tran = {"States":[], "Year":[], "Quarter":[], "District":[] ,"District_transaction_count":[],"District_transaction_amount":[]}


    for state in top_tran_list:
        top_trans_states = path5+state+"/"
        top_year_list = os.listdir(top_trans_states)

        for year in top_year_list:
            top_trans_years = top_trans_states+year+"/"
            top_file_list = os.listdir(top_trans_years)

            for file in top_file_list:
                top_trans_files = top_trans_years+file
                data = open(top_trans_files,"r")
                dist_trans = json.load(data)

                for i in dist_trans["data"]["districts"]:
                    district = i["entityName"]
                    district_count = i["metric"]["count"]
                    district_amount = i["metric"]["amount"]
                    top_d_tran["District"].append(district)
                    top_d_tran["District_transaction_count"].append(district_count)
                    top_d_tran["District_transaction_amount"].append(district_amount)
                    top_d_tran["States"].append(state)
                    top_d_tran["Year"].append(year)
                    top_d_tran["Quarter"].append(int(file.strip(".json")))


    top_district_transaction = pd.DataFrame(top_d_tran)

    top_district_transaction["States"] = top_district_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    top_district_transaction["States"] = top_district_transaction["States"].str.replace("-"," ")
    top_district_transaction["States"] = top_district_transaction["States"].str.title()
    top_district_transaction['States'] = top_district_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return top_district_transaction

dist_trans=top_dist_trans()   #calling fuction

# top trans district table
def top_trans_dist_table():
    cursor.execute("""
                    CREATE TABLE if not exists top_transaction_district (States varchar(100),Year int,Quarter int,District varchar(100),
                    District_transaction_count bigint,District_transaction_amount bigint)""")
    cursor.execute("""SELECT COUNT(*) FROM top_transaction_district """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False

    for index,row3 in dist_trans.iterrows():

        cursor.execute("""
                        INSERT INTO top_transaction_district (States, Year, Quarter, District, District_transaction_count, District_transaction_amount)
                                                            values(%s,%s,%s,%s,%s,%s)""",

                (row3["States"],row3["Year"],row3["Quarter"],row3["District"],row3['District_transaction_count'],row3['District_transaction_amount']))

    mydb.commit()

top_trans_dist_table()    #calling fuction

#top_transaction_pincodes
def top_pin_trans():
    path5 = "C:/Users/raji/guvi/pulse/data/top/transaction/country/india/state/"
    top_tran_list = os.listdir(path5)

    tran_pin =  {"States":[], "Year":[], "Quarter":[] ,"Pincodes":[], "Pincode_transaction_count":[], "Pincode_transaction_amount":[]}

    for state in top_tran_list:
        top_trans_states = path5+state+"/"
        top_year_list = os.listdir(top_trans_states)

        for year in top_year_list:
            top_trans_years = top_trans_states+year+"/"
            top_file_list = os.listdir(top_trans_years)

            for file in top_file_list:
                top_trans_files = top_trans_years+file
                data = open(top_trans_files,"r")
                pin_trans = json.load(data)

                for j in pin_trans["data"]["pincodes"]:
                    pincodes=j["entityName"]
                    pincode_count=j["metric"]["count"]
                    pincode_amount=j["metric"]["amount"]
                    tran_pin["Pincodes"].append(pincodes)
                    tran_pin["Pincode_transaction_count"].append(pincode_count)
                    tran_pin["Pincode_transaction_amount"].append(pincode_amount)
                    tran_pin["States"].append(state)
                    tran_pin["Year"].append(year)
                    tran_pin["Quarter"].append(int(file.strip(".json")))

    top_pincodes_transaction = pd.DataFrame(tran_pin)

    top_pincodes_transaction["States"] = top_pincodes_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    top_pincodes_transaction["States"] = top_pincodes_transaction["States"].str.replace("-"," ")
    top_pincodes_transaction["States"] = top_pincodes_transaction["States"].str.title()
    top_pincodes_transaction['States'] = top_pincodes_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return top_pincodes_transaction

pin_trans=top_pin_trans()   #calling fuction

# top trans pincode table
def top_trans_pin_table():
    cursor.execute("""
                    CREATE TABLE if not exists top_transaction_pincode (States varchar(100),Year int,Quarter int,Pincodes int,Pincode_transaction_count bigint,
                    Pincode_transaction_amount bigint)""")
    cursor.execute("""SELECT COUNT(*) FROM top_transaction_pincode """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False

    for index,row3 in pin_trans.iterrows():

        cursor.execute("""
                        INSERT INTO top_transaction_pincode (States, Year, Quarter,Pincodes,
                        Pincode_transaction_count,Pincode_transaction_amount)
                                                            values(%s,%s,%s,%s,%s,%s)""",

                (row3["States"],row3["Year"],row3["Quarter"],row3['Pincodes'],row3['Pincode_transaction_count'],row3['Pincode_transaction_amount']))

    mydb.commit()

top_trans_pin_table()   #calling fuction


#top_user_district
def dist_user():
    path6 = "C:/Users/raji/guvi/pulse/data/top/user/country/india/state/"
    top_user_list = os.listdir(path6)

    user_dist = {"States":[], "Year":[], "Quarter":[], "District":[], "District_registereduser":[]}

    for state in top_user_list:
        top_user_states = path6+state+"/"
        top_year_list = os.listdir(top_user_states)

        for year in top_year_list:
            top_user_years = top_user_states+year+"/"
            top_file_list = os.listdir(top_user_years)

            for file in top_file_list:
                top_user_files = top_user_years+file
                data = open(top_user_files,"r")
                dist_user = json.load(data)

                for i in dist_user["data"]["districts"]:
                    name = i["name"]
                    registeredusers = i["registeredUsers"]
                    user_dist["District"].append(name)
                    user_dist["District_registereduser"].append(registeredusers)
                    user_dist["States"].append(state)
                    user_dist["Year"].append(year)
                    user_dist["Quarter"].append(int(file.strip(".json")))

    top_district_user = pd.DataFrame(user_dist)

    top_district_user["States"] = top_district_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    top_district_user["States"] = top_district_user["States"].str.replace("-"," ")
    top_district_user["States"] = top_district_user["States"].str.title()
    top_district_user['States'] = top_district_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return top_district_user

dis=dist_user()   #calling fuction

# top user district table
def top_user_dist_table():
    cursor.execute("""
                    CREATE TABLE if not exists top_user_district (States varchar(100),Year int,Quarter int,District varchar(100),
                    District_registereduser bigint)""")
    cursor.execute("""SELECT COUNT(*) FROM top_user_district """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False

    for index,row4 in dis.iterrows():

        cursor.execute("""
                        INSERT INTO top_user_district (States, Year, Quarter, District,District_registereduser)
                                                            values(%s,%s,%s,%s,%s)""",

                (row4["States"],row4["Year"],row4["Quarter"],row4["District"],row4['District_registereduser']))

    mydb.commit()

top_user_dist_table()   #calling fuction


#top_user_pincode
def pin_user():
    path6 = "C:/Users/raji/guvi/pulse/data/top/user/country/india/state/"
    top_user_list = os.listdir(path6)

    user_pin = {"States":[], "Year":[], "Quarter":[], "Pincodes":[], "Pincode_registereduser":[]}

    for state in top_user_list:
        top_user_states = path6+state+"/"
        top_year_list = os.listdir(top_user_states)

        for year in top_year_list:
            top_user_years = top_user_states+year+"/"
            top_file_list = os.listdir(top_user_years)

            for file in top_file_list:
                top_user_files = top_user_years+file
                data = open(top_user_files,"r")
                pin_user = json.load(data)

                for j in pin_user["data"]["pincodes"]:
                    name = j["name"]
                    registeredusers = j["registeredUsers"]
                    user_pin["Pincodes"].append(name)
                    user_pin["Pincode_registereduser"].append(registeredusers)
                    user_pin["States"].append(state)
                    user_pin["Year"].append(year)
                    user_pin["Quarter"].append(int(file.strip(".json")))

    top_pincode_user = pd.DataFrame(user_pin)

    top_pincode_user["States"] = top_pincode_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    top_pincode_user["States"] = top_pincode_user["States"].str.replace("-"," ")
    top_pincode_user["States"] = top_pincode_user["States"].str.title()
    top_pincode_user['States'] = top_pincode_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    return top_pincode_user

pin=pin_user()   #calling fuction

#top user pincode table
def top_user_pin_table():
    cursor.execute("""
                    CREATE TABLE if not exists top_user_pincode (States varchar(100),Year int,Quarter int,Pincodes int,Pincode_registereduser bigint)""")
    cursor.execute("""SELECT COUNT(*) FROM top_user_pincode """)
    count = cursor.fetchone()[0]
    if count > 0:
        return False

    for index,row4 in pin.iterrows():

        cursor.execute("""
                        INSERT INTO top_user_pincode (States, Year, Quarter,Pincodes,Pincode_registereduser)
                                                            values(%s,%s,%s,%s,%s)""",

                (row4["States"],row4["Year"],row4["Quarter"],row4['Pincodes'],row4['Pincode_registereduser']))

    mydb.commit()

top_user_pin_table()   #calling fuction


