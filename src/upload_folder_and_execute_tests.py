from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams, Sandbox
import os


def create_daytona_sandbox() -> tuple[Daytona, Sandbox]:
    DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")

    if not DAYTONA_API_KEY:
        raise ValueError("DAYTONA_API_KEY is not set")

    config = DaytonaConfig(
        api_key=DAYTONA_API_KEY,
        server_url="https://app.daytona.io/api",
        target="us",
    )

    # Initialize the Daytona client
    daytona = Daytona(config)

    # Create the Sandbox instance
    sandbox = daytona.create(CreateSandboxParams(language="python"))

    return daytona, sandbox


