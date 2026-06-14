import os
import mlflow
import mlflow.data
import logging

from src.data.data_services import Data_Services
from src.visualization.data_visualization import Data_VIsualization


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Email_Data_Processing")

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))

data_path = os.path.join(project_root, "data", "raw", "dataset.csv")

data_serv = Data_Services()
data_vis = Data_VIsualization()

with mlflow.start_run(run_name="Data_Cleaning_and_Tokenization") as run:
    try:
        if not os.path.isfile(data_path):
            raise FileNotFoundError(f"Dataset not found: {data_path}")

        logger.info(f"Dataset found: {data_path}")
        data = data_serv.load_data(data_path)

        # Is data empty
        if data.empty:
            raise ValueError("Dataset is empty")
        logger.info(f"Dataset loaded successfully. Shape: {data.shape}")

        # Merging of table class variables
        merged_data = data_serv.merge_target_vals()

        # Tokenize the text data
        merged_data["message_body_tokens"] = merged_data["message_body"].apply(
            data_serv.tokenize_text
        )

        # Rejecting the irrelevant fields
        processed_data = merged_data[
            ['message_body', 'message_body_tokens', 'email_criticality']
            ]

        logging.info("Tokenization of words completed")

        # Visualization of data
        fig_location = os.path.join(project_root, 'reports', 'figures')
        os.makedirs(fig_location, exist_ok=True)

        count_file_name = "count_class.jpg"
        data_vis.count_class(processed_data, fig_location, count_file_name)

        class_vs_len_file_name = "class_vs_len.jpg"
        data_vis.len_vs_class(processed_data, fig_location,
                              class_vs_len_file_name)

        wcloud_file_name = "word_cloud.jpg"
        data_vis.words_cloud(processed_data, fig_location, wcloud_file_name)

        # Saving the file to the data/processed
        processed_dir = os.path.join(project_root, "data", "processed")

        os.makedirs(processed_dir, exist_ok=True)
        output_path = os.path.join(processed_dir, "processed_dataset.csv")

        # Save the DataFrame
        processed_data.to_csv(output_path, index=False)
        logger.info(f"Processed dataset saved successfully to: {output_path}")

        # Logging the processed_data to mlflow as artifacts
        dataset_metadata = mlflow.data.from_pandas(
            processed_data, source=output_path, name="processed_email_dataset"
        )
        mlflow.log_input(dataset_metadata, context="processed")
        logger.info("Dataset profile metadata logged to MLflow Inputs.")

        mlflow.log_artifact(output_path, artifact_path="datasets")
        logger.info("Physical CSV file logged to MLflow Artifacts.")

        # Logging the figures to MLFLOW
        if os.path.exists(fig_location):
            mlflow.log_artifacts(fig_location, artifact_path="plots")
            logger.info(
                "All visualization images logged"
                "to MLflow Artifacts successfully."
                )
        else:
            logger.warning(
                f"Visualization directory not found at: {fig_location}"
                )

    except Exception as ex:
        logger.exception("Something went wrong in data_main")
        raise ex
