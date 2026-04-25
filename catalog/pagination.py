"""Catalog service pagination.

In production, `_fetch_rows` runs SQL like:
    SELECT * FROM items ORDER BY id LIMIT %s OFFSET %s
"""
TOTAL_ITEMS = 47


def _fetch_rows(limit: int, offset: int) -> list[dict]:
    items = [{"id": i, "name": f"item-{i}"} for i in range(1, TOTAL_ITEMS + 1)]
    return items[offset : offset + limit]


def list_items(page: int, page_size: int) -> list[dict]:
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be >= 1")
    # BUG: off-by-one in the offset computation. The +1 drops one item per
    # page. On inner pages the gateway's id-dedup masks it (it never
    # actually fires here, but the symptom would be visible in any system
    # that joined results). On the LAST partial page it is exposed: page 5
    # of 47 with size 10 returns 5 items instead of 7.
    offset = (page - 1) * page_size + 1
    return _fetch_rows(limit=page_size, offset=offset)
