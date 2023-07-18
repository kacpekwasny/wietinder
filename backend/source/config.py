from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BACKEND_DIR.parent
UPLOADS_DIR = BACKEND_DIR / "uploads"


class Config:
    """
    Abstrakcyjna clasa, do configu. Wskazuje jakie pola powinien konfig implementować.
    """

    SQLALCHEMY_DATABASE_URI: str
    """TODO: docstr - od czego jest ten atrybut"""

    SECRET_KEY: str
    """ """


class ConfigDev(Config):
    """Development config to be run on local machine."""
    db_path = str(BACKEND_DIR / "database.db")

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    SECRET_KEY = 'asdfjasdi'


class ConfigProd(Config):
    """Production config to be run on server."""

    SQLALCHEMY_DATABASE_URI = f'mysql:///127.0.0.1 costam costam'
    
    SECRET_KEY = ''


