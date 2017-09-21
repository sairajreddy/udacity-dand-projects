import csv
import sqlite3

#Calculates the total number of nodes
def total_nodes():
	result = cur.execute('SELECT COUNT(*) FROM nodes')
	return result.fetchone()[0]

#Calculates total number of unique users
def total_unique_users():
	result = cur.execute('SELECT COUNT(DISTINCT(allusers.uid)) \
            FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) allusers')
	return result.fetchone()[0]

#Calculates total number of ways
def total_ways():
	result = cur.execute('SELECT COUNT(*) FROM ways')
	return result.fetchone()[0]


#My own implementation of the largest leisure club data
def biggest_leisure_club():
	for row in cur.execute('SELECT value, COUNT(*) as num \
	        FROM nodes_tags \
	        WHERE key="leisure" \
	        GROUP BY value \
	        ORDER BY num DESC \
	        LIMIT 10'):
   		 return row

#The most contributing users 
def top_most_contributing_users():
	users = []
	for row in cur.execute('SELECT allusers.user, COUNT(*) as num \
            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) allusers \
            GROUP BY allusers.user \
            ORDER BY num DESC \
            LIMIT 10'):
		users.append(row)
	return users


#The main function
if __name__ == '__main__':
	
	con = sqlite3.connect("data/bengaluru_india.db")
	cur = con.cursor()
	
	print("The largest leisure club :- " , biggest_leisure_club())
	print("Total number of nodes are :- " , total_nodes())
	print("Total number of ways are :- " , total_ways())
	print("Total number of unique users :- " , total_unique_users())
	print("The top most contributing users :- " , top_most_contributing_users())

    