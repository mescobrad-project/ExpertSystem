from pathlib import Path

db_path = Path("/tmp/").joinpath("test_db.db")
open(db_path, "a").close()
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
