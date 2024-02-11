from unittest import TestCase
from render_sysbnech import parse_latency
from render_sysbnech import parse_memory
from render_sysbnech import parse_cpu


class Test(TestCase):

    def test_extract_actors_and_participants(self):
        testcases = [
            {
                "latency_output": "23.521 |**************************************** 316",
                "expected": (23.521, 316)
            },
            {
                "latency_output": "23.948 |********                                 63",
                "expected": (23.948, 63)
            },
            {
                "latency_output": "24.384 |**                                       14",
                "expected": (24.384, 14)
            },
            {
                "latency_output": "24.827 |                                         2",
                "expected": (24.827, 2)
            },
            {
                "latency_output": "26.205 |*                                        5",
                "expected": (26.205, 5)
            }
        ]

        for case in testcases:
            actual = parse_latency(case['latency_output'])
            self.assertEqual(
                case["expected"],
                actual,
                "failed test expected {}, actual {}".format(case["expected"], actual),
            )

    def test_parse_memory(self):
        testcases = [
            {
                "latency_output": "10810.02 MiB transferred (1079.59 MiB/sec)",
                "expected": (10810.02, 1079.59)
            },
        ]

        for case in testcases:
            actual = parse_memory(case['latency_output'])
            self.assertEqual(
                case["expected"],
                actual,
                "failed test expected {}, actual {}".format(case["expected"], actual),
            )

    def test_parse_cpu(self):
        testcases = [
            {
                "latency_output": "events per second:    41.82",
                "expected": 41.82
            },
        ]

        for case in testcases:
            actual = parse_cpu(case['latency_output'])
            self.assertEqual(
                case["expected"],
                actual,
                "failed test expected {}, actual {}".format(case["expected"], actual),
            )
