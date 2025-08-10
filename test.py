from pydantic import BaseModel, Field

class Test(BaseModel):
    usr: str
    sec: str

json = '{"usr": "hello", "sec": "sec"}'
print(Test.model_validate_json(json))
