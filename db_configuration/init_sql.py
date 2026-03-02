"""
SQL initialization script for database setup.
This file contains SQL commands that should be executed before running the application.
"""

# SQL commands to create extensions (if not already created)
INIT_SQL = """
-- Create vector extension if not exists (required for pgvector)
CREATE EXTENSION IF NOT EXISTS vector;
"""

# Additional SQL that can be run on startup if needed
POST_INIT_SQL = """
-- Example: Refresh collation version (uncomment if needed)
-- ALTER DATABASE {db_name} REFRESH COLLATION VERSION;
"""


def get_init_sql():
    """Returns the init SQL commands as a string."""
    return INIT_SQL


def get_post_init_sql(db_name: str = None):
    """Returns the post init SQL commands as a string.
    
    Args:
        db_name: Database name to use in SQL commands
    """
    if db_name:
        return POST_INIT_SQL.format(db_name=db_name)
    return POST_INIT_SQL
