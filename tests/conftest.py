import os
import pathlib
import shutil
import sys
from typing import NamedTuple

from delta import configure_spark_with_delta_pip
import pytest
from pyspark.sql import SparkSession

# os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-arm64/"
# os.environ["PATH"] = f"{os.environ['JAVA_HOME']}/bin:{os.environ['PATH']}"
# os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
# os.environ["SPARK_HOME"] = "../.venv/lib/python3.12/site-packages/pyspark/"
DELTA_JAR = (pathlib.Path(__file__).parent / "delta-spark_2.13-3.3.0.jar").absolute()
UC_JAR = (pathlib.Path(__file__).parent / "unitycatalog-spark_2.13-0.2.1.jar").absolute()


class TestingContext(NamedTuple):
    data_dir: str


class SparkTestingContext(NamedTuple):
    ctx: TestingContext
    spark: SparkSession


@pytest.fixture(scope="session", autouse=True)
def testing_context(tmp_path_factory) -> TestingContext:
    data_dir = tmp_path_factory.mktemp("data_dir")

    yield TestingContext(str(data_dir))

    shutil.rmtree(data_dir)


@pytest.fixture(scope="session")
def spark_testing_context(testing_context, tmp_path_factory):
    packages = [
        "io.delta:delta-spark_2.12:3.3.0",
        "io.unitycatalog:unitycatalog-spark_2.12:0.2.1",
        "io.delta:delta-storage:3.3.0",
    ]
    spark = (
        SparkSession.builder.appName("TestSession")
        .master("local[1]")
        .config(
            "spark.driver.extraJavaOptions",
            " ".join(["-Ddelta.log.cacheSize=3", "-XX:+CMSClassUnloadingEnabled", "-XX:+UseCompressedOops"]),
        )
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.databricks.delta.snapshotPartitions", "2")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.ui.enabled", "false")
        .config("spark.ui.dagGraph.retainedRootRDDs", "1")
        .config("spark.ui.retainedJobs", "1")
        .config("spark.ui.retainedStages", "1")
        .config("spark.ui.retainedTasks", "1")
        .config("spark.sql.ui.retainedExecutions", "1")
        .config("spark.worker.ui.retainedExecutors", "1")
        .config("spark.worker.ui.retainedDrivers", "1")
        .config("spark.driver.memory", "2g")
        .config("spark.sql.warehouse.dir", str(tmp_path_factory.mktemp("warehouse").absolute()))
        # .config("spark.jars.packages", packages)
        .config("spark.sql.catalog.unity", "io.unitycatalog.spark.UCSingleCatalog")
        .config("spark.sql.catalog.unity.uri", "http://server:8080")
        .config("spark.sql.catalog.unity.token", "")
        .config("spark.sql.catalog.portfolio", "io.unitycatalog.spark.UCSingleCatalog")
        .config("spark.sql.catalog.portfolio.uri", "http://server:8080")
        .config("spark.sql.catalog.portfolio.token", "")
        .config("spark.sql.defaultCatalog", "unity")
        .config("spark.driver.host", "127.0.0.1")

    )
    spark = configure_spark_with_delta_pip(spark, packages).getOrCreate()

    spark.sparkContext.setCheckpointDir(str(tmp_path_factory.mktemp("checkpoints").absolute()))

    yield SparkTestingContext(ctx=testing_context, spark=spark)

    spark.stop()
