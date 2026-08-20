from dataclasses import dataclass
import os


@dataclass
class WorkflowConfig:
    enable_memory: bool = True
    enable_rag: bool = True
    enable_database: bool = True

    max_history: int = 5

    @classmethod
    def from_env(cls):
        return cls(
            enable_memory=os.getenv(
                "ENABLE_MEMORY", "true"
            ).lower() == "true",

            enable_rag=os.getenv(
                "ENABLE_RAG", "true"
            ).lower() == "true",

            enable_database=os.getenv(
                "ENABLE_DATABASE", "true"
            ).lower() == "true",

            max_history=int(
                os.getenv("MAX_MEMORY_HISTORY", "5")
            ),
        )