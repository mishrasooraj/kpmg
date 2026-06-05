from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.data_engineering.azure_workflows import AzureDataWorkflowService
from app.db.session import get_db
from app.repositories.documents import DocumentRepository
from app.schemas.data import (
    DocumentIngestRequest,
    DocumentIngestResponse,
    PipelineRunRequest,
    PipelineRunResponse,
)
from app.services.embeddings import EmbeddingService

router = APIRouter(prefix="/data", tags=["data-engineering"])


@router.post("/pipelines/run", response_model=PipelineRunResponse)
async def run_pipeline(
    request: PipelineRunRequest,
    settings: Settings = Depends(get_settings),
) -> PipelineRunResponse:
    run = await AzureDataWorkflowService(settings).trigger_pipeline(
        request.pipeline_name,
        request.source_uri,
        request.target_uri,
        request.parameters,
    )
    return PipelineRunResponse(
        run_id=run["run_id"],
        status=run["status"],
        activities=run["activities"],
    )


@router.post("/documents/ingest", response_model=DocumentIngestResponse)
async def ingest_document(
    request: DocumentIngestRequest,
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> DocumentIngestResponse:
    embedding = await EmbeddingService(settings).embed_text(request.content)
    document = await DocumentRepository(session).create(
        request.source_uri,
        request.content,
        request.metadata,
        embedding,
    )
    return DocumentIngestResponse(document_id=str(document.id), embedded=embedding is not None)
