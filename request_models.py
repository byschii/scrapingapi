import pydantic

class ScrapeRequest(pydantic.BaseModel):
    url: str
    max_wait: int = 30

