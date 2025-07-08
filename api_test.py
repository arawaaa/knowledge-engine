from openai import OpenAI
import numpy as np
import wikipedia
import os
from dotenv import load_dotenv

from typing import Union, Optional
from enum import Enum
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

models = {"embedding" : "text-embedding-3-small", "llm" : "gpt-4o"}

class Embedder:
  def __init__(self, client: OpenAI, model, encoding_format):
    self.embedding_model = model
    self.fmt = encoding_format
    self.client = client

  def generate(self, inp):
    retd = self.client.embeddings.create(input=inp, encoding_format=self.fmt, model=self.embedding_model)
    return np.array(retd.data[0].embedding)

  def retrieve_similar(emb):
    return

def filterWikipedia(content, terms):
  paras = set()
  paragraphs = content.split("\n")

  for para in paragraphs:
    for term in terms:
      if term in para:
        paras.add(para)

  return paras

class MemoryLookup(BaseModel):
  LikeText: str

class WikipediaQuery(BaseModel):
  Article: str
  returnLinks: bool
  paragraphSearchTerms: list[str] = Field(..., title="ParagraphSearchTerms", description="A list of terms to search paragraphs by; must exactly match some phrase. If empty, the entire document will be returned.")


class Response(BaseModel):
  ResponseType: Union[str, MemoryLookup, WikipediaQuery]

emb_gen = Embedder(client, models["embedding"], "float")

feedback = False
ms = ""
json = None

while (True):
  # single response interactions
  formatT = Response
  try:
    query = input("Msg: ")
    res = client.responses.parse(input = [{"role" : "system", "content" : "You are a chatbot with the ability to respond to user input and look up information using the provided format."},
                                          {"role" : "user", "content" : query}], model = models["llm"], text_format = formatT)
    json = res.output_parsed

  except Exception as e:
    print(e)

  if (isinstance(json.ResponseType, str)):
    print("\033[92m" + json.ResponseType + "\033[00m")

  if (isinstance(json.ResponseType, WikipediaQuery)):
    feedback = True

  tries = 0
  while (feedback && tries < 3):
    if (isinstance(json.ResponseType, WikipediaQuery)):
      searchResults = wikipedia.search(LikeText)
      if (len(searchResults) == 0):
        tries += 1
        client.responses.parse(input)
        formatT = WikipediaQuery
      else:
        wikipedia.page(searchResults[0])


