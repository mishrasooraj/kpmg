from app.core.config import Settings


class EmbeddingService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def embed_text(self, text: str) -> list[float] | None:
        if not self.settings.openai_api_key:
            return None

        from langchain_openai import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        return await embeddings.aembed_query(text)
