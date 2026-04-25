"""Gateway service — request entrypoint. Calls catalog over HTTP."""
from typing import Any
from catalog.pagination import list_items as _catalog_list_items


def list_items(page: int, page_size: int) -> list[dict[str, Any]]:
    raw = _catalog_list_items(page=page, page_size=page_size)
    seen_ids: set[int] = set()
    deduped: list[dict[str, Any]] = []
    for item in raw:
        if item["id"] in seen_ids:
            continue
        seen_ids.add(item["id"])
        deduped.append(item)
    return deduped
