from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams, Sandbox
import os
BUILD_CODE_PATH = "build_code"
SANDBOX_TARGET_DIR = f"{ROOT_DIR}/build_code"


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


def upload_repo_to_sandbox(sandbox: Sandbox):
    # Expand the tilde in the path to get the absolute path
    local_build_dir = os.path.expanduser(BUILD_CODE_PATH)
    print(f"Copying files from: {local_build_dir}")

    # Create the target directory in the sandbox if it doesn't exist
    sandbox.fs.create_folder(SANDBOX_TARGET_DIR, mode="755")

    # Walk through all files in the build_code directory
    for root, dirs, files in os.walk(local_build_dir):
        for dir_name in dirs:
            # Create corresponding directory structure in sandbox
            local_dir_path = os.path.join(root, dir_name)
            relative_path = os.path.relpath(local_dir_path, local_build_dir)
            sandbox_dir_path = os.path.join(SANDBOX_TARGET_DIR, relative_path)
            print(f"Creating directory: {sandbox_dir_path}")
            sandbox.fs.create_folder(sandbox_dir_path, mode="755")

        for file_name in files:
            # Get the local file path
            local_file_path = os.path.join(root, file_name)
            # Get the relative path to maintain directory structure
            relative_path = os.path.relpath(local_file_path, local_build_dir)
            # Construct the target path in sandbox
            sandbox_file_path = os.path.join(SANDBOX_TARGET_DIR, relative_path)

            print(f"Copying file: {local_file_path} -> {sandbox_file_path}")

            # Read the file content
            with open(local_file_path, "rb") as file:
                content = file.read()

            # Upload the file to the sandbox
            sandbox.fs.upload_file(sandbox_file_path, content)

    print("File copying completed")
