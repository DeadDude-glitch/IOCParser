#!/usr/bin/env python3

"""
Shared utilities for IOCParser modules.

Author: Marc Rivero | @seifreed
"""

from typing import Dict, List, Set, Union


def deduplicate_iocs(
    iocs: Dict[str, List[Union[str, Dict[str, str]]]],
) -> Dict[str, List[Union[str, Dict[str, str]]]]:
    """
    Remove duplicate IOCs while preserving order.

    Args:
        iocs: Dictionary of IOC type to list of IOC values

    Returns:
        Dictionary with deduplicated IOC lists
    """
    deduplicated: Dict[str, List[Union[str, Dict[str, str]]]] = {}

    for ioc_type, ioc_list in iocs.items():
        unique_items: List[Union[str, Dict[str, str]]] = []
        seen_keys: Set[str] = set()

        for item in ioc_list:
            key = str(sorted(item.items())) if isinstance(item, dict) else str(item)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_items.append(item)

        deduplicated[ioc_type] = unique_items

    return deduplicated


def deduplicate_iocs_with_state(
    new_iocs: Dict[str, List[str]],
    seen_iocs: Dict[str, Set[str]],
) -> Dict[str, List[str]]:
    """
    Remove duplicate IOCs using external state tracking.

    This function is designed for streaming/incremental deduplication
    where you need to track seen IOCs across multiple calls.

    Args:
        new_iocs: Newly extracted IOCs to deduplicate
        seen_iocs: State dictionary tracking already-seen IOCs (modified in place)

    Returns:
        Dictionary containing only the unique IOCs not seen before
    """
    unique_iocs: Dict[str, List[str]] = {}

    for ioc_type, ioc_list in new_iocs.items():
        unique = []
        for ioc in ioc_list:
            if ioc not in seen_iocs[ioc_type]:
                seen_iocs[ioc_type].add(ioc)
                unique.append(ioc)

        if unique:
            unique_iocs[ioc_type] = unique

    return unique_iocs
