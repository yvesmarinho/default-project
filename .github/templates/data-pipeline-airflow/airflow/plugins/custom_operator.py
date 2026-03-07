"""
custom_operator.py — Example custom Airflow operator.

Demonstrates how to extend BaseOperator to encapsulate reusable
business logic. Credentials always come from Airflow Connections.
"""

from __future__ import annotations

import logging
from typing import Any, Sequence

from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context

log = logging.getLogger(__name__)


class CustomTransformOperator(BaseOperator):
    """
    Apply a Python callable as a transformation with structured logging.

    :param transform_fn: Callable that receives (record: dict) → dict.
    :param source_task_id: Task ID whose XCom output is the input list.
    :param conn_id: Optional Airflow Connection ID for destination writes.
    """

    template_fields: Sequence[str] = ("source_task_id",)

    def __init__(
        self,
        *,
        transform_fn,
        source_task_id: str,
        conn_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.transform_fn = transform_fn
        self.source_task_id = source_task_id
        self.conn_id = conn_id

    def execute(self, context: Context) -> list[dict]:
        ti = context["task_instance"]
        records: list[dict] = ti.xcom_pull(task_ids=self.source_task_id) or []

        log.info("CustomTransformOperator: processing %d records", len(records))
        transformed = [self.transform_fn(r) for r in records]
        log.info("CustomTransformOperator: produced %d records", len(transformed))

        if self.conn_id:
            self._write_to_destination(transformed)

        return transformed

    def _write_to_destination(self, records: list[dict]) -> None:
        """
        Write records using the configured Airflow Connection.
        Never access credentials directly — use get_connection().
        """
        from airflow.hooks.base import BaseHook

        conn = BaseHook.get_connection(self.conn_id)
        log.info(
            "Writing %d records to %s (conn_id=%s)",
            len(records),
            conn.host,
            self.conn_id,
        )
        # TODO: implement actual write logic using conn.host, conn.port,
        # conn.login, conn.password (fetched from Airflow's encrypted store)
