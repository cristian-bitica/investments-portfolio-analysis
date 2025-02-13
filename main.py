
from src.bronze.ingest_assets_prices import download_data_from_api
from src.spark_session import get_spark_session

get_spark_session()

download_data_from_api(["AAPL", "MSFT"], "2021-01-01", "2021-12-31").show()