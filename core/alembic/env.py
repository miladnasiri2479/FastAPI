import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from pathlib import Path
from dotenv import load_dotenv

# Import the SQLAlchemy Base from your database module
from core.database import Base
from core.models import Task

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Environment Variable Setup ---
# Locate the .env file in the core directory (one level up from this file's directory)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    print(f"Warning: .env file not found at {ENV_PATH}. Using default settings.")

# Get the database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
    """
    url = SQLALCHEMY_DATABASE_URL or config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    In this scenario, we create an Engine and associate a connection with the context.
    """
    # 1. Get the configuration section from alembic.ini
    conf_section = config.get_section(config.config_ini_section, {})
    
    # 2. Inject the Database URL from environment variables
    # Default to a local sqlite file if the environment variable is not set
    url = SQLALCHEMY_DATABASE_URL or "sqlite:///./sqlite.db"
    conf_section["sqlalchemy.url"] = url

    # 3. Create the engine from the modified configuration
    connectable = engine_from_config(
        conf_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # render_as_batch is required for SQLite to support ALTER TABLE operations
            render_as_batch=True 
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine if we should run in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()