from pathlib import Path


class Config:
    """
    Abstrakcyjna clasa, do configu. Wskazuje jakie pola powinien konfig implementować.
    """

    SQLALCHEMY_DATABASE_URI: str
    """TODO: docstr - od czego jest ten atrybut"""

    SECRET_KEY: str
    """ """

    UPLOAD_FOLDER: str
    """Folder do uploadowania zdjec???"""


class ConfigDev(Config):
    """Development config to be run on local machine."""
    db_path = str(Path(__file__).resolve().parent.parent / "database.db")

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    SECRET_KEY = 'asdfjasdi'


class ConfigProd(Config):
    """Production config to be run on server."""

    SQLALCHEMY_DATABASE_URI = f'mysql:///127.0.0.1 costam costam'
    
    SECRET_KEY = ''


