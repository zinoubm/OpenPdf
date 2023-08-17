import os

# from dotenv import load_dotenv
import openai


class OpenAiManager:
    def __init__(self):
        # load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_completion(
        self,
        prompt,
        model="text-davinci-003",
        max_tokens=128,
        temperature=0,
    ):
        response = None
        try:
            response = openai.Completion.create(
                prompt=prompt,
                max_tokens=max_tokens,
                model=model,
                temperature=temperature,
            )["choices"][0]["text"]

        except Exception as err:
            print(f"Sorry, There was a problem \n\n {err}")

        return response

    def get_chat_completion(self, prompt, model="gpt-3.5-turbo"):
        response = None
        try:
            response = (
                openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": prompt,
                        }
                    ],
                )
                .choices[0]
                .message.content.strip()
            )

        except Exception as err:
            print(f"Sorry, There was a problem \n\n {err}")

        return response

    def get_embedding(self, prompt, model="text-embedding-ada-002"):
        prompt = prompt.replace("\n", " ")

        embedding = None
        try:
            embedding = openai.Embedding.create(input=[prompt], model=model)["data"][0][
                "embedding"
            ]

        except Exception as err:
            print(f"Sorry, There was a problem {err}")

        return embedding

    def get_embeddings(self, prompts, model="text-embedding-ada-002"):
        prompts = [prompt.replace("\n", " ") for prompt in prompts]

        embeddings = None
        try:
            embeddings = openai.Embedding.create(input=prompts, model=model)["data"]

        except Exception as err:
            print(f"Sorry, There was a problem {err}")

        return [embedding["embedding"] for embedding in embeddings]


openai_manager = OpenAiManager()
