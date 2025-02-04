from pyspark.sql import SparkSession


def get_spark_session():
    # token is not required for local testing
    return (
        SparkSession.builder.appName("local-uc-test")
        .master("local[*]")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.1")
        .config("spark.jars.packages", "io.unitycatalog:unitycatalog-spark_2.12:0.2.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "io.unitycatalog.spark.UCSingleCatalog")
        .config("spark.sql.catalog.unity", "io.unitycatalog.spark.UCSingleCatalog")
        .config("spark.sql.catalog.unity.uri", "http://localhost:8080")
        .config("spark.sql.catalog.unity.token", "")
        .config("spark.sql.defaultCatalog", "unity")
        .getOrCreate()
    )
