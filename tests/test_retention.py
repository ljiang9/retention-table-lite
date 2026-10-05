import unittest

from retention import build_retention, render_markdown


EVENTS = [
    ("u1", 0), ("u2", 0), ("u3", 0), ("u4", 0),
    ("u1", 1), ("u2", 1), ("u3", 1),
    ("u1", 2), ("u2", 2),
    ("u5", 1), ("u6", 1), ("u7", 1),
    ("u5", 2), ("u6", 2),
    ("u5", 3),
]


class TestRetention(unittest.TestCase):
    def setUp(self):
        self.t = build_retention(EVENTS)

    def test_cohorts(self):
        # cohort 0 与 cohort 1
        self.assertEqual(self.t["cohorts"], ["0", "1"])

    def test_first_period_always_100(self):
        for row in self.t["matrix"]:
            self.assertEqual(row[0], 100.0)

    def test_cohort0_size(self):
        # cohort 0 = u1,u2,u3,u4 = 4
        self.assertEqual(self.t["sizes"][0], 4)

    def test_cohort0_d1(self):
        # cohort0 在 +1 活跃: u1,u2,u3 = 3/4 = 75%
        self.assertEqual(self.t["matrix"][0][1], 75.0)

    def test_cohort0_d2(self):
        # cohort0 在 +2 活跃: u1,u2 = 2/4 = 50%
        self.assertEqual(self.t["matrix"][0][2], 50.0)

    def test_cohort1_d1(self):
        # cohort1 在 +1: u5,u6 = 2/3 ≈ 66.7%
        self.assertAlmostEqual(self.t["matrix"][1][1], 66.7, places=1)

    def test_render(self):
        md = render_markdown(self.t)
        self.assertIn("| Cohort | 规模 |", md)
        self.assertIn("75.0%", md)


if __name__ == "__main__":
    unittest.main()
