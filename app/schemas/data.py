from pydantic import BaseModel, Field


class PipelineRunRequest(BaseModel):
    pipeline_name: str = Field(min_length=1)
    source_uri: str = Field(min_length=1)
    target_uri: str = Field(min_length=1)
    parameters: dict = Field(default_factory=dict)


class PipelineRunResponse(BaseModel):
    run_id: str
    status: str
    activities: list[str]


class DocumentIngestRequest(BaseModel):
    source_uri: str
    content: str = Field(min_length=1)
    metadata: dict = Field(default_factory=dict)


class DocumentIngestResponse(BaseModel):
    document_id: str
    embedded: bool
