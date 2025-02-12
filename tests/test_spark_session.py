from pyspark.sql.catalog import Catalog
from tests.conftest import SparkTestingContext
from src.spark_session import get_spark_session


def test_get_spark_session():
    spark = get_spark_session()
    assert spark is not None
    assert spark.conf.get("spark.sql.catalog.unity.uri") == "http://server:8080"
    assert spark.conf.get("spark.sql.catalog.unity.token") == ""
    assert spark.conf.get("spark.sql.defaultCatalog") == "unity"
    assert spark.conf.get("spark.sql.extensions") == "io.delta.sql.DeltaSparkSessionExtension"
    assert Catalog(spark).currentCatalog() == "unity"
    spark.stop()


def test_spark_testing_session(spark_testing_context: SparkTestingContext):
    spark = spark_testing_context.spark
    assert spark is not None
    assert spark.conf.get("spark.sql.catalog.unity.uri") == "http://server:8080"
    assert spark.conf.get("spark.sql.catalog.unity.token") == ""
    assert spark.conf.get("spark.sql.defaultCatalog") == "unity"
    assert spark.conf.get("spark.sql.extensions") == "io.delta.sql.DeltaSparkSessionExtension"
    assert Catalog(spark).currentCatalog() == "unity"
    spark.stop()