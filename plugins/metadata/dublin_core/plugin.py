from pathlib import Path
from typing import Dict, Any


PLUGIN_ID = "metadata.dublin-core"


def apply_metadata(doc_metadata: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply Dublin Core defaults and normalization to a document metadata dict.

    :param doc_metadata: Existing document metadata (from YAML front matter).
    :param config: Dublin Core plugin configuration (e.g., required fields, defaults).
    :return: Updated metadata dict with Dublin Core fields applied.
    """
    result = dict(doc_metadata) if doc_metadata is not None else {}

    fields_cfg = config.get("fields", {}) if config else {}

    for field_name, field_spec in fields_cfg.items():
        default = field_spec.get("default")
        required = field_spec.get("required", False)

        if field_name not in result or result.get(field_name) in (None, "", []):
            if default is not None:
                result[field_name] = default
            elif required and field_name not in result:
                # Leave a placeholder for required-but-missing fields
                result[field_name] = "__REQUIRED_FIELD_MISSING__"

    return result
