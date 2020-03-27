# -*- coding: utf-8 -*-
"""Functional Maxes unit tests"""


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
        assert b"Squat Max" in r.data
        assert b"315" in r.data
        assert b"Bench Max" in r.data
        assert b"225" in r.data
        assert b"Deadlift Max" in r.data
        assert b"405" in r.data
        assert b"Press Max" in r.data
        assert b"135" in r.data

    def test_valid_max_submission(self, test_client, init_database):
        """
        GIVEN a Flask application
        WHEN the '/maxes' page is posted to (POST)
        THEN check the response is valid
        """
        with test_client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["_fresh"] = True
        r = test_client.post(
            "/max",
            data=dict(squat=325, bench=235, deadlift=415, press=145),
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"325" in r.data
        assert b"235" in r.data
        assert b"415" in r.data
        assert b"145" in r.data
