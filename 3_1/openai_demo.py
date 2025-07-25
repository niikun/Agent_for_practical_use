import os
from dotenv import load_dotenv
import weave

from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

weave.init("agent-demo")

client = OpenAI(api_key=api_key)

@weave.op()
def get_response(prompt:str)->str:
    """
    Generates a response from the OpenAI API 
    based on the provided prompt.
    Args:
        prompt (str): The input text to generate a response for.
    Returns:
        str: The generated response from the OpenAI API.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user",
             "content": prompt}
        ],
        temperature=0.0,
        seed=42,
    )
    answer = response.choices[0].message.content.strip()
    tokens_used = response.usage
    return answer, tokens_used

if __name__=="__main__":
    user_input = "こんにちは。今日はどんな天気ですか？"
    ans,tokens = get_response(user_input)
    print("Answer: ", ans)
    print("Tokens used: ", tokens)




