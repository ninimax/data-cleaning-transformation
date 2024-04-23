# Data Transformation and Cleaning

## TL;DR

### WHO

Shuang

### WHAT

A pipeline app for data cleaning and transformation based on the requirements

### WHAT WHAT (high-level structure)

- data: original and generated data files
- logs: application- and data quality- logs
- src: source code
- tests: unit and integration testings
- data_sources.json: json file holding name, type and path to original files
- .env: environment file for quickly switching configurations between dev/prod env

### HOW

- Install dependencies

  ```pip install -r requirements.txt```
- Run the app

  ```python ./src/pipeline.py```
- Run the unit tests

  ```python -m unittest discover -s ./tests/unit```
- Run the integration tests

  ```python -m unittest discover -s ./tests/integration```

### BEST PRACTICE

- TDD (with unit- & integration tests)
- Clean Code (I believe that the code itself should explain (almost) everything,
  therefore you may not find too many comments unless absolutely needed)
- PEP8
- Dotenv
- Generic parameterized functions, e.g., param "column_name" gives reusability 

### REFLECTION

- It is a fun project to get hands dirty!
- It is also a great assignment to simulate a pipeline covering many ELT steps!
- Configuring two loggers was trivial if you really want to detail all aspects, e.g.,
  handlers, formatters etc.
- Handling missing values can sometimes be tricky and may need to use str() first,
  especially for null, NaT, NaN etc.
- The command "pytest" did not work for automatically detection of all test cases and therefore
  I use command "python -m unittest discover -s [path]" instead
