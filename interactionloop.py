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
    if (regObj)

