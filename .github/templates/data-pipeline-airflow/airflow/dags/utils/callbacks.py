"""
callbacks.py — Shared Airflow task/DAG callbacks.

Import in your DAGs:
  from dags.utils.callbacks import on_failure_slack, on_retry_log
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


def on_failure_log(context) -> None:
    """Minimal failure callback: logs structured context. Replace with alerting."""
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    execution_date = context["execution_date"]
    exception = context.get("exception")
    log.error(
        "TASK_FAILED | dag=%s task=%s execution_date=%s exception=%s",
        dag_id,
        task_id,
        execution_date,
        exception,
    )


def on_retry_log(context) -> None:
    """Log retry attempts with attempt number."""
    ti = context["task_instance"]
    log.warning(
        "TASK_RETRY | dag=%s task=%s attempt=%d",
        ti.dag_id,
        ti.task_id,
        ti.try_number,
    )


def on_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis) -> None:
    """Called when a task misses its SLA."""
    log.warning(
        "SLA_MISS | dag=%s tasks=%s",
        dag.dag_id,
        [t.task_id for t in task_list],
    )


# ---------------------------------------------------------------------------
# Slack callback (optional — requires apache-airflow-providers-slack)
# ---------------------------------------------------------------------------

def on_failure_slack(context) -> None:
    """
    Send a Slack alert on task failure.

    Prerequisites:
      1. Install: apache-airflow-providers-slack
      2. Create Airflow Connection: conn_id='slack_default',
         conn_type='slack', password=<Bot Token>

    Usage in DAG:
      default_args = {"on_failure_callback": on_failure_slack}
    """
    try:
        from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

        ti = context["task_instance"]
        message = (
            f":red_circle: *Task Failed*\n"
            f"*DAG*: `{ti.dag_id}`\n"
            f"*Task*: `{ti.task_id}`\n"
            f"*Execution*: `{context['execution_date']}`\n"
            f"*Log*: {ti.log_url}"
        )

        SlackWebhookOperator(
            task_id="slack_alert",
            slack_webhook_conn_id="slack_default",
            message=message,
        ).execute(context)
    except ImportError:
        log.warning(
            "slack callback: apache-airflow-providers-slack not installed. "
            "Falling back to log."
        )
        on_failure_log(context)
