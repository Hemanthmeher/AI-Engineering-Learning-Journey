# Section 23: Pydantic Nested Models — Deep Validation Like a Pro

## Overview & Core Concepts

When building real-world AI applications (like RAG pipelines, structured output parsers, and multi-turn agents), data is rarely flat. We deal with nested hierarchies—such as a user having multiple posts, and each post having multiple comments.

Instead of writing custom validation code for each level, Pydantic handles hierarchical data natively using **Nested Models**.

When you define a Pydantic model inside another model using type annotations, Pydantic automatically performs recursive validation across the entire data tree down to the primitive fields.

---

## 1. Why Use Nested Models?

- **Clean Structure:** Organizes complex schemas logically into modular sub-models.
- **Recursive Validation:** Validates parent data and all nested child objects simultaneously.
- **Detailed Error Pathing:** If validation fails deep inside a nested structure, Pydantic points directly to the exact error location (`posts -> 0 -> comments -> 0 -> likes`).
- **Easy Serialization:** Converts the entire nested tree into dictionaries or JSON strings instantly.

---

## 2. Defining Nested Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Comment(BaseModel):
    text: str
    likes: int = Field(default=0, ge=0)

class Post(BaseModel):
    title: str
    content: str
    comments: List[Comment] = Field(default_factory=list)

class UserProfile(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    posts: List[Post] = Field(default_factory=list)


## 3. Instantiating and Validating Data

You can pass nested raw dictionaries directly into the main model, and Pydantic will automatically coerce them into their respective model instances.

```python
raw_data = {
    "username": "Rohan",
    "email": "rohan@example.com",
    "posts": [
        {
            "title": "Why Pydantic Rocks",
            "content": "Seriously it does",
            "comments": [
                {
                    "text": "Great Post",
                    "likes": 5
                },
                {
                    "text": "Very Helpful",
                    "likes": 3
                }
            ]
        }
    ]
}

user = UserProfile(**raw_data)

print(type(user.posts[0]))
print(type(user.posts[0].comments[0]))

## 4. Exporting Nested Models

To serialize your nested models back into dictionaries or JSON strings for databases or APIs, use `.model_dump()` or `.model_dump_json()`.

### Export to Dictionary
```python
user_dict = user.model_dump()
print(user_dict)