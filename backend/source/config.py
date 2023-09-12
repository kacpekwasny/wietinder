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

    JWT_SECRET: str
    """ secret for JWT """

    JWT_TIMEOUT: float = 30
    """ Time for which JWT is valid represented in seconds """


class ConfigDev(Config):
    """Development config to be run on local machine."""
    db_path = str(BACKEND_DIR / "database_dev.db")

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    SECRET_KEY = 'asdfjasdi'

    JWT_SECRET = 'apud'


class ConfigProd(ConfigDev):
    """Production config to be run on server."""

    # SQLALCHEMY_DATABASE_URI = f'mysql:///127.0.0.1 costam costam'
    
    # SECRET_KEY = 'o87gouyvi65divuio6fb cu6f7'



from . import IS_PROD

CONFIG: Config = ConfigProd if IS_PROD else ConfigDev