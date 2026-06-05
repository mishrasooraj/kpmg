from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import DocumentEmbedding


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        source_uri: str,
        content: str,
        metadata: dict,
        embedding: list[float] | None,
    ) -> DocumentEmbedding:
        document = DocumentEmbedding(
            source_uri=source_uri,
            content=content,
            metadata_json=metadata,
            embedding=embedding,
        )
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document
