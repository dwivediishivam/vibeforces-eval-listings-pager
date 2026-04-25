"""Regression test for the off-by-one pagination bug.

The agent must edit catalog/pagination.py so this passes.
"""
from gateway.gateway import list_items


def test_last_page_complete():
    page_size = 10
    pages = []
    for page in range(1, 6):
        pages.append(list_items(page=page, page_size=page_size))

    assert len(pages[0]) == 10, "page 1 should be full"
    assert len(pages[1]) == 10, "page 2 should be full"
    assert len(pages[2]) == 10, "page 3 should be full"
    assert len(pages[3]) == 10, "page 4 should be full"
    assert len(pages[4]) == 7, f"page 5 should contain the last 7 items, got {len(pages[4])}"
    all_ids = [item["id"] for page in pages for item in page]
    assert all_ids == list(range(1, 48)), "every id 1..47 must appear exactly once"


def test_no_duplicates_on_inner_pages():
    page = list_items(page=2, page_size=10)
    ids = [item["id"] for item in page]
    assert len(set(ids)) == len(ids)
