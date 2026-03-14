"""lib/flows — UI flow wrappers (argparse.Namespace → int) para scaffold.py."""

from .check_links import flow_check_links
from .compose import flow_compose_profiles
from .dry_run import flow_dry_run
from .generate_infra import flow_generate_infra
from .generate_rules import flow_generate_rules
from .list_profiles import _load_descriptor, flow_list_profiles
from .new_project import flow_new_project
from .publish import flow_publish
from .release import flow_release
from .upgrade import flow_upgrade
from .validate import flow_validate

__all__ = [
    "flow_new_project",
    "flow_compose_profiles",
    "flow_upgrade",
    "flow_dry_run",
    "flow_generate_infra",
    "flow_check_links",
    "flow_publish",
    "flow_release",
    "flow_validate",
    "flow_generate_rules",
    "flow_list_profiles",
    "_load_descriptor",
]
