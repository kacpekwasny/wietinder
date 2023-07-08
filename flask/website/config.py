from pathlib import Path


class Config:
    """
    Abstrakcyjna clasa, do configu. Wskazuje jakie pola powinien konfig implementować.
    """

    SQL_ALCHEMY_DATABSE_URI: str
    """TODO: docstr - od czego jest ten atrybut"""

    SECRET_KEY: str
    """ """


class ConfigDev(Config):
    """Development config to be run on local machine."""
    db_path = str(Path(__file__).resolve().parent.parent / "database.db")

    SQL_ALCHEMY_DATABSE_URI = f'sqlite:///{db_path}'
    
    SECRET_KEY = 'asdfjasdi'


class ConfigProd(Config):
    """Production config to be run on server."""

    SQL_ALCHEMY_DATABSE_URI = f'mysql:///127.0.0.1 costam costam'
    
    SECRET_KEY = ''


