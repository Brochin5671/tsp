# The Space Prime API

API for all things space.
Space news, epihermes, other info and more!

## Space News

- **/news**
  - Returns both space science and industry news
- **/news/industry/**
  - Returns space industry news (spaceflight, space tech, etc.)
- **/news/science/**
  - Returns space science news (astronomy, astrobiology, astrophysics, etc.)

## Roadmap & WIP

Tracking progress of the API (frontend will be its own section). Not all items are listed, just more general ones and expecting scope-creep.

- [ ] Space News
  - [x] All
  - [x] Industry
  - [x] Science
  - [ ] Other filters
- [ ] NASA Imagery
  - [ ] Current Earth imagery
  - [ ] Data from Mars rovers
- [ ] Astronomy Weather
  - [ ] Light pollution estimation
  - [ ] Seeing
  - [ ] Transparency
  - [ ] Clouds
- [ ] Epihermes
  - [ ] Observation data
  - [ ] Events
- [ ] Tests
  - [ ] More coverage
  - [ ] Automation
- [ ] Technical
  - [ ] Logger
  - [ ] Use PyPi

## Dev Setup & Installation

**Ensure python3 and pip are installed in your Linux environment.**

Clone the repository:

```bash
git clone https://github.com/Brochin5671/tsp.git
cd tsp
```

Create and activate a virtual environment for the backend API:

```bash
cd backend
python3 -m venv env
source env/bin/activate
```

Install requirements for the backend API:

```bash
pip install -r requirements.txt
```

Run the backend API:

```bash
uvicorn main:app --reload --port=8000
```

The backend will be available at `localhost:8000`.
API docs are available at `localhost:8000/docs`

### Tests

Run tests for the backend API:

```bash
pytest -vv
```
