from pydantic import BaseModel, Field

class UserRegistration(BaseModel):
    user: str
    password: str

class MemoryLookup(BaseModel):
  LikeText: str

class WikipediaQuery(BaseModel):
  Article: str
  returnLinks: bool
  paragraphSearchTerms: list[str] = Field(..., title="ParagraphSearchTerms", description="Only paragraphs containing one of these phrases will be returned. To get the whole document, leave empty.")

class String(BaseModel):
  ShortTermMemory: list[str] = Field(..., description="A scratchpad for thoughts across the conversation.", max_length=7)
  ResponseText: str

class StringWithStore(BaseModel):
  ShortTermMemory: list[str] = Field(..., description="A scratchpad for thoughts across the conversation.", max_length=7)
  ExcerptsToStore: list[str] = Field(..., description="")
  ResponseText: str

class Response(BaseModel):
  ResponseType: Union[String, MemoryLookup, WikipediaQuery, StringWithStore]
