# Browser_Automation_python

Secure browser automation with credential management and encryption.

## Features
- Secure credential storage with AES-256 encryption
- Multiple verification modes (CLI, JSON, binary)
- Docker support
- Comprehensive error handling

## Workflow

### For local development:

```bash
# Configure environment:
./scripts/dev_setup.sh

# Or
# Activate environment:
source .venv/bin/activate

pip install -r requirements.txt

# Run tests:
./scripts/run_tests.sh
```

### For Docker:

```bash
# Configure environment:
./scripts/docker_build_run.sh

# Or
# Build image:
docker build -t browser-automation-python .

# Perform standard check:
docker run --rm browser-automation-python

# Perform JSON verification:
docker run --rm browser-automation-python check_cred_json

# Run tests inside the container:
docker run --rm browser-automation-python pytest
```

## Installation

### Python workbench setup:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install basic dependencies:
```bash
pip install --upgrade pip setuptools
pip install -e .
```

### Docker:
```bash
docker build -t browser-automation-python
docker run --rm browser-automation-python
```

### Testing:

```bash
./scripts/run_tests.sh
```

## Usege pip

```bash
# Check credentials (human-readable).
check_cred

# Check credentials (JSON output).
check_cred_json

# Check credentials (binary output).
check_cred_bin
```

## Directory ->
```
browser_automation_python/
├── credentials/
│   ├── __init__.py
│   ├── credentials.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── check_cred_bin.py
│   │   ├── check_cred.py
│   │   └── check_cred_json.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py
│   └── msg/
│       ├── __init__.py
│       └── message.py
├── tests/
│   ├── unit/
│   │   ├── test_credentials.py
│   │   └── test_message.py
│   └── integration/
│       ├── test_commands.py
│       └── test_c_integration.c
├── docs/
│   ├── design.md
│   └── api_reference.md
├── scripts/
│   ├── setup_venv.sh
│   └── run_tests.sh
├── .gitignore
├── Dockerfile
├── requirements.txt
├── setup.py
└── README.md
```