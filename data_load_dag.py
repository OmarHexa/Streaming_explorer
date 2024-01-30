import os
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

PATH_RAW = "../Data"

default_args = {
    "owner": "your_name",
    "start_date": datetime(2024, 1, 1),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "process_datasets_dag",
    default_args=default_args,
    schedule_interval="@daily",
)


def process_datasets(**kwargs):
    """Data cleaning of the raw csv dataset."""
    logger = kwargs["ti"].xcom_push(key="logger", value=kwargs["log"])
    logger.info("All the available datasets: %s", os.listdir(PATH_RAW))

    datasets_names = [
        filename
        for filename in os.listdir(PATH_RAW)
        if filename.endswith(".csv") and not filename.startswith("IMDb")
    ]
    all_data = []
    for dir_ in datasets_names:
        read_pd = pd.read_csv(os.path.join(PATH_RAW, dir_))
        read_pd["channel_streaming"] = dir_.split("_")[0]
        all_data.append(read_pd)

    for data in all_data:
        logger.info("Columns in %s Data: \n %s", data["channel_streaming"].iloc[0], data.columns)

    for data in all_data:
        nan_columns = data.columns[data.isnull().any()]
        nan_columns_with_percentage = {
            column: data[column].isnull().mean() * 100 for column in nan_columns
        }  # Dict comprehension

        logger.info("NaN Columns and Percentages in %s Data:", data["channel_streaming"].iloc[0])
        for column, percentage in nan_columns_with_percentage.items():
            logger.info("\t %s: %.2f%%", column, percentage)
        logger.info("\n")

    for data in all_data:
        data["cast"].fillna("unknown", inplace=True)
        data["director"].fillna("unknown", inplace=True)
        data["country"].fillna("unknown", inplace=True)
        data["date_added"].fillna("unknown", inplace=True)
        data["rating"].fillna("unknown", inplace=True)
        data["rating"] = data["rating"].str.upper()
        data["duration"].fillna("unknown", inplace=True)

    output_directory = os.path.join(PATH_RAW, "processed")
    os.makedirs(output_directory, exist_ok=True)

    for data in all_data:
        channel_name = data["channel_streaming"].iloc[0]

        data = data.drop(columns=["channel_streaming"])

        output_file_path = os.path.join(output_directory, f"{channel_name}.csv")
        data.to_csv(output_file_path, index=False)
    logger.info("Datasets saved into separate CSV files.")


with dag:
    process_datasets_task = PythonOperator(
        task_id="process_datasets_task",
        python_callable=process_datasets,
        provide_context=True,
    )

process_datasets_task
