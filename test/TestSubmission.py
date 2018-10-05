"""
This file uses the configuration.
"""

import unittest

class TestSubmission(unittest.TestCase):
    def test_submit_single(self):
        sub = Submission(conf)
        sub.run()

    def test_submit_multiple(self):
        sub = Submission(conf)
        sub.run()
