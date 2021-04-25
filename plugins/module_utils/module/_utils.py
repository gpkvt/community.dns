# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2021 Felix Fontein
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This module_utils is PRIVATE and should only be used by this collection. Breaking changes can occur any time.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible_collections.community.dns.plugins.module_utils.names import (
    split_into_labels,
    join_labels,
    normalize_label,
)

from ansible_collections.community.dns.plugins.module_utils.zone_record_api import (
    DNSAPIError,
)


def normalize_dns_name(name):
    if name is None:
        return name
    labels, dummy = split_into_labels(name)
    return join_labels([normalize_label(label) for label in labels])


def get_prefix(normalized_zone, normalized_record=None, prefix=None):
    # If normalized_record is not specified, use prefix
    if normalized_record is None:
        if prefix is not None:
            prefix = normalize_dns_name(prefix)
            if prefix == '':
                prefix = None
        return (prefix + '.' + normalized_zone) if prefix else normalized_zone, prefix
    # Convert record to prefix
    if not normalized_record.endswith('.' + normalized_zone) and normalized_record != normalized_zone:
        raise DNSAPIError('Record must be in zone')
    if normalized_record == normalized_zone:
        return normalized_record, None
    else:
        return normalized_record, normalized_record[:len(normalized_record) - len(normalized_zone) - 1]