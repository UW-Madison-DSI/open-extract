import logging

import ollama
from pydantic import BaseModel

QUESTIONS = {
    "Q1": "How do different seed treatments (insecticide and fungicide) impact soybean yield when planted before May 1 compared to after May 1?",
    "Q2": "What is the effectiveness of foliar fungicide applications in controlling white mold and improving soybean yield in fields where white mold is a primary concern?",
    "Q3": "How does the application of foliar fungicide at the R3 growth stage for general disease control affect soybean yield compared to other growth stages?",
    "Q4": "Which row-spacing and seeding rate combinations are most effective in maximizing soybean yield in the North Central U.S. and how do these compare to the mid-south and southern U.S.?",
    "Q5": "What environmental and planting date conditions best support the effectiveness of insecticidal and fungicide seed treatments in protecting soybean yield?",
    "Q6": "How do no-till practices influence insect and slug pest pressures and soybean yield in different regions?",
    "Q7": "What are the primary factors that predict foliar and root diseases in soybeans across various U.S. regions and how do these factors interact with pest management practices?",
    "Q8": "How does the presence of cover crops affect weed emergence, insect pest pressures, and overall soybean yield?",
    "Q9": "What are the long-term trends in soybean yield improvement associated with changes in planting dates, row spacing, tillage practices, and other agronomic inputs?",
    "Q10": "Which pest management strategies (e.g., seed treatments, scouting-based treatments) are most consistent in protecting soybean yield under varying environmental and biotic conditions?",
}


class OLLAMAExtractor:
    def __init__(
        self, model_name: str, ollama_host: str, target_model: type[BaseModel]
    ):
        self.model_name = model_name
        self.ollama_host = ollama_host
        self.target_model = target_model
        self.ollama_client = ollama.Client(host=ollama_host)

    def run(self, content: str) -> BaseModel:
        system_message = {
            "role": "system",
            "content": "You are a research assistant specializing in agriculture, your role is to extract data from academic papers and provide accurate answers based on their findings.",
        }
        user_message = {"role": "user", "content": content}
        messages = [system_message, user_message]
        response = self.ollama_client.chat(
            model=self.model_name,
            messages=messages,
            format=self.target_model.model_json_schema(),
        )

        logging.debug(response)
        assert response.message.content is not None
        return self.target_model.model_validate_json(response.message.content)


def keep_alive(
    model: str, host: str | None = None, duration: int = -1
) -> ollama.ChatResponse:
    """Keep the model in memeory for a duration explicitly."""
    return ollama.Client(host=host).chat(model=model, keep_alive=duration)
