from openai import OpenAI
import numpy as np
import wikipedia
import os
from dotenv import load_dotenv
from flask import Flask, request

from typing import Union, Optional
from enum import Enum
from pydantic import BaseModel, Field

import sqliface as sql
import pydantic_defs as pyd

load_dotenv()

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

models = {"embedding" : "text-embedding-3-small", "llm" : "gpt-4o"}

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def handleLogin():
  if (request.method == "POST" and request.is_json() and request.content_length < 500):
    datum = request.get_data()
    regObj = pyd.UserRegistration.model_validate_json(datum)



class Commentator(Enum):
  Developer = "developer"
  User = "user"
  System = "system"
  Assistant = "assistant"

class ResponseT(Enum):
  Wikipedia = 1
  Memory = 2
  Str = 3

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

def getPreamble(stwm):
  systemPrompt = [
      {"role" : "system", "content" : "You are a helpful chatbot with the ability to respond to user input and look up information using the provided format. The 12 most recent messages exchanged between you and the user are provided. Follow the schema field descriptions if available or you will be disconnected and your weights deleted."},
      {"role" : "system", "content" : "Recent thoughts" + "\n".join(stwm)}]
  return systemPrompt

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

emb_gen = Embedder(client, models["embedding"], "float")
history = HistoryManager(12)

feedback = False
ms = ""
json = None
stwm = []

while (True):
  # single response interactions
  formatT = Response
  try:
    query = input("Msg: ")
    history.append(Commentator.User, query)
    res = client.responses.parse(input = getPreamble(stwm) + history.getRecent(), model = models["llm"], text_format = formatT)
    json = res.output_parsed

  except Exception as e:
    print(e)
    continue

  respType = None
  print(json)

  if (isinstance(json.ResponseType, String)):
    print("\033[92m" + json.ResponseType.ResponseText + "\033[00m")
    history.append(Commentator.Assistant, json.ResponseType.ResponseText)
    stwm = json.ResponseType.ShortTermMemory
    respType = ResponseT.Str

  if (isinstance(json.ResponseType, WikipediaQuery)):
    feedback = True
    history.append(Commentator.Developer, "The assistant began a wikipedia lookup.")
    respType = ResponseT.Wikipedia

  if (isinstance(json.ResponseType, MemoryLookup)):
    feedback = True
    history.append(Commentator.Developer, "The assistant began a memory lookup.")
    respType = ResponseT.Memory

  json = json.Response

  tries = 0
  msg = ""
  while (feedback and tries < 3):
    msg = ""
    if (respType == ResponseT.Wikipedia):
      searchResults = wikipedia.search(json.Article)
      if (len(searchResults) == 0):
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

    if (respType == ResponseT.Memory):
      vec = emb_gen.generate(json.LikeText)
      similar_results = emb_gen.retrieve_similar(vec)
      if (len(similar_results) == 0):
        msg = "Try a different search phrase"
        formatT = MemoryLookup
      else:
        msg = "Here are your results:\n" + emb_gen.retrieve_similar(vec)
        feedback = False
        formatT = String

    res = client.responses.parse(input = getPreamble(stwm) + history.getRecent() + [{"role" : "developer", "content" : msg}], model = models["llm"], text_format = formatT)
    json = res.output_parsed
    if (formatT == String):
      print("\033[92m" + json.ResponseText + "\033[00m")

    tries += 1

  if (feedback):
    history.append(Commentator.Developer, "You were unable to perform the previous action. Try to respond as best as possible to the user or state that you don't have the requisite details.")
    res = client.responses.parse(input = getPreamble(stwm) + history.getRecent(), text_format=String)
    json = res.output_parsed
    stwm = json.ShortTermMemory
    print("\033[92m" + json.ResponseText + "\033[00m")
    history.append(Commentator.Assistant, json.ResponseText)

