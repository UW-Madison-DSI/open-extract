from pydantic import BaseModel
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
    study_independent_variables: list[str]
    study_dependent_variables: list[str]
    data_points: list[DataPoint]

    def save(self, path: Path | None = None):
        if not path:
            path = Path(f"data/jsons/{self.title}.json")
        with open(path, "w") as f:
            f.write(self.model_dump_json(indent=4))


class ArticleV2(BaseModel):
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
