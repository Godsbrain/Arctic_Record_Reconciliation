from urllib.parse import quote_plus
from sqlalchemy import create_engine

def get_engine():
    username = "root"
    password = quote_plus("Akwasi@1996")
    host = "localhost"
    port = "3306"
    database = "arctic_records"

    connection_string = (
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )

    engine = create_engine(connection_string)
    return engine