# migrations/env.py

import logging
from logging.config import fileConfig

from alembic import context
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# --------------------------------------------------
# Tentamos importar Flask só se possível
try:
    from flask import current_app
    flask_app = current_app
except Exception:
    flask_app = None

# --------------------------------------------------
if flask_app:
    # Rodando dentro do contexto Flask
    config.set_main_option('sqlalchemy.url', current_app.config.get('SQLALCHEMY_DATABASE_URI'))
    target_db = current_app.extensions['migrate'].db

    def get_metadata():
        if hasattr(target_db, 'metadatas'):
            return target_db.metadatas[None]
        return target_db.metadata

    def get_engine():
        try:
            # Flask-SQLAlchemy<3 e Alchemical
            return current_app.extensions['migrate'].db.get_engine()
        except (TypeError, AttributeError):
            # Flask-SQLAlchemy>=3
            return current_app.extensions['migrate'].db.engine

else:
    import sys
    from sqlalchemy import create_engine

    # Adiciona o diretório src ao sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    # Importe todos os models do src.models
    from models import auditoria, documento, endividamento, fazenda, notificacao_endividamento, pessoa, usuario
    from models.db import Base

    def get_metadata():
        return Base.metadata

    def get_engine():
        url = config.get_main_option('sqlalchemy.url')
        return create_engine(url)

# --------------------------------------------------

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    def process_revision_directives(context, revision, directives):
        if flask_app:
            conf_args = current_app.extensions['migrate'].configure_args
            if conf_args.get("process_revision_directives") is None:
                conf_args["process_revision_directives"] = process_revision_directives
            return conf_args
        else:
            return {}

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **(current_app.extensions['migrate'].configure_args if flask_app else {})
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()