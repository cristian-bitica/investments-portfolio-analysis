from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


def get_spark_session():
    packages = [
        "io.delta:delta-spark_2.12:3.3.0",
        "io.unitycatalog:unitycatalog-spark_2.12:0.2.0",
        "io.delta:delta-storage:3.3.0",
    ]
    # token is not required for local testing
    builder = (
        SparkSession.builder.appName("local-spark-uc")
        .master("local[*]")
        .config("spark.jars.packages", packages)
        # .config("spark.jars.packages", "io.unitycatalog:unitycatalog-spark_2.12:0.2.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.catalog.unity", "io.unitycatalog.spark.UCSingleCatalog")
        .config("spark.sql.catalog.unity.uri", "http://server:8080")
        .config("spark.sql.catalog.unity.token", "")
        .config("spark.sql.catalog.portfolio", "io.unitycatalog.spark.UCSingleCatalog")
        .config("spark.sql.catalog.portfolio.uri", "http://server:8080")
        .config("spark.sql.catalog.portfolio.token", "")
        .config("spark.sql.defaultCatalog", "unity")
        .config("spark.driver.host", "localhost")
    )
    return configure_spark_with_delta_pip(builder, packages).getOrCreate()
