Custom Validators & Serialization Mastery) lo vallu cover chesina key points anni clear ga, neat notes la kinda isthunnanu.

Idi chusi nuvvu direct ga nee notes lo or repository lo save chesukovachu!

🚀 Pydantic: Custom Validators & Serialization Mastery (Lecture Notes)
1. Field-Specific Custom Validators (@validator / @field_validator)
Purpose: Single field meedha specific validation rules (lanti spaces undakudadhu, min length, special chars check cheyyadam) apply cheyadaniki vadatharu.

Key Behavior: Kevalam aa target field ki input vachinappude function run avuthundi.

Important Syntax Note: Validation fail ayithe error trigger cheyyadaniki raise ValueError("...") vaadali, return ValueError kaadu!

Example Code:

Python
from pydantic import BaseModel, validator

class User(BaseModel):
    username: str
    password: str

    @validator('username')
    def check_no_spaces(cls, username):
        if ' ' in username:
            raise ValueError("Username should not contain spaces")
        return username
2. Model-Level Custom Validators (@model_validator)
Purpose: Rendokante ekkuva fields ni (lanti password & confirm_password or start_date & end_date) kalipi motham model meedha validation run cheyyalsi vachinappudu idi vadatharu.

Why self is used? Regular field validator lo single value pass avuthundi, kani model validator lo entire class/object meedha work chesthundi kabatti self (lanti self.start, self.end) use chesi multiple fields ni cross-check cheyochu.

mode='after' meaning: Motham fields ki values successfully assign ayina tharuvatha ee validator execute avuthundi.

Example Code:

Python
from pydantic import BaseModel, model_validator
from datetime import date

class Event(BaseModel):
    name: str
    start: date
    end: date

    @model_validator(mode='after')
    def check_dates(self):
        if self.start > self.end:
            raise ValueError("Start date cannot be after end date")
        return self
3. Serialization (model_dump vs model_dump_json)
Serialization ante Python objects/models ni standard formats (Dictionary or JSON string) loki convert cheyyadam.

model_dump():

Pydantic model ni oka standard Python Dictionary (dict) ga convert chesthundi.

When to use: Local Python code lo internal data manipulation, logic, or debugging kosam.

model_dump_json():

Pydantic model ni oka JSON-formatted String (str) ga convert chesthundi.

When to use: APIs ki data pampalanna, frontend ki transmit cheyyalanna, or file (.json) lo save cheyyalanna.

4. Aliases in Fields (Field(..., alias="..."))
Purpose: Python coding standards snake_case (full_name) lo untayi, kani external APIs or JSON data camelCase (fullName) lo ravochu. Naming mismatch error raakunda handle cheyyadaniki alias vadatharu.

How it works: Input lo alias name (fullName) teesukuni python variable (full_name) ki map chesthundi. Output lo malli by_alias=True isthe alias format loki convert chesthundi.

Example Code:

Python
from pydantic import BaseModel, Field

class Employee(BaseModel):
    full_name: str = Field(..., alias="fullName")

    class Config:
        populate_by_name = True
5. Private Attributes (PrivateAttr)
Purpose: Model lo sensitive data (lanti internal tokens, hashed passwords) ni secure ga daachukodaniki vadatharu.

Important Rule: Ivi user nundi direct ga input ga raavu (ValidationError vasthundi). Object create chesaka internal methods dwara assign cheyyali.

Example Code:

Python
from pydantic import BaseModel, PrivateAttr

class SecureUser(BaseModel):
    username: str
    _password: str = PrivateAttr()  # Private attribute

    def set_password(self, pwd: str):
        self._password = pwd

    def get_password(self):
        return self._password


from pydantic import BaseModel, Field, model_validator

## Prastice for ModelValidation in Pydantic 
class UserSignup(BaseModel):
    username: str
    password: str = Field(..., min_length=6)
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserSignup":
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm Password do not match!")
        return self


if __name__ == "__main__":
    try:
        user = UserSignup(
            username="hemanth",
            password="secretpassword",
            confirm_password="secretpassword",
        )
        print("Success:", user.model_dump())

        invalid_user = UserSignup(
            username="hemanth",
            password="password123",
            confirm_password="wrongpassword",
        )
    except ValueError as e:
        print("\nValidation Error Caught:")
        print(e)