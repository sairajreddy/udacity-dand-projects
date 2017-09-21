import csv, sqlite3

connection = sqlite3.connect("data/bengaluru_india.db")
connection.text_factory = str
cursor = connection.cursor()

cursor.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open('data/bi_nodes.csv','r') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i["id"], i["lat"], i["lon"], i["user"], i["uid"], i["version"], i["changeset"], i["timestamp"]) \
             for i in dr]

cursor.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
connection.commit()


cursor.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open('data/bi_nodes_tags.csv','r') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cursor.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
connection.commit()


cursor.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open('data/bi_ways.csv','r') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cursor.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
connection.commit()


cursor.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open('data/bi_ways_nodes.csv','r') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cursor.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
connection.commit()


cursor.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open('data/bi_ways_tags.csv','r') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]


cursor.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
connection.commit()