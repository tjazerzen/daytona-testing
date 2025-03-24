# daytona-testing

Testing https://www.daytona.io/

## Setup

- Create venv from requirements.txt
- `export DAYTONA_API_KEY=...`

## Example Workflows

### Deploy Python code to Sandbox and execute tests

Summary:

- Uploads contents of `build_code/` to Daytona sandbox with the same tree structure
- Moves `run_conformance_python.sh` to the sandbox and makes it executable
- Moves `run_unittests_python.sh` to the sandbox and makes it executable
- Executes `run_conformance_python.sh`
- Executes `run_unittests_python.sh`
- Cleans up the sandbox after tests are finished

Further remarks:

- run the code from the root of the repository because of the relative paths
