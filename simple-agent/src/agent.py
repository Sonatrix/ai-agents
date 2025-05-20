import os
from openai import OpenAI

# Initialize the OpenAI client with Ollama's endpoint


class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []

        client = OpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key='ollama'  # Required but unused
        )
        self.client = client

        if system:
            self.messages.append({"role": "system", "content": system})

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

    def get_system(self):
        return self.system
    
    def __call__(self, message):
        self.add_message("user", message)
        result = self.execute()
        self.add_message("assistant", result)
        return result

    def execute(self):
        response = self.client.chat.completions.create(
            model=os.getenv('MODEL_NAME'),
            messages=self.messages
        )
        return response.choices[0].message.content