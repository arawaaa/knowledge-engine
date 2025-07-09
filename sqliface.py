import os
import psycopg

conn = psycopg.connect("dbname=retrieval user=arawat")
cursor = conn.cursor()

# Database schema contained in *.sql
# Currently a table of embeddings and related text, intention is to
# also encode textual relationships ("is a member of", "caused by") and temporal data

def get():
    cursor.execute("select * from embeds;")
    for entry in cursor:
        print(entry)
