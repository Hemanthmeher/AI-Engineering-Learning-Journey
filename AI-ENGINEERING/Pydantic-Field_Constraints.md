
# 🚀 Pydantic `Field()` Constraints, Patterns & Validation Notes

Today, I learned how to supercharge Pydantic models using the `Field()` function in Python. Instead of basic data types, `Field()` gives us absolute control over validation, metadata, and data constraints.

Here is my complete, hands-on understanding of what I studied today!

---

## 1. Why do we need `Field()` in Pydantic?
Normally, when we define a Pydantic model, we specify types like `name: str` or `age: int`. But what if we want to enforce rules like:
* "Name length must be at least 3 characters."
* "Age must be 18 or above."
* "Email must follow a strict regex pattern."
* "Provide a clean description and example for API documentation (like FastAPI Swagger UI)."

This is exactly where `Field()` comes into play! It acts as a wrapper to add constraints and metadata to model attributes.

---

## 2. Deep Dive: String Patterns (`pattern` parameter)
One of the most powerful features I explored is using regular expressions (`pattern`) inside `Field()` to validate specific string formats.

### Example: Email Validation Pattern
```python
email: str = Field(
    ...,
    pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
)
Breaking down each part of this Regex:
^ (Caret): Enforces that the string validation must start right from the very first character.

[\w\.-]+ (Username part):

\w means word characters (alphabets a-z, A-Z, 0-9, and underscore _).

\. and - allow dots and hyphens.

+ means it must appear at least one or more times before the @ symbol (e.g., hemanth.meher).

@ (At symbol): The mandatory @ separator in every email address.

[\w\.-]+ (Domain name part): Validates the mail server provider name (e.g., gmail, yahoo).

\. (Escaped Dot): In regex, a plain dot (.) means "any character". To match a literal dot (like the one before com or in), we use a backslash escape: \..

\w+ (Top-Level Domain extension): Matches the final domain suffix like com, in, or org.

$ (Dollar sign): The end anchor. It ensures that the string strictly terminates right after the extension. No extra trailing characters, spaces, or junk text are allowed at the end!

3. Metadata & Documentation: description & examples
When building APIs (especially with FastAPI), data models need to be self-documenting. Pydantic allows us to attach metadata directly inside Field():

description: Explains what the field actually represents (displayed automatically in Swagger UI documentation).

examples: Provides a sample value to show users or clients what valid input looks like.

Code Implementation:
Python
from typing import Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    sku: str = Field(
        ...,
        pattern=r"^[A-Z]{3}-\d{4}$",
        description="Stock Keeping Unit code for inventory tracking.",
        examples=["ELE-1234"]
    )
    price: float = Field(
        ...,
        gt=0,
        description="The retail price of the item. Must be greater than 0.",
        examples=[499.99]
    )