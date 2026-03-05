"""A very small command-line/demo driver for the kill‑line calculator.

This module simply runs a couple of hardcoded examples when invoked directly.

To launch the web interface, run ``python -m app`` or ``python app.py``
from the project root after installing the dependencies (``pip install -r
requirements.txt``).
"""

from execution_line import calculate_kill_line_risk


if __name__ == "__main__":
    print("Running CLI demo of calculate_kill_line_risk()")
    print(calculate_kill_line_risk(
        region='US',
        monthly_income=5000,
        monthly_rigid_expenses=4000,
        cash_savings=500,
        total_debt=300000,
        net_assets=100000,
        has_medical_insurance=False,
        has_unemployment_insurance=False
    ))
    print(calculate_kill_line_risk(
        region='HK',
        monthly_income=20000,
        monthly_rigid_expenses=15000,
        cash_savings=20000,
        total_debt=0,
        net_assets=1000000,
        has_medical_insurance=True,
        has_unemployment_insurance=False,
        is_negative_equity=False,
        has_domestic_helper=True,
        children_in_private_school=False
    ))
