import pytest
import runpy
import unittest

from unittest.mock import patch
from io import StringIO
from drunk_polish_calculator import op_divide, op_multiply, op_minus, op_plus, main


class DrunkPolishCalculatorUnitTests(unittest.TestCase):
    def test_op_plus(self):
        # Test cases for op_plus function
        test_cases = [
            (5, 5, 10.0),
            (10, -3, 7.0),
            (0, 0, 0.0),
            (-2, 5, 3.0),
            (1.5, 2.5, 4)
        ]
        # when
        for x, y, expected in test_cases:
            result = op_plus(x, y)
            # then
            self.assertEqual(result, expected)

    def test_op_minus(self):
        # Test cases for op_minus function
        test_cases = [
            (10, 5, 5.0),
            (2, -3, 5.0),
            (-4, 7, -11.0),
            (-12, -5, -7.0),
            (1.5, 2.5, -1)
        ]
        # when
        for x, y, expected in test_cases:
            result = op_minus(x, y)
            # then
            self.assertEqual(result, expected)

    def test_op_multiply(self):
        # Test cases for op_multiply function
        test_cases = [
            (5, 5, 25.0),
            (2, -3, -6.0),
            (-4, 7, -28.0),
            (-12, -5, 60.0),
            (1.5, 2.5, 3.75)
        ]
        # when
        for x, y, expected in test_cases:
            result = op_multiply(x, y)
            # then
            self.assertEqual(result, expected)

    def test_op_divide(self):
        # Test cases for op_divide function
        test_cases = [
            (10, 5, 2.0),
            (2, -3, -0.6666666666666666),
            (-4, 7, -0.5714285714285714),
            (-12, -5, 2.4),
            (1.5, 2.5, 0.6)
        ]
        # when
        for x, y, expected in test_cases:
            result = op_divide(x, y)
            # then
            self.assertEqual(result, expected)

    def test_errors(self):
        # Test cases for op_plus function
        test_cases = [
            ("a", 5, TypeError),
            (5, "-", TypeError),
            ([4], 2, TypeError),
            (2, None, TypeError)
        ]
        # when
        for x, y, expected in test_cases:
            if isinstance(x, str) or isinstance(y, str):
                # If x or y are strings, expect TypeError
                with self.assertRaises(TypeError):
                    op_plus(x, y)


class TestDrunkPolishCalculator:
    # given
    @pytest.mark.parametrize("input_expression, expected_result", [
        ("5 5 +", "10.0"),
        ("10 -3 +", "7.0"),
        ("0 0 +", "0.0"),
        ("-2 5 +", "3.0"),
        ("10 5 -", "5.0"),
        ("2 -3 -", "5.0"),
        ("-4 7 -", "-11.0"),
        ("-12 -5 -", "-7.0"),
        ("10 5 *", "50.0"),
        ("10 5 /", "2.0"),
        ("6 2 *", "12.0"),
        ("3 5 *", "15.0"),
        ("12 4 /", "3.0"),
        ("2 3 + 4 *", "14.0"),
        ("8 2 / 4 +", "8.0"),
        ("10 2 + 3 *", "16.0"),
    ])
    def test_main_option(self, input_expression, expected_result):
        with patch("sys.stdin", StringIO(input_expression)), patch("sys.stdout", StringIO()) as output:
            runpy.run_path("/Users/borschevskyi/Hillel-Python-Pro/drunk_polish_calculator.py", run_name = "__main__")
            output.seek(0)
            result = output.read().strip().split(":")[-1].strip()
            assert result == expected_result

