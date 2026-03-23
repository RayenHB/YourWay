# xtend-recruit-back



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Project Structure

```
xtend-recruit-back/
├── any_manager
├── user_manager
├── .env
├── .gitignore
├── .idea/
├── pyproject.toml
├── poetry.lock
├── xtend_recruit-back/
```

## Prerequisites

- Python 3.12+
- PostgreSQL
- Poetry

## Setup Instructions
### 1. Clone the Repository

```bash
git clone https://gitlab.xtendplex.com/xtendrecruit/xtend-recruit-back.git
cd xtend_recruit_back
```
### 2. Environment Variables

Copy the provided `.env` file or create a new one with the necessary environment variables. An example `.env` file might look like this:

```
SECRET_KEY=your_secret_key
DEBUG=True or False
APP_ENV=dev or prod or test
DATABASE_URL=postgresql+asyncpg://your_db_user:your_db_password@your_db_host:your_db_port/your_db_name
```

### 3. Install Dependencies

Make sure you have Poetry installed. If not, you can install it using:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then, install the project dependencies:

```bash
poetry install
```

### 4. Set Up the Database

Make sure you have PostgreSQL installed and running :


Update the `DATABASE_URL` in your `.env` file with your database credentials.

### 5. Run Migrations

To Generate a new migration:
```bash
poetry run alembic revision --autogenerate -m ""
```
To run the migrations, use Alembic:

```bash
poetry run alembic upgrade head
```

### 6. Start the Application

To start the application, use:

```bash
poetry run uvicorn --host=0.0.0.0 --port=8000 main:app
```

The application will be available at `http://127.0.0.1:8000`.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

