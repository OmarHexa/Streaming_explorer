import os
import logging
from typing import Set
import kagglehub
import pandas as pd
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamingDataProcessor:
    def __init__(self,output_directory: str = "/opt/processed"):


        self.dataset_paths = {
            'netflix': self._find_csv_file(kagglehub.dataset_download("shivamb/netflix-shows")),
            'amazon': self._find_csv_file(kagglehub.dataset_download("shivamb/amazon-prime-movies-and-tv-shows")),
            'disney': self._find_csv_file(kagglehub.dataset_download("shivamb/disney-movies-and-tv-shows"))
        }        
        self.output_directory = output_directory
        self.all_data = []

    def _find_csv_file(self, path):
            """Find the first CSV file in the given path."""
            for file in os.listdir(path):
                if file.endswith('.csv'):
                    return os.path.join(path, file)
            raise FileNotFoundError(f"No CSV file found in {path}")
    
    def load_datasets(self) -> None:
        """Load all streaming datasets and add channel information."""
        try:
            for service, file_path in self.dataset_paths.items():
                df = pd.read_csv(file_path)
                df["channel_streaming"] = service
                self.all_data.append(df)
            logger.info("Successfully loaded all datasets")
        except Exception as e:
            logger.error(f"Error loading datasets: {str(e)}")
            raise

    def handle_missing_values(self) -> None:
        """Handle missing values in all datasets."""
        try:
            common_nan_columns = self._get_common_nan_columns()
            for data in self.all_data:
                for column in common_nan_columns:
                    data[column].fillna("UNKNOWN", inplace=True)
            logger.info("Successfully handled missing values")
        except Exception as e:
            logger.error(f"Error handling missing values: {str(e)}")
            raise

    def _get_common_nan_columns(self) -> Set[str]:
        """Get columns with NaN values across all datasets."""
        common_nan_columns = set()
        for data in self.all_data:
            nan_columns = data.columns[data.isnull().any(axis=0)]
            common_nan_columns.update(nan_columns)
        return common_nan_columns

    def save_processed_data(self) -> None:
        """Save processed datasets to CSV files."""
        try:
            os.makedirs(self.output_directory, exist_ok=True)
            for data in self.all_data:
                channel_name = data["channel_streaming"].iloc[0]
                output_df = data.drop(columns=["channel_streaming"])
                output_file_path = os.path.join(self.output_directory, f"{channel_name}.csv")
                output_df.to_csv(output_file_path, index=False)
            logger.info("Successfully saved processed datasets")
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            raise

class DatabaseUploader:
    def __init__(self,data_directory: str = "/opt/processed"):
        self.engine = self._create_database_engine()
        self.processed_directory = data_directory

    def _create_database_engine(self) -> create_engine:
        """Create SQLAlchemy engine with environment variables."""
        try:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise ValueError("DATABASE_URL environment variable not found")
            return create_engine(database_url)
        except Exception as e:
            logger.error(f"Error creating database engine: {str(e)}")
            raise

    def upload_data(self) -> None:
        """Upload processed data to database."""
        try:
            datasets = [f for f in os.listdir(self.processed_directory) if f.endswith(".csv")]
            for dataset in datasets:
                data = pd.read_csv(os.path.join(self.processed_directory, dataset))
                table_name = dataset.split(".")[0]
                data.to_sql(table_name, con=self.engine, if_exists="replace", index=False)
                logger.info(f"Successfully uploaded {table_name} to database")
        except Exception as e:
            logger.error(f"Error uploading data to database: {str(e)}")
            raise

def main():
    try:
        # Process streaming data
        processor = StreamingDataProcessor()
        processor.load_datasets()
        processor.handle_missing_values()
        processor.save_processed_data()

        # Upload to database
        uploader = DatabaseUploader()
        uploader.upload_data()
        
        logger.info("Data processing and upload completed successfully")
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()