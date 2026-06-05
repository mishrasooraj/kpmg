from uuid import uuid4

from app.core.config import Settings


class AzureDataWorkflowService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def trigger_pipeline(
        self,
        pipeline_name: str,
        source_uri: str,
        target_uri: str,
        parameters: dict,
    ) -> dict:
        run_id = str(uuid4())
        activities = [
            "validate-source",
            "copy-to-azure-storage",
            "transform-with-adf-or-functions",
            "notify-with-logic-apps",
        ]
        status = "queued" if self.settings.azure_storage_connection_string else "dry_run"
        return {
            "run_id": run_id,
            "status": status,
            "activities": activities,
            "details": {
                "pipeline_name": pipeline_name,
                "source_uri": source_uri,
                "target_uri": target_uri,
                "parameters": parameters,
            },
        }
