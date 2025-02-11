from pydantic import BaseModel, Field
from pathlib import Path


class DataPoint(BaseModel):
    year: int
    location: str
    planting_date: str
    harvest_date: str
    crop_is_soybean: bool
    crop_yield: float
    crop_yield_units: str
    treatment: str
    seed_maturity: str
    protein_and_oil_content_description: str


class Article(BaseModel):
    title: str
    authors: list[str]
    publication_date: str
    publication_name: str
    publication_doi: str
    methodology_summary: str
    key_findings: str
    insights_on_the_effect_of_plant_date_on_soybean_yield: str
    study_independent_variables: list[str]
    study_dependent_variables: list[str]
    data_points: list[DataPoint]

    def save(self, path: Path | None = None):
        if not path:
            path = Path(f"data/jsons/{self.title}.json")
        with open(path, "w") as f:
            f.write(self.model_dump_json(indent=4))


class Screening(BaseModel):
    """This model is used to screen articles for further extraction."""

    title: str
    authors: list[str]
    publication_date: str
    publication_year: int
    publication_name: str
    publication_doi: str
    study_within_us: bool = Field(..., description="Was the study conducted in the US")
    study_location: str = Field(..., description="Location of the study conducted")
    is_soybean_study: bool = Field(..., description="Was the study about soybean?")
    has_yield_data: bool = Field(..., description="Whether the study has yield data")


class QA(BaseModel):
    """This model is used to store the question and answer pairs with additional context."""

    question: str = Field(..., description="The question that I am trying to answer")
    study_is_answering_question: bool = Field(
        ...,
        description="Whether the study has useful information to answer the question",
    )
    useful_information_summary: str = Field(
        ..., description="A summary of the useful information for the question"
    )
    supporting_data: str = Field(
        ..., description="The data that supports answering the question"
    )
    answer: str = Field(..., description="The answer to the question")
    confidence: int = Field(
        ...,
        description="Confidence in the answer (0-5), 0 being the lowest and 5 being the highest",
    )
