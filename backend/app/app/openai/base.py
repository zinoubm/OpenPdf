import os
import logging
import openai


class OpenAiManager:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.organization = os.getenv("OPENAI_ORGANIZATION")

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
            logging.error(f"Sorry, There was a problem \n\n {err}")

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
            logging.error(f"Sorry, There was a problem \n\n {err}")

        return response
    
    def follow_instruction(self, prompt, max_tokens=200, model="gpt-3.5-turbo-instruct"):
        response = None
        try:
            response = (
                openai.Completion.create(
                    model=model,
                    prompt=prompt,
                    temperature=0,
                    max_tokens=max_tokens
                )
                .choices[0]
                .text.strip()
            )

        except Exception as err:
            logging.error(f"Sorry, There was a problem \n\n {err}")

        return response

    def get_chat_completion_stream(self, prompt, model="gpt-3.5-turbo"):
        try:
            for chunk in openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    }
                ],
                stream=True,
            ):
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    yield content

        except Exception as err:
            logging.error(f"Sorry, There was a problem \n\n {err}")

    def get_chat_completion_stream_with_messages(self, messages, model="gpt-3.5-turbo-1106"):
        try:
            for chunk in openai.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=True,
            ):
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    yield content

        except Exception as err:
            logging.error(f"Sorry, There was a problem \n\n {err}")

    def get_embedding(self, prompt, model="text-embedding-ada-002"):
        prompt = prompt.replace("\n", " ")

        embedding = None
        try:
            embedding = openai.Embedding.create(input=[prompt], model=model)["data"][0][
                "embedding"
            ]

        except Exception as err:
            logging.error(f"Sorry, There was a problem {err}")

        return embedding

    def get_embeddings(self, prompts, model="text-embedding-ada-002"):
        prompts = [prompt.replace("\n", " ") for prompt in prompts]

        embeddings = None
        try:
            embeddings = openai.Embedding.create(input=prompts, model=model)["data"]
            return [embedding["embedding"] for embedding in embeddings]

        except Exception as err:
            logging.error(f"Sorry, There was a problem {err}")


openai_manager = OpenAiManager()
