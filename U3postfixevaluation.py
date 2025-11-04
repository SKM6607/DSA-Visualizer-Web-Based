from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------
# Postfix Evaluation Logic
# ------------------------------

def evaluate_postfix(expression):
    """Evaluate a postfix expression and record visualization steps"""
    stack = []
    steps = []

    for char in expression:
        if char == ' ':
            continue
        if char.isdigit():
            stack.append(int(char))
            steps.append({
                "symbol": char,
                "action": f"Pushed {char} to stack (operand)",
                "stack": stack.copy()
            })
        elif char in "+-*/^":
            if len(stack) < 2:
                steps.append({
                    "symbol": char,
                    "action": "Error: insufficient operands",
                    "stack": stack.copy()
                })
                continue
            b = stack.pop()
            a = stack.pop()

            if char == '+': result = a + b
            elif char == '-': result = a - b
            elif char == '*': result = a * b
            elif char == '/': result = a / b
            elif char == '^': result = a ** b

            stack.append(result)
            steps.append({
                "symbol": char,
                "action": f"Applied operator {char}: {a} {char} {b} = {result}",
                "stack": stack.copy()
            })
        else:
            steps.append({
                "symbol": char,
                "action": f"Ignored invalid symbol '{char}'",
                "stack": stack.copy()
            })

    final_result = stack[-1] if stack else None
    return final_result, steps


# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Postfix Evaluation Visualizer</title>
        <style>
            body { font-family: Arial; background: #f8fafc; text-align: center; margin-top: 40px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
            #status { font-size: 16px; color: #222; margin: 10px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>🧮 Postfix Expression Evaluation Visualization</h2>
        <input type="text" id="expression" placeholder="Enter postfix (e.g., 231*+9-)" size="40">
        <button onclick="evaluate()">Evaluate</button>
        <p id="status"></p>
        <canvas id="canvas" width="1000" height="500"></canvas>

        <script>
            async function evaluate() {
                let expr = document.getElementById("expression").value;
                if (!expr) return alert("Enter a postfix expression");
                let res = await fetch('/evaluate?expr=' + expr);
                let data = await res.json();
                document.getElementById("status").innerText = "Final Result: " + data.result;
                animateSteps(data.steps);
            }

            function animateSteps(steps) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                let i = 0;

                function drawStep(step) {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    ctx.font = "18px Arial";
                    ctx.fillText("Processing Symbol: " + step.symbol, 50, 40);
                    ctx.fillText("Action: " + step.action, 50, 70);

                    // Draw Stack Visualization
                    ctx.font = "16px Arial";
                    ctx.fillText("Stack:", 50, 120);
                    for (let j = 0; j < step.stack.length; j++) {
                        ctx.strokeRect(50, 150 + j * 50, 100, 50);
                        ctx.fillText(step.stack[j], 85, 180 + j * 50);
                    }
                }

                function stepThrough() {
                    if (i < steps.length) {
                        drawStep(steps[i]);
                        i++;
                        setTimeout(stepThrough, 1500);
                    }
                }
                stepThrough();
            }
        </script>
    </body>
    </html>
    """)

@app.route('/evaluate')
def evaluate_expression():
    expr = request.args.get('expr', '')
    result, steps = evaluate_postfix(expr)
    return jsonify({"result": result, "steps": steps})


# ------------------------------
# Run Flask App
# ------------------------------

if __name__ == '__main__':
    app.run(debug=True)
