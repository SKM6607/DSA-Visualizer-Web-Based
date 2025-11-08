from flask import Blueprint, request, jsonify, render_template_string

infix_to_postfix_bp = Blueprint('infixToPostfix', __name__, url_prefix='/infix_to_postfix')

# ------------------------------
# Infix to Postfix Conversion Logic
# ------------------------------

precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

def infix_to_postfix(expression):
    """Convert infix expression to postfix and return each step"""
    stack = []
    output = []
    steps = []

    for char in expression:
        if char == ' ':
            continue
        if char.isalnum():  # Operand
            output.append(char)
            steps.append({
                "symbol": char,
                "action": "Added to output (operand)",
                "stack": stack.copy(),
                "output": output.copy()
            })
        elif char == '(':
            stack.append(char)
            steps.append({
                "symbol": char,
                "action": "Pushed '(' onto stack",
                "stack": stack.copy(),
                "output": output.copy()
            })
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
            steps.append({
                "symbol": char,
                "action": "Popped until '('",
                "stack": stack.copy(),
                "output": output.copy()
            })
        else:
            # Operator
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[char]:
                output.append(stack.pop())
            stack.append(char)
            steps.append({
                "symbol": char,
                "action": f"Pushed operator '{char}' onto stack",
                "stack": stack.copy(),
                "output": output.copy()
            })

    while stack:
        output.append(stack.pop())
        steps.append({
            "symbol": "-",
            "action": "Popped remaining operators",
            "stack": stack.copy(),
            "output": output.copy()
        })

    return "".join(output), steps


# ------------------------------
# Flask Routes
# ------------------------------

@infix_to_postfix_bp.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Infix to Postfix Visualizer</title>
        <style>
            body { font-family: Arial; background: #f8fafc; text-align: center; margin-top: 40px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
            #status { font-size: 16px; color: #333; margin: 10px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>🧠 Infix to Postfix Conversion Visualization</h2>
        <input type="text" id="expression" placeholder="Enter infix expression (e.g. A+B*(C-D))" size="40">
        <button onclick="convert()">Convert</button>
        <p id="status"></p>
        <canvas id="canvas" width="1100" height="500"></canvas>

        <script>
            async function convert() {
                let expr = document.getElementById("expression").value;
                if (!expr) return alert("Enter an infix expression");
                let res = await fetch('/infix_to_postfix/convert?expr=' + expr);
                let data = await res.json();
                document.getElementById("status").innerText = "Postfix Expression: " + data.postfix;
                animateSteps(data.steps);
            }

            async function animateSteps(steps) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                let i = 0;

                function drawStep(step) {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    ctx.font = "18px Arial";
                    ctx.fillText("Processing Symbol: " + step.symbol, 50, 40);
                    ctx.fillText("Action: " + step.action, 50, 70);

                    // Draw Stack
                    ctx.font = "16px Arial";
                    ctx.fillText("Stack:", 50, 120);
                    for (let j = 0; j < step.stack.length; j++) {
                        ctx.strokeRect(50, 150 + j * 40, 60, 40);
                        ctx.fillText(step.stack[j], 70, 178 + j * 40);
                    }

                    // Draw Output
                    ctx.fillText("Output:", 200, 120);
                    for (let j = 0; j < step.output.length; j++) {
                        ctx.strokeRect(200 + j * 50, 150, 50, 40);
                        ctx.fillText(step.output[j], 220 + j * 50, 178);
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

@infix_to_postfix_bp.route('/convert')
def convert_expression():
    expr = request.args.get('expr', '')
    postfix, steps = infix_to_postfix(expr)
    return jsonify({"postfix": postfix, "steps": steps})


# ------------------------------
# Run Flask App
# ------------------------------