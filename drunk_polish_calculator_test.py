import runpy
from unittest.mock import patch
from io import StringIO
import pytest

from drunk_polish_calculator import op_plus, op_minus, op_multiply, op_divide


class TestDrunkPolishCalculator:
    # given
    @pytest.mark.parametrize(
        "x, y, expected",
        [
            (5, 5, 10.0),
            (10, -3, 7.0),
            (0, 0, 0.0),
            (-2, 5, 3.0),
            (1.5, 2.5, 4)
        ],
    )
    def test_op_plus(self, x, y, expected):
        # when
        result = op_plus(x, y)
        # then
        assert result == expected

    # given
    @pytest.mark.parametrize(
        "x, y, expected",
        [
            (15, 5, -10.0),
            (2, -3, -5.0),
            (-4, 7, 11.0),
            (-12, -5, 7.0),
            (1.5, 2.5, 1)
        ],
    )
    def test_op_minus(self, x, y, expected):
        # when
        result = op_minus(x, y)
        # then
        assert result == expected

    # given
    @pytest.mark.parametrize(
        "x, y, expected",
        [
            (5, 5, 25.0),
            (2, -3, -6.0),
            (-4, 7, -28.0),
            (-12, -5, 60.0),
            (1.5, 2.5, 3.75),
        ],
    )
    def test_op_multiply(self, x, y, expected):
        # when
        result = op_multiply(x, y)
        # then
        assert result == expected

    # given
    @pytest.mark.parametrize(
        "x, y, expected",
        [
            (10, 5, 2.0),
            (2, -3, -0.6666666666666666),
            (-4, 7, -0.5714285714285714),
            (-12, -5, 2.4),
            (1.5, 2.5, 0.6),
        ],
    )
    def test_op_divide(self, x, y, expected):
        # when
        result = op_divide(x, y)
        # then
        assert result == expected

    # given
    @pytest.mark.parametrize(
        "input_expression, expected_result",
        [
            ("5 5 +", "10.0"),
            ("10 -3 +", "7.0"),
            ("0 0 +", "0.0"),
            ("-2 5 +", "3.0"),
            ("10 5 -", "5.0"),
            ("-4 7 -", "-11.0"),
            ("-12 -5 -", "-7.0"),
            ("10 5 *", "50.0"),
            ("10 5 /", "2.0"),
            ("6 2 *", "12.0"),
            ("3 5 *", "15.0"),
            ("12 4 /", "3.0"),
            ("2 3 + 4 *", "20.0"),
            ("8 2 / 4 +", "8.0"),
            ("10 2 + 3 *", "36.0"),
        ],
    )
    def test_main(self, input_expression, expected_result, capsys):
        # when
        with patch("sys.stdin", StringIO(input_expression)):
            runpy.run_path(
                "./drunk_polish_calculator.py",
                run_name="__main__",
            )
            captured = capsys.readouterr()
            result = captured.out.strip().split(":")[-1].strip()
            # then
            assert result == expected_result
