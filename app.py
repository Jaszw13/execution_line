from flask import Flask, render_template, request
from execution_line import calculate_kill_line_risk

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # parse inputs with safe defaults
        region = request.form.get("region", "US")
        try:
            monthly_income = float(request.form.get("monthly_income", "0"))
        except ValueError:
            monthly_income = 0.0
        try:
            monthly_rigid_expenses = float(request.form.get("monthly_rigid_expenses", "0"))
        except ValueError:
            monthly_rigid_expenses = 0.0
        try:
            cash_savings = float(request.form.get("cash_savings", "0"))
        except ValueError:
            cash_savings = 0.0
        try:
            total_debt = float(request.form.get("total_debt", "0"))
        except ValueError:
            total_debt = 0.0
        try:
            net_assets = float(request.form.get("net_assets", "0"))
        except ValueError:
            net_assets = 0.0

        has_medical_insurance = request.form.get("has_medical_insurance") == "on"
        has_unemployment_insurance = request.form.get("has_unemployment_insurance") == "on"
        is_negative_equity = request.form.get("is_negative_equity") == "on"
        has_domestic_helper = request.form.get("has_domestic_helper") == "on"
        children_in_private_school = request.form.get("children_in_private_school") == "on"

        result = calculate_kill_line_risk(
            region=region,
            monthly_income=monthly_income,
            monthly_rigid_expenses=monthly_rigid_expenses,
            cash_savings=cash_savings,
            total_debt=total_debt,
            net_assets=net_assets,
            has_medical_insurance=has_medical_insurance,
            has_unemployment_insurance=has_unemployment_insurance,
            is_negative_equity=is_negative_equity,
            has_domestic_helper=has_domestic_helper,
            children_in_private_school=children_in_private_school,
        )

    return render_template("index.html", result=result)


if __name__ == "__main__":
    # run the app on localhost:5000
    app.run(debug=True)
