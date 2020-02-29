# -*- coding: utf-8 -*-
"""Functional Maxes unit tests"""
from loguru import logger


class TestMaxes:
    """Maxes tests"""

    def test_maxes_page(self, test_client, init_database):
        """
        GIVEN a Flask application
        WHEN the '/maxes' page is requested (GET)
        THEN check the response is valid
        """
        with test_client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["_fresh"] = True

        r = test_client.get("/max")
        assert r.status_code == 200

    def test_valid_max_submission(self, test_client, init_database):
        """
        GIVEN a Flask application
        WHEN the '/maxes' page is requested (POST)
        THEN check the response is valid
        """
        with test_client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["_fresh"] = True
