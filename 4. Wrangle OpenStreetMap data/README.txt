I. Files in this repo.

0. data/ - All data needed for processing and the intermediate data files generated. https://s3.amazonaws.com/metro-extracts.mapzen.com/bengaluru_india.osm.bz2 (Download from the link and save it as ‘bengaluru_india.osm’)

1. a_audit_data.py — Audit the data.
2. b_create_tags.py - Creates and counts tags.
3. c_create_schema.py - Just a schema structure to init Database.
4. d_a_init_db.py - Converts the XML data into SQLlite readable.
5. d_b_create_db.py - Uses sqlite to create a DB.
6. e_query_data.py - Query using sqlite3 to view desired results.



II. Usage :

1. Open terminal or CMD

2. Execute following commands 

$ python3 a_audit_data.py
$ python3 b_create_tags.py
$ python3 c_create_schema.py 
$ python3 d_a_init_db.py
$ python3 d_b_create_db.py
$ python3 e_query_data.py
