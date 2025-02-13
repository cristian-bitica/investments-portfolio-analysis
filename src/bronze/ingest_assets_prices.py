import yfinance as yf
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession

from src.spark_session import get_spark_session

spark = get_spark_session()


def download_data_from_api(tickers: list[str], start_date: str, end_date: str) -> DataFrame:
    """
    Download data from Yahoo Finance API
    :param tickers: list: Tickers of the stocks
    :param start_date: str: Start date in the format 'YYYY-MM-DD'
    :param end_date: str: End date in the format 'YYYY-MM-DD'
    :return: pd.DataFrame: Dataframe with the stock data
    """
    data = yf.download(tickers, start=start_date, end=end_date or None)
    return spark.createDataFrame(data)


if __name__ == "__main__":
    download_data_from_api(["AAPL", "MSFT"], "2021-01-01", "2021-12-31").show()
