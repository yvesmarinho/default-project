"""
example_pipeline.py — Template DAG for Apache Airflow.

Demonstrates:
  - DAG with retries, SLA, and email/slack alert callbacks
  - PythonOperator, BashOperator, BranchPythonOperator
  - XCom for inter-task communication
  - Connection-based credentials (never hardcoded)
  - TaskGroup for logical grouping
  - Dynamic task mapping pattern
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.task_group import TaskGroup

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default args — applied to every task unless overridden
# ---------------------------------------------------------------------------
DEFAULT_ARGS = {
    "owner": "data-team",
    "depends_on_past": False,
    "email_on_failure": False,  # use callbacks instead
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=1),
}


# ---------------------------------------------------------------------------
# Callbacks — centralised in utils/callbacks.py for reuse
# ---------------------------------------------------------------------------
def _on_failure(context):
    """Called on task failure. Send alert to Slack/PagerDuty/etc."""
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    log.error("Task failed: dag=%s task=%s", dag_id, task_id)
    # TODO: hook into alerting (see airflow/dags/utils/callbacks.py)


# ---------------------------------------------------------------------------
# DAG definition
# ---------------------------------------------------------------------------
@dag(
    dag_id="example_pipeline",
    description="Template pipeline — replace with real business logic",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args=DEFAULT_ARGS,
    on_failure_callback=_on_failure,
    tags=["template", "example"],
)
def example_pipeline():
    # ------------------------------------------------------------------
    # Step 1: Extract
    # ------------------------------------------------------------------
    @task(task_id="extract_data")
    def extract_data(**context) -> dict:
        """Pull data from source. Use Airflow Connections — never hardcode creds."""
        # Retrieve config from Airflow Variables (encrypted at rest)
        source_path = Variable.get("EXAMPLE_SOURCE_PATH", default_var="/tmp/source")
        log.info("Extracting from %s", source_path)
        # TODO: replace with actual extraction logic
        return {"record_count": 100, "source_path": source_path}

    # ------------------------------------------------------------------
    # Step 2: Validate — branch based on record count
    # ------------------------------------------------------------------
    def _branch_on_count(**context) -> str:
        ti = context["ti"]
        result = ti.xcom_pull(task_ids="extract_data")
        if result and result.get("record_count", 0) > 0:
            return "transform_group.transform_data"
        return "skip_empty"

    validate = BranchPythonOperator(
        task_id="validate_record_count",
        python_callable=_branch_on_count,
    )

    # ------------------------------------------------------------------
    # Step 3a: Skip path (empty extract)
    # ------------------------------------------------------------------
    skip = BashOperator(
        task_id="skip_empty",
        bash_command='echo "No records to process. Skipping pipeline."',
    )

    # ------------------------------------------------------------------
    # Step 3b: Transform group
    # ------------------------------------------------------------------
    with TaskGroup("transform_group") as transform_group:

        @task(task_id="transform_data")
        def transform_data(**context) -> dict:
            """Apply transformations. Return counts for downstream tasks."""
            ti = context["ti"]
            extract_result = ti.xcom_pull(task_ids="extract_data")
            log.info("Transforming %d records", extract_result["record_count"])
            # TODO: add real transformation logic
            return {"transformed_count": extract_result["record_count"]}

        @task(task_id="validate_transformed")
        def validate_transformed(**context) -> bool:
            ti = context["ti"]
            result = ti.xcom_pull(task_ids="transform_group.transform_data")
            assert result["transformed_count"] > 0, "Transformation produced no records"
            return True

        transform_data() >> validate_transformed()

    # ------------------------------------------------------------------
    # Step 4: Load
    # ------------------------------------------------------------------
    @task(task_id="load_data", trigger_rule="none_failed_min_one_success")
    def load_data(**context) -> None:
        """Write to destination using Airflow Connection (not raw credentials)."""
        ti = context["ti"]
        result = ti.xcom_pull(task_ids="transform_group.transform_data")
        if result:
            log.info("Loading %d records to destination", result["transformed_count"])
            # TODO: replace with actual load logic using Connection:
            # from airflow.hooks.base import BaseHook
            # conn = BaseHook.get_connection("my_destination_conn_id")
        else:
            log.info("No transformed data — nothing to load")

    # ------------------------------------------------------------------
    # Wire up
    # ------------------------------------------------------------------
    extracted = extract_data()
    extracted >> validate
    validate >> [transform_group, skip]
    transform_group >> load_data()


example_pipeline()
