# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Optional post-publish jobs for Dataflow Gen2 (ApplyChanges, Refresh)."""

import logging

from fabric_cicd import FabricWorkspace

logger = logging.getLogger(__name__)

JOB_TYPE_APPLY_CHANGES = "ApplyChanges"
JOB_TYPE_REFRESH = "Refresh"


def run_dataflow_job(
    fabric_workspace_obj: FabricWorkspace,
    item_guid: str,
    item_name: str,
    job_type: str,
) -> None:
    """Start an on-demand dataflow job and wait for completion."""
    url = (
        f"{fabric_workspace_obj.base_api_url}/items/{item_guid}"
        f"/jobs/instances?jobType={job_type}"
    )
    logger.info(f"{item_name}: starting dataflow job {job_type}")
    fabric_workspace_obj.endpoint.invoke(method="POST", url=url, body="{}")
    logger.info(f"{item_name}: completed dataflow job {job_type}")


def run_post_publish_dataflow_jobs(
    fabric_workspace_obj: FabricWorkspace,
    item_guid: str,
    item_name: str,
) -> None:
    """Run optional ApplyChanges / Refresh after a dataflow definition publish."""
    if fabric_workspace_obj.apply_dataflow_changes:
        run_dataflow_job(fabric_workspace_obj, item_guid, item_name, JOB_TYPE_APPLY_CHANGES)
    if fabric_workspace_obj.refresh_dataflows:
        run_dataflow_job(fabric_workspace_obj, item_guid, item_name, JOB_TYPE_REFRESH)
