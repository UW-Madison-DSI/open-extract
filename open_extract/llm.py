import logging

import ollama
from pydantic import BaseModel

from open_extract.data_model import Article


class Extractor:
    def __init__(self, model_name: str, ollama_host: str, target_model: Article):
        self.model_name = model_name
        self.ollama_host = ollama_host
        self.target_model = target_model
        self.ollama_client = ollama.Client(host=ollama_host)

    def format_prompt(self, content: str) -> str:
        return f"Extract data carefully from this academic paper: {content}"

    def run(self, content: str) -> BaseModel:
        messages = [{"role": "user", "content": self.format_prompt(content)}]
        response = self.ollama_client.chat(
            model=self.model_name,
            messages=messages,
            format=self.target_model.model_json_schema(),
        )

        logging.debug(response)
        assert response.message.content is not None
        return self.target_model.model_validate_json(response.message.content)
