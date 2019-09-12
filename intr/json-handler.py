# -*- coding: utf-8 -*-
import mysql.connector
import os
import json
import time
import rediswq

def get_db_connection():
    try:
        print ("Establishing db connection : " + db_host + ", " + db_user + "/" + "*******")
        connection = mysql.connector.connect(user=db_user,
                                             password=db_pass,
                                             host=db_host,
                                             port=db_port,
                                             database=db_name)
        print ("Connected to : " + db_name)
        return connection
    except mysql.connector.Error as err:
        raise err


def close_connection(connection):
    connection.close()


def insert_db_data(insert_query):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
    except mysql.connector.Error as e:
        print ("ERROR: DB Exception : " + str(e))
    else:
        cursor.execute(insert_query)

        connection.commit()
        print ("INFO: Added : "+insert_query)
    finally:
        cursor.close()
        close_connection(connection)

def inject_data():
    count = json_dict.get("count")
    text = json_dict.get("text").replace("'", r"\'")
    topics = json_dict.get("topics")
    player = json_dict.get("player")
    flags = json_dict.get("flags")
    client_id = json_dict.get("client_id")
    filtered = json_dict.get("filtered")
    simplified = json_dict.get("simplified").replace("'", r"\'")
    


    insert_message = "INSERT INTO `txtmessage` VALUES ('"+str(count)+"'," \
                                                         " '"+text+"'," \
                                                         " '"+player+"'," \
                                                         " '"+str(flags)+"'," \
                                                         " '"+str(client_id)+"'," \
                                                         " '"+str(filtered)+"'," \
                                                         "'"+simplified+"')"
    insert_db_data(insert_message)

    for topic in topics:
        _topic = topic.get("topic")
        relevance = topic.get("relevance")
        confidence = topic.get("confidence")

        insert_topic = "INSERT INTO `topics` VALUES ('"+str(client_id)+"'," \
                                                            " '"+str(simplified)+"'," \
                                                            " '"+str(_topic)+"'," \
                                                            " '"+str(confidence)+"'," \
                                                            "'"+str(relevance)+"')"
    insert_db_data(insert_topic)



# Main
host="redis"
q = rediswq.RedisWQ(name="job", host="redis")

# Each pod will pull a task (file name in the nfs server) and will execute until redis is empty
while not q.empty():
  item = q.lease(lease_secs=10, block=True, timeout=2) 
  if item is not None:
    # itemstr is the a chunk of the main data.json after the split
    itemstr = item.decode("utf-8")
    print("Working on chunk" + itemstr)
    
    # Path to the file on the mounted volume
    json_path = '/opt/' + itemstr
    db_host = os.environ['db_host']
    db_port = os.environ['db_port']
    db_user = os.environ['db_user']
    db_pass = os.environ['db_pass']
    db_name = os.environ['db_name']

    datafile = open(json_path, "r")
    # For each line in the file load the json and inject into the database
    for line in datafile:
        
        # read from the json file
        json_dict = json.loads(line)
        
        # insert json into db
        inject_data()

    datafile.close()

    q.complete(item)
  else:
    print("Waiting for work")



