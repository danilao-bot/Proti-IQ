"""
Security and input validation unit tests.
"""

import pytest
from fastapi import HTTPException
from api.security import validate_accession
from pipeline.export import sanitize_csv_cell


def test_valid_accessions():
    assert validate_accession("P12345") == "P12345"
    assert validate_accession("Q9ABC4") == "Q9ABC4"
    assert validate_accession("a0a0b2") == "A0A0B2"


def test_invalid_accessions_raise_error():
    with pytest.raises(HTTPException):
        validate_accession("../../../etc/passwd")

    with pytest.raises(HTTPException):
        validate_accession("P12345; DROP TABLE crops;--")

    with pytest.raises(HTTPException):
        validate_accession("P")  # too short


def test_csv_formula_injection_sanitization():
    assert sanitize_csv_cell("=1+1") == "'=1+1"
    assert sanitize_csv_cell("+cmd|' /C calc'!A0") == "'+cmd|' /C calc'!A0"
    assert sanitize_csv_cell("-10") == "'-10"
    assert sanitize_csv_cell("@SUM(A1:A10)") == "'@SUM(A1:A10)"
    assert sanitize_csv_cell("Cowpea") == "Cowpea"
