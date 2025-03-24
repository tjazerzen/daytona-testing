from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams, Sandbox
import os

ROOT_DIR = "/home/daytona"
BUILD_CODE_PATH = "build_code"
SANDBOX_TARGET_DIR = f"{ROOT_DIR}/build_code"
UNITTEST_SCRIPT_PATH = "run_unittests_python.sh"
UNITTEST_SCRIPT_SANDBOX_NAME = "run_unittests_python.sh"
UNITTEST_SCRIPT_SANDBOX_PATH = f"{SANDBOX_TARGET_DIR}/{UNITTEST_SCRIPT_SANDBOX_NAME}"
CONFORMANCE_TESTS_SCRIPT_PATH = "run_conformance_tests_python.sh"
CONFORMANCE_TESTS_SCRIPT_SANDBOX_NAME = "run_conformance_tests_python.sh"
CONFORMANCE_TESTS_SCRIPT_SANDBOX_PATH = (
    f"{SANDBOX_TARGET_DIR}/{CONFORMANCE_TESTS_SCRIPT_SANDBOX_NAME}"
)
CONFORMANCE_TESTS_FOLDER = "tests"
CONFORMANCE_TESTS_SANDBOX_PATH = f"{SANDBOX_TARGET_DIR}/{CONFORMANCE_TESTS_FOLDER}"


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


def upload_unittest_files(sandbox: Sandbox):
    with open(UNITTEST_SCRIPT_PATH, "rb") as file:
        content = file.read()

    sandbox.fs.upload_file(UNITTEST_SCRIPT_SANDBOX_PATH, content)

    change_permissions_cmd = f"chmod +x {UNITTEST_SCRIPT_SANDBOX_PATH}"
    print(f"Executing change permissions command: {change_permissions_cmd}")
    response = sandbox.process.exec(change_permissions_cmd, cwd=SANDBOX_TARGET_DIR)
    print("change permissions response:", response.exit_code)
    print("change permissions result:", response.result)


def run_unittest_script(sandbox: Sandbox):
    unittest_cmd = f"./{UNITTEST_SCRIPT_SANDBOX_PATH} {SANDBOX_TARGET_DIR}"
    print(f"Executing unittest command: {unittest_cmd}")
    response = sandbox.process.exec(unittest_cmd, cwd=SANDBOX_TARGET_DIR)
    print("unittest response:", response.exit_code)
    print("unittest result:", response.result)


def upload_conformance_tests_files(sandbox: Sandbox):
    with open(CONFORMANCE_TESTS_SCRIPT_PATH, "rb") as file:
        content = file.read()

    sandbox.fs.upload_file(CONFORMANCE_TESTS_SCRIPT_SANDBOX_PATH, content)

    change_permissions_cmd = f"chmod +x {CONFORMANCE_TESTS_SCRIPT_SANDBOX_PATH}"
    print(f"Executing change permissions command: {change_permissions_cmd}")
    response = sandbox.process.exec(change_permissions_cmd, cwd=SANDBOX_TARGET_DIR)
    print("change permissions response:", response.exit_code)
    print("change permissions result:", response.result)


def run_conformance_tests_script(sandbox: Sandbox):
    conformance_tests_cmd = f"./{CONFORMANCE_TESTS_SCRIPT_SANDBOX_PATH} {SANDBOX_TARGET_DIR} {CONFORMANCE_TESTS_SANDBOX_PATH}"
    print(f"Executing conformance tests command: {conformance_tests_cmd}")
    response = sandbox.process.exec(conformance_tests_cmd, cwd=SANDBOX_TARGET_DIR)
    print("conformance tests response:", response.exit_code)
    print("conformance tests result:", response.result)


# Example usage
if __name__ == "__main__":
    # Get the user root directory in the sandbox
    daytona, sandbox = create_daytona_sandbox()

    try:
        # uploading python code to the sandbox
        upload_repo_to_sandbox(sandbox)

        # uploading and running unittests
        upload_unittest_files(sandbox)
        run_unittest_script(sandbox)

        # uploading and running conformance tests
        upload_conformance_tests_files(sandbox)
        run_conformance_tests_script(sandbox)
    finally:
        # Clean up the Sandbox
        print("Cleaning up the sandbox")
        daytona.remove(sandbox)
