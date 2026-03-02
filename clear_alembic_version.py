from sqlalchemy import create_engine, text
from db_configuration.config import settings

engine = create_engine(
    f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

with engine.connect() as conn:
    conn.execute(text('DELETE FROM alembic_version'))
    conn.commit()
    print('Cleared alembic_version table')
