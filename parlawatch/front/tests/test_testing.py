# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from front.models import User


def test_dummy():
    """Assert that 23 + 42 = 65."""
    illuminati = 23
    answer = 42
    assert illuminati + answer == 65


@pytest.mark.django_db
def test_database():
    """Check whether database access works."""
    assert User.objects.count() == 0
    User.objects.create(username='dummy', email='dummy@example.com')
    assert User.objects.count() == 1
