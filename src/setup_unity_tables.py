from delta import DeltaTable
from pyspark.sql.types import DoubleType, StringType, StructField, StructType

from spark_session import get_spark_session

spark = get_spark_session()


def create_delta_table():
    schema = StructType(
        [
            StructField("symbol", StringType(), False),
            StructField("name", StringType(), False),
            StructField("sector", StringType(), False),
            StructField("price", DoubleType(), False),
        ]
    )
    DeltaTable.createIfNotExists(spark).addColumns(schema).tableName("bronze.raw_stocks").execute()


# def create_delta_table():
#     spark.sql(
#         """
#         CREATE TABLE IF NOT EXISTS portfolio.bronze.raw_stocks
#         (symbol STRING, name STRING, sector STRING, price DOUBLE)
#         USING delta
#         """
#     )


def create_medallion_schemas():
    spark.sql("CREATE SCHEMA IF NOT EXISTS portfolio.bronze;")
    spark.sql("CREATE SCHEMA IF NOT EXISTS portfolio.silver;")
    spark.sql("CREATE SCHEMA IF NOT EXISTS portfolio.gold;")


def create_portfolio_catalog():
    spark.sql("CREATE CATALOG IF NOT EXISTS portfolio")
    spark.sql("USE CATALOG portfolio")


if __name__ == "__main__":
    create_portfolio_catalog()

    create_medallion_schemas()
    print(spark.catalog.currentCatalog())
    print(spark.catalog.currentDatabase())
    create_delta_table()
    spark.stop()
