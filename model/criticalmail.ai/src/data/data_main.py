import os
import logging
from data_services import Data_Services

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

data_path = os.path.join(project_root, "data", "raw", "dataset.csv")

data_serv = Data_Services()

try:
    if not os.path.isfile(data_path):
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    logger.info(f"Dataset found: {data_path}")
    data = data_serv.load_data(data_path)

    # Is data empty
    if data.empty:
        raise ValueError("Dataset is empty")
    logger.info(f"Dataset loaded successfully. Shape: {data.shape}")

    # Tokenize the text data
    tokenize_text = data_serv.tokenize_text()
    data['message_body_tokens'] = data['message_body'].apply(tokenize_text)
    logging.info("Tokenization of words completed")

except Exception as ex:
    logger.exception("Something went wrong in data_main")
    raise ex
