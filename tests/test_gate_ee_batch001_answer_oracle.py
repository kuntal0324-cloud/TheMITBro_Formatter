from __future__ import annotations

import json
import math
from pathlib import Path
import re

import sympy as sp

from src.gate_ee_batch_qualification import _question_markdown
from src.solution_validation import validate_solution


JSONL = Path("input/gate_ee_batch_001/BATCH_001_ENGINEERING_MATHEMATICS.jsonl")
QUESTIONS = {
    q["id"]: q
    for q in (json.loads(line) for line in JSONL.read_text(encoding="utf-8").splitlines() if line)
}


def q(number: int) -> dict:
    return QUESTIONS[f"TMB-GATE-EE-EM-{number:03d}"]


def test_all_twenty_answers_recompute_independently():
    x, y, t = sp.symbols("x y t", real=True)
    z = sp.symbols("z")

    matrix_1 = sp.Matrix([[2, 1], [1, 2]])
    assert max(matrix_1.eigenvals()) == 3
    assert q(1)["answer"] == "C" and q(1)["options"][2] == "3"

    matrix_2 = sp.Matrix([[1, 2], [3, 5]])
    assert sp.trace(matrix_2.inv()) == -6
    assert q(2)["answer"] == -6

    eigenvalue = sp.symbols("eigenvalue", real=True)
    assert sp.solve(eigenvalue**2 - eigenvalue, eigenvalue) == [0, 1]
    assert q(3)["answer"] == ["A", "B", "C"]

    assert sp.limit((sp.exp(2 * x) - 1 - 2 * x) / x**2, x, 0) == 2
    assert q(4)["answer"] == "B" and q(4)["options"][1] == "2"

    polynomial = x**3 - 3 * x**2 + 2
    candidates = [polynomial.subs(x, value) for value in (0, 2, 3)]
    assert min(candidates) == -2
    assert q(5)["answer"] == -2

    assert sp.integrate(x / (1 + x**2), (x, 0, 1)) == sp.log(2) / 2
    assert q(6)["answer"] == "B"

    ode_solution = 2 - sp.exp(-2 * x)
    assert sp.simplify(sp.diff(ode_solution, x) + 2 * ode_solution - 4) == 0
    assert ode_solution.subs(x, sp.log(2)) == sp.Rational(7, 4)
    assert math.isclose(q(7)["answer"], 1.75)

    candidates_8 = [sp.exp(-x), sp.exp(-3 * x), sp.exp(-2 * x), 2 * sp.exp(-x) - 5 * sp.exp(-3 * x)]
    valid_8 = [label for label, fn in zip("ABCD", candidates_8) if sp.simplify(sp.diff(fn, x, 2) + 4 * sp.diff(fn, x) + 3 * fn) == 0]
    assert valid_8 == ["A", "B", "D"] == q(8)["answer"]

    assert sp.expand((1 + sp.I) ** 4) == -4
    assert q(9)["answer"] == "B"

    roots = sp.solve(z**2 - 2 * z + 5, z)
    assert sp.simplify(sp.Abs(roots[0] - roots[1])) == 4
    assert q(10)["answer"] == 4

    union_probability = sp.Rational(3, 5) + sp.Rational(1, 2) - sp.Rational(3, 10)
    assert union_probability == sp.Rational(4, 5)
    assert q(11)["answer"] == "C"

    second_moment = sum(value**2 * probability for value, probability in ((0, 0.2), (1, 0.5), (2, 0.3)))
    assert math.isclose(second_moment, 1.7)
    assert math.isclose(q(12)["answer"], second_moment)

    mu, sigma2, a = sp.symbols("mu sigma2 a", real=True)
    assert sp.simplify(mu - mu) == 0
    assert sp.simplify((sigma2 + mu**2) - mu**2) == sigma2
    assert sp.simplify(a**2 * sigma2) == a**2 * sigma2
    assert q(13)["answer"] == ["A", "B", "C", "D"]

    b1 = sp.integrate(sp.sin(x) ** 2, (x, 0, sp.pi)) / sp.pi
    assert b1 == sp.Rational(1, 2)
    assert math.isclose(q(14)["answer"], 0.5)

    integrand = (z**2 + 1) / (z * (z - 1))
    contour_integral = 2 * sp.pi * sp.I * (sp.residue(integrand, z, 0) + sp.residue(integrand, z, 1))
    assert sp.simplify(contour_integral) == 2 * sp.pi * sp.I
    assert q(15)["answer"] == "B"

    assert 2 * 2 == 4 == q(16)["answer"]

    function_17 = x**2 * y + y**2
    gradient_17 = sp.Matrix([sp.diff(function_17, x), sp.diff(function_17, y)]).subs({x: 1, y: 2})
    direction_17 = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5)])
    assert gradient_17.dot(direction_17) == sp.Rational(32, 5)
    assert q(17)["answer"] == "B"

    field_p, field_q = y, -x
    assert sp.diff(field_p, x) + sp.diff(field_q, y) == 0
    assert sp.diff(field_q, x) - sp.diff(field_p, y) == -2
    circulation = sp.integrate(
        field_p.subs({x: sp.cos(t), y: sp.sin(t)}) * sp.diff(sp.cos(t), t)
        + field_q.subs({x: sp.cos(t), y: sp.sin(t)}) * sp.diff(sp.sin(t), t),
        (t, 0, 2 * sp.pi),
    )
    assert circulation == -2 * sp.pi
    assert q(18)["answer"] == ["A", "B", "D"]

    assert math.isclose(0.4 * (1 - 0.4), 0.24)
    assert math.isclose(q(19)["answer"], 0.24)

    heat_mode = 3 * sp.exp(-4 * t) * sp.sin(2 * x)
    value_20 = heat_mode.subs({x: sp.pi / 4, t: sp.log(2) / 4})
    assert value_20 == sp.Rational(3, 2)
    assert math.isclose(q(20)["answer"], 1.5)


def test_every_solution_has_one_plain_machine_detectable_final_answer():
    for question in QUESTIONS.values():
        markers = re.findall(r"(?m)^Final answer:\s*([^\n]+)$", question["solution"])
        assert len(markers) == 1, question["id"]
        assert not re.search(r"[$\\{}]", markers[0]), question["id"]
        assert validate_solution(_question_markdown(question)).status == "PASS", question["id"]
