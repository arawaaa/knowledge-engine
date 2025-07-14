from openai import OpenAI

import os
import psycopg
import numpy as np
from pgvector.psycopg import register_vector

class Embedder:
  def __init__(self, client: OpenAI, model, encoding_format):
    self.embedding_model = model
    self.fmt = encoding_format
    self.client = client

  def generate(self, inp):
    retd = self.client.embeddings.create(input=inp, encoding_format=self.fmt, model=self.embedding_model)
    embeddings = []
    for embed in retd.data:
        embeddings.append(embed)
    return embeddings

  def retrieve_similar(emb):
    return sql.get(emb)

conn = psycopg.connect("dbname=retrieval user=arawat")
register_vector(conn)
cursor = conn.cursor()

# Database schema contained in *.sql
# Currently a table of embeddings and related text, intention is to
# also encode textual relationships ("is a member of", "caused by") and temporal data

def get(vec):
    cursor.execute("""
        select description, (embed <#> %s) * -1 as cosine_score
        from embeds
        where cosine_score > 0.85
        order by cosine_score desc
        limit 6;""", (vec,)) # inner product is cosine distance since |e| = 1
    matches = ""
    for desc, _ in cursor:
        matches += desc + '\n\n'
    return matches

def put(emb, strings):
    valuePairs = []
    for elem in emb.generate(strings):
        valuePairs.append((elem,strings))

    cursor.execute("""
        insert into embeds
        values %s
        """, (valuePairs,))

