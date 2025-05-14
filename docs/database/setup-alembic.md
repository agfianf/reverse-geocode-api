
## Setup Alembic
### 1. init Alembic

```bash
cd src
alembic init migrations
```

### 2. edit alembic.ini
remove the `#` from the line below

```ini
...
- # file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
+ file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
...
```

### 3. edit env.py
3.0 add Database URL to config.py
```python
...

settings: Final[Settings] = Settings()
DATABASE_URL: Final = f"postgresql+psycopg://{settings.POSTGRE_USER}:{settings.POSTGRE_PASSWORD}@{settings.POSTGRE_HOST}:{settings.POSTGRE_PORT}/{settings.POSTGRE_DB}"
```

#### 3.1 setup database connection on your code
```python app/helpers/database.py
"""Database connection configuration and setup for the FastAPI auth service."""

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from app.config import settings


DATABASE_URL = URL.create(
    driver_name="postgresql+psycopg",
    username=settings.POSTGRE_USER,
    password=settings.POSTGRE_PASSWORD,
    host=settings.POSTGRE_HOST,
    port=settings.POSTGRE_PORT,
    database=settings.POSTGRE_DB,
)


engine_async = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=20,
    echo=False,
    echo_pool=True,
)

Base = declarative_base()
metadata = Base.metadata
```

#### 3.2 setup database depedencies
```python  app/dependencies/database.py
from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncConnection

from app.helpers.database import engine_async


async def get_async_transaction_conn() -> AsyncGenerator[
    AsyncConnection,
    None,
]:
    # Get async connection
    async with engine_async.connect() as connection:  # noqa: SIM117
        # Begin transaction
        async with connection.begin():
            try:
                yield connection
                # Transaction will be automatically committed
                # if no exceptions occur (feature of sqlalchemy2)
            except SQLAlchemyError as e:
                # Transaction will be automatically rolled back on exception
                print(f"SQLAlchemyError: {e}")
                raise
            finally:
                pass
                # Connection will be automatically closed due to async with


async def get_async_conn() -> AsyncGenerator[AsyncConnection, None]:
    """For simple read operations."""
    async with engine_async.connect() as connection:
        try:
            yield connection
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError: {e}")
            raise
        finally:
            pass

```

#### 3.3 edit env.py
```python
from app.helpers.database import metadata
from app.config import DATABASE_URL

# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# [ADD BY ME]
# Set the database URL in the Alembic configuration
config.set_main_option("sqlalchemy.url", str(DATABASE_URL))
configuration = config.get_section(config.config_ini_section, {})

def run_migrations_offline() -> None:
...
```

### 4. Try your first migration
```bash
cd src
alembic revision -m "create user table"
```

### 5. edit the migration file
### 6. apply the migration
```bash
alembic upgrade head
```


## List of Alembic commands in Table
|Command | Description |
|--------|-------------|
| `alembic init <directory>` | Create a new migration environment. |
| `alembic revision -m <message>` | Create a new migration script. |
| `alembic upgrade <revision>` | Apply migrations up to a specific revision. |
| `alembic downgrade <revision>` | Revert migrations to a specific revision. |
| `alembic history` | Show the migration history. |
| `alembic current` | Show the current revision. |
