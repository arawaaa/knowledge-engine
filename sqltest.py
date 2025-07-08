import os
import psycopg

with psycopg.connect("dbname=retrieval user=arawat") as conn:
    with psycopg.cursor()
