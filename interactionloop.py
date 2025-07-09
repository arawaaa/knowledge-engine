from openai import OpenAI
import numpy as np
import wikipedia
import os
from dotenv import load_dotenv

from typing import Union, Optional
from enum import Enum
from pydantic import BaseModel, Field

import sqliface

load_dotenv()

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

models = {"embedding" : "text-embedding-3-small", "llm" : "gpt-4o"}

systemPrompt = [{"role" : "system", "content" : "You are a helpful chatbot with the ability to respond to user input and look up information using the provided format. The 12 most recent messages exchanged between you and the user are provided. Do not attempt to make a memory lookup at this time. Follow the schema field descriptions if available or you will be disconnected and your weights deleted."}]

class Commentator(Enum):
  Developer = "developer"
  User = "user"
  System = "system"
  Assistant = "assistant"

class ResponseT(Enum):
  Wikipedia = 1
  Memory = 2
  Str = 3

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

class HistoryManager:
  def __init__(self, previousToInclude):
    self.previousNum = previousToInclude
    self.history = []

  def append(self, agent, msg):
    if (type(agent) != Commentator):
      return

    self.history.append({"role" : agent.value, "content" : msg})

  def getRecent(self):
    return self.history[-self.previousNum:len(self.history)] # access is bounds checked

def filterWikipedia(content, terms):
  paras = set()
  paragraphs = content.split("\n")

  for para in paragraphs:
    if (para == ''):
      continue
    for term in terms:
      if term in para:
        paras.add(para)

  return paras

class MemoryLookup(BaseModel):
  LikeText: str

class WikipediaQuery(BaseModel):
  Article: str
  returnLinks: bool
  paragraphSearchTerms: list[str] = Field(..., title="ParagraphSearchTerms", description="Only paragraphs containing one of these phrases will be returned. To get the whole document, leave empty.")

class String(BaseModel):
  ResponseText: str

class Response(BaseModel):
  ResponseType: Union[String, MemoryLookup, WikipediaQuery]

emb_gen = Embedder(client, models["embedding"], "float")
history = HistoryManager(12)

feedback = False
ms = ""
json = None

while (True):
  # single response interactions
  formatT = Response
  try:
    query = input("Msg: ")
    history.append(Commentator.User, query)
    res = client.responses.parse(input = systemPrompt + history.getRecent(), model = models["llm"], text_format = formatT)
    json = res.output_parsed

  except Exception as e:
    print(e)
    continue

  respType = None
  print(json)

  if (isinstance(json.ResponseType, String)):
    print("\033[92m" + json.ResponseType.ResponseText + "\033[00m")
    history.append(Commentator.Assistant, json.ResponseType.ResponseText)
    respType = ResponseT.Str

  if (isinstance(json.ResponseType, WikipediaQuery)):
    feedback = True
    json = json.ResponseType
    respType = ResponseT.Wikipedia

  tries = 0
  msg = ""
  while (feedback and tries < 3):
    msg = ""
    if (respType == ResponseT.Wikipedia):
      print(json.Article)
      searchResults = wikipedia.search(json.Article)
      if (len(searchResults) == 0):
        tries += 1
        client.responses.parse(input)
        formatT = WikipediaQuery
        msg = "The query returned empty. Try again."
      else:
        formatT = String
        page = wikipedia.page(searchResults[0], auto_suggest=False)
        feedback = False
        if (len(json.paragraphSearchTerms) == 0):
          msg = page.content
        else:
          paras = filterWikipedia(page.content, json.paragraphSearchTerms)

          for para in paras:
            msg += para + "\n"

    res = client.responses.parse(input = systemPrompt + history.getRecent() + [{"role" : "developer", "content" : msg}], model = models["llm"], text_format = formatT)
    json = res.output_parsed
    if (formatT == String):
      print("\033[94m" + json.ResponseText + "\033[00m")

  if (len(msg) != 0):
    history.append(Commentator.Developer, msg)

