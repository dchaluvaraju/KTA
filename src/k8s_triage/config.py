from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    max_tool_iterations: int = Field(default=10, description="Max tool iterations per request")
    max_log_lines: int = Field(default=100, description="Default number of log lines to tail")
    max_log_lines_cap: int = Field(default=300, description="Max allowed log lines to tail")
    max_log_chars: int = Field(default=12000, description="Max characters per log chunk")
    model: str = Field(default="gpt-4o", description="OpenAI model to use")

    model_config = SettingsConfigDict(env_prefix="K8S_TRIAGE_", env_file=".env", extra="ignore")

config = AppConfig()
