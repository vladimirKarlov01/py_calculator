from flask import Flask, jsonify, request

from src.calculator import CalculationError, Calculator

app = Flask(__name__)


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    expression = data.get("expression")
    if expression is None:
        return jsonify({"error": "No expression provided!"}), 400

    try:
        calculator = Calculator()
        result = calculator.evaluate(expression)
        return jsonify({"result": result})
    except CalculationError as e:
        return jsonify({"result": str(e)}), 200
    except Exception:
        return jsonify({"error": f"Invalid expression: {expression}"}), 422


if __name__ == "__main__":
    app.run(debug=True)
