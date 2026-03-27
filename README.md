<img src="media/mitly_logos/mitly-type-orange.svg" alt="mitly_logo" width="300">

### Table of contents

* [Project Overview](#project-overview)
* [Folder Structure](#folder-structure)
* [Development Workflow](#development-workflow)
* [System Design](#system-design)
* [Low Level Design Implementation](#low-level-design-implementation)
* [Setup](#setup)
* [Helpful stuff](#helpful-stuff)

# Project Overview

* **Tech**: <img src="media/fastapi_icon.svg" width="22" height="22" valign="middle"> FastAPI
  <img src="media/react_icon.svg" width="26" height="26" valign="middle"> React
  <img src="media/postgresql_icon.svg" width="23" height="23" valign="middle"> PostgreSQL
  <img src="media/sqlalchemy_icon.svg" width="23" height="23" valign="middle"> SQLAlchemy
  <img src="media/pytest_icon.svg" width="21" height="21" valign="middle"> Pytest
  <img src="media/pydantic_icon.svg" width="21" height="21" valign="middle"> Pydantic
  <img src="media/docker_icon.svg" width="21" height="21" valign="middle"> Docker


* **Summary**: Mitly is a URL shortening service inspired by [Bitly](https://app.bitly.com/)

### Key Technical Implementation:

* **Architectural Design:** Implemented an **N-Tier (Layered) Architecture** separating concerns into:
    * Presentation Layer: `app/api/` & `app/schemas/`
    * Business Logic Layer: `app/crud/`
    * Data Access Layer: `app/crud/` how the app uses the database
    * Database/Persistence Layer: `app/db/` how the database exists


* **Database Integration:** Implemented a PostgreSQL-backed persistence layer using SQLAlchemy ORM. Utilized a
  `db.flush()` pattern to obtain auto-incremented primary keys for Base62 encoding, ensuring transactional
  integrity and unique ID generation. [crud_url.py](src/app/crud/crud_url.py)


* **Base62 Encoding Algorithm:** Developed a custom utility to convert internal database IDs into short, URL-friendly
  alphanumeric strings (e.g. `mit.ly/1zG7`), optimized for $O(\log_{62} n)$ runtime. [utils.py](src/app/crud/utils.py)


* **Robust Configuration Management:** Built a multienvironment settings system using `pydantic-settings` and
  `@lru_cache`, supporting seamless transitions between Development, Production, and
  Testing via `.env` files. [base.py](src/app/config/base.py) | [__init__.py](src/app/config/__init__.py)


* **Unit testing:** Test suite using `pytest`. Configured an in-memory SQLite db and leveraged `pytest-mock`
  for dependency injection and lifecycle testing. [conftest.py](tests/conftest.py)


* **Modern Dependency Management:** Utilized `uv` for lightning-fast package management and
  reproducible virtual environments. [pyproject.toml](pyproject.toml) | [uv.lock](uv.lock)

### Upcoming Features & Scale-Up Plan:

* **Deployment:** Dockerizing the application for containerized deployment.
* **Frontend Integration:** Building a responsive user interface with **React** to allow users to manage their shortened
  links.
* **Advanced Testing:** Developing a custom "Live Migration" test suite to verify database schema migrations while the
  application remains active and handles real-time read/write traffic.

[↑ Back to Top](#table-of-contents)

# Folder Structure

helper command: ```uv run python -m directory_tree -I temp media __init__.py __pycache__ *.* routes low_level_design```

```shell
mitly/
├── requirements/     # base/local dependencies
├── src/              # source code
│   └── app/          # application code
│       ├── api/      # Presentation Layer: api routers and endpoint definitions
│       │   ├── v1/   # current public/stable api version
│       │   └── v2/   # next/experimental api version
│       ├── config/   # app settings split by environment type
│       ├── crud/     # Business Logic & Data Access Layer
│       ├── db/       # Database Layer: database setup, sessions, and ORM models
│       ├── schemas/  # Presentation Layer: pydantic schemas defining the valid api input/output format
│       └── main.py   # application entry point
└── tests/            # automated tests
```

[↑ Back to Top](#table-of-contents)

# Development Workflow

Inside out approach (Data > Logic > Interface)  
database models > pydantic schemas > crud logic > fastapi endpoints > main.py entry point

[↑ Back to Top](#table-of-contents)

# System Design

## Delivery Framework

![delivery_framework.png](media/delivery_framework.png)

## -------------------- 1. Requirements

### Functional Requirements

Core features

1. create a short url from a long url
    - [optional] support expiration time
    - [skipped] support a custom alias
2. redirection to the original url from the short one

### Non-functional Requirements

Qualities like Scalability, Latency, Security, Fault Tolerance

1. Ensure **uniqueness**   
   We must guarantee that each short URL maps to exactly one long URL; otherwise users could be redirected to an
   unexpected website.

2. Low **latency** on redirects (~200 ms)

3. **Scale** to support:
    - 100M daily active users (DAU)
    - 1B stored URLs

4. **CAP Theorem** (Brewer's theorem says that **distributed systems** can guarantee only two guaranties at the same
   time)  
   **AP + eventual consistency** (Tech: Cassandra, DynamoDB)  
   eventual consistency means that updates propagate to all replicas over time  
   Because we would prefer the system to be always working, despite a node failure. Having the most recent data as soon
   as possible is not a priority.
    - ✅ Guarantee **[A]vailability**: (информацията винаги е налична, но не винаги е актуална) Every request receives
      a (non-error) response, even if a node has dropped, without the guarantee that it contains the most recent
      write/data.
    - ✅ Guarantee **[P]artition tolerance (устойчивост при разделяне)**: System continues to work even if network
      communication between nodes is interrupted
    - ❌ **[C]onsistency**: (информацията е винаги актуална, но не винаги е налична) All clients/nodes see the same data
      at the same time  
      Usecases: Banking, Stocks, Ticket booking system, etc.  
      Strong consistency guarantees that the following example will **NOT** happen:  
      p1 from EU buys last ticket to a concert and p2 buys it at the same time from US.

💡Note: [P]artition Tolerance is usually not optional in modern distributed systems because networks will eventually
fail

## -------------------- 2. Core Entities

- Original url
- Short url
- [optional] User

## -------------------- 3. API or Interface

💡 Tip: Functional Requirements hint the endpoints

- shorten url  
  POST /urls > short_url

```json
{
  "original_url": "https://github.com/miray-mustafov/mitly",
  "optional_alias": null,
  "optional_expiration_time": null
}
```

- redirect  
  GET {short_url} > redirect to original_url

```json
{
  "short_url": "https://mitly/asd123"
}
```

## -------------------- 4. Data Flow (skipped)

## -------------------- 5. High-level Design

![basic_high_level_design.png](media/basic_high_level_design.png)

## -------------------- 6. Deep Dives

todo

[↑ Back to Top](#table-of-contents)

# Low Level Design Implementation

[low_level_design/url_shortener.py](low_level_design/url_shortener.py)

[↑ Back to Top](#table-of-contents)

# Setup

Local setup for Windows OS

### Open the terminal, navigate to a desired folder, and run:

```shell
git clone git@github.com:miray-mustafov/mitly.git
```

<br>

### Navigate to the root level of the project:

```shell
cd mitly
```

<br>

### Configure and activate python virtual environment

```shell
uv venv --python 3.13
.venv\Scripts\activate
```

*Note: If uv not installed ```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```  
<br>

### Install dependencies

```shell
uv sync
```

<br>

### Create a local .env file next to .env.example:

<br>

### Setup postgres database (suggested command in .env.example):

<br>

### Run the app:

```shell
uv run mitly
```

[↑ Back to Top](#table-of-contents)

# Helpful stuff

run tests locally at root level:

```shell
uv run pytest
```

[↑ Back to Top](#table-of-contents)