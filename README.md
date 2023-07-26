# Baseball Stats Core
Core for baseball stats app

### Run :sparkles:
#### Localy:
- Clone this repo
- Run the following commands:
```bash
make venv  # virtual env
source venv/bin/activate
make install
uvicorn beistats_core.app:app --reload
```
#### Docker:

- Run the following commands in the root file:
```bash
make docker-run
```