from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


user = "postgres"
password = 12345678
host = "127.0.0.1"
database = "email"
port = 5432

link = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(link)
logging.info("Successfully created engine")

Base = declarative_base()
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logging.info("Local session created")


def get_db():
    db = sessionLocal()
    try:
        yield db
    except Exception as ex:
        # Log it properly with exc_info=True
        logging.error(
            "Database dependency encountered an error", exc_info=True
            )
        raise ex
    finally:
        db.close()
        logging.info("Database closed")


def create_db():
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)
    logging.info("Created Database successfully")
