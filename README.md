# API and MCP server for querying current UK MP Interests

- Provides an API (built with fastAPI), for querying the registered interests and information of current UK members of parliament (MP).

## File strucutre
```text
├── app
│   ├── __init__.py
│   ├── api_server.py
│   ├── client
│   │   ├── __init__.py
│   │   ├── client_interface.py
│   │   ├── clients.py
│   │   ├── fetch.py
│   │   ├── mock_responses
│   │   │   ├── mock_interest_response.json
│   │   │   └── mock_member_response.json
│   │   └── tests
│   │       ├── __init__.py
│   │       └── test_fetch.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── filters.py
│   │   └── tests
│   │       ├── __init__.py
│   │       ├── test_filters.py
│   │       └── test_merge_to_db.py
│   ├── data
│   │   └── members.db
│   ├── models
│   │   ├── __init__.py
│   │   ├── api_models.py
│   │   ├── parsers.py
│   │   ├── sqlmodel_models.py
│   │   └── tests
│   │       ├── __init__.py
│   │       ├── parsed_interest_response.py
│   │       ├── parsed_member_response.py
│   │       └── test_parsers.py
│   └── routes
│       ├── __init__.py
│       ├── interests_total_value.py
│       ├── members.py
│       └── party.py
├── docker-compose.yaml
├── Dockerfile
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

Where:
- `client` is responsible for fetching MP data from publicly available UK government APIs.
- `core` manages uploading data to an SQLite database (located in `app/data`), provides queries for that database, and contains global settings, such as the database location and log level.
- `data` contains the database.
- `models` contains `SQLModels` which define the tables in the database, the `api_models` which define the response types of the API endpoints, as well as `parsers` for parsing the `SQLModels` from json data.
- `routes` contains the API routes for the `FastAPI` app, including routes for searching members, interests, parties, as well as the total value of members interests between two dates.
- `app/api_server.py` is the entry point for the app.

## Installation

The app can be used with docker, or as a python package. In both cases, you must first clone the responsitory to a local directory by opening a terminal in said local directory and running
```bash
https://github.com/LylePoley/MP-interests-api.git
```

### With docker
If you have docker installed and the docker daemon is running, then you can run one of the following commands to run the application (they are equivalent):
```bash
make run-with-docker
```
or
```bash
docker-compose up --build
```

### With uv
If you would like to run the app using the uv package manager, you will need to have uv installed. To run the app, you can run either of the following commands (they are equivalent):
```bash
make run-with-uv
```

or
```bash
uv sync
uv run uvicorn app.api_server:app --host localhost --port 8000
```

## Using the MCP server with Claude desktop
To expose the FastAPI server to Claude desktop, the settings within the Claude desktop app need to be changed. Additional documentation can be found at the [FastAPI-MCP page](https://fastapi-mcp.tadata.com/getting-started/quickstart). In the Claude desktop app, go to `Settings->Developer->Edit Config` and add the `mp-interests` field to the `claude_desktop_config.json` file.
```json
{
  "mcpServers": {
    "mp-interests": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp"
      ]
    }
  }
}
```
Note that you may have to have `npx` installed on your local machine.
