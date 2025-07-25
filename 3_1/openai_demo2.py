from dotenv import load_dotenv
import os
import weave

from pydantic import BaseModel
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

weave.init("agent-demo2")

client = OpenAI(api_key=api_key)

class Recipe(BaseModel):
    name: str
    servings: int
    ingredients: list[str]
    steps: list[str]


@weave.op()
def get_response(prompt: str) -> Recipe:
    """
    Generates a response from the OpenAI API 
    based on the provided prompt.
    
    Args:
        prompt (str): The input text to generate a response for.
        
    Returns:
        Recipe: A Recipe object containing the generated response.
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        seed=42,
        response_format=Recipe
    )

    return response.choices[0].message.parsed

if __name__ == "__main__":
    user_input = "トマトソースパスタのレシピを教えてください。"
    recipe = get_response(user_input)
    print("Recipe Name: ", recipe.name)
    print("Servings: ", recipe.servings)
    print("Ingredients: ", recipe.ingredients)
    print("Steps: ", recipe.steps)