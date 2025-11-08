from flask import Blueprint, jsonify, render_template_string, request
#DONE
balancing_symbol_bp = Blueprint('balancingSymbol', __name__, url_prefix='/balancing_symbol')
# -----------------------------
# Symbol Balance Logic (Detailed)
# -----------------------------
def is_balanced(expression):
    """Check if parentheses/brackets/braces are balanced and record all steps"""
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    steps = []

    for ch in expression:
        if ch in "([{":
            stack.append(ch)
            steps.append({
                "char": ch,
                "action": "push",
                "description": f"Pushed '{ch}' onto stack.",
                "stack": stack.copy()
            })
        elif ch in ")]}":
            if not stack:
                steps.append({
                    "char": ch,
                    "action": "error",
                    "description": f"No matching opening for '{ch}'. Stack is empty.",
                    "stack": stack.copy()
                })
                return False, steps
            if stack[-1] == pairs[ch]:
                popped = stack.pop()
                steps.append({
                    "char": ch,
                    "action": "pop",
                    "description": f"Popped '{popped}' because it matches '{ch}'.",
                    "stack": stack.copy()
                })
            else:
                steps.append({
                    "char": ch,
                    "action": "error",
                    "description": f"Top of stack '{stack[-1]}' does not match '{ch}'.",
                    "stack": stack.copy()
                })
                return False, steps
        else:
            steps.append({
                "char": ch,
                "action": "skip",
                "description": f"Ignored non-symbol character '{ch}'.",
                "stack": stack.copy()
            })

    if stack:
        steps.append({
            "char": None,
            "action": "error",
            "description": f"Unmatched opening symbols remain: {stack}.",
            "stack": stack.copy()
        })
        return False, steps

    steps.append({
        "char": None,
        "action": "done",
        "description": "All symbols processed — stack is empty. Expression is balanced!",
        "stack": stack.copy()
    })
    return True, steps


# -----------------------------
# Routes
# -----------------------------
@balancing_symbol_bp.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Balancing Symbols Visualizer (Step-by-Step)</title>
    <style>
        body { font-family: Arial; text-align: center; background: #eef2f7; }
        input, button { padding: 10px; margin: 5px; font-size: 16px; }
        canvas { border: 2px solid #333; background: #fff; margin-top: 20px; }
        h1 { margin-top: 30px; }
        .desc-box {
            width: 80%%;
            margin: 15px auto;
            padding: 10px;
            background: #fff3cd;
            border: 1px solid #856404;
            border-radius: 8px;
            color: #444;
            font-size: 16px;
        }
        .status {
            font-size: 22px;
            margin-top: 15px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>🧠 Step-by-Step Balancing Symbols Visualizer</h1>
    <input type="text" id="expr" placeholder="Enter expression e.g. (a+b)*[c-{d/e}]" size="45">
    <button onclick="checkBalance()">Check Balance</button>
    <p class="status" id="status"></p>
    <div id="desc" class="desc-box">Enter an expression to start the visualization.</div>
    <canvas id="canvas" width="950" height="400"></canvas>

    <script>
        let steps = [];
        let index = 0;
        let result = false;

        async function checkBalance() {
            const expr = document.getElementById('expr').value.trim();
            if (!expr) return alert("Please enter an expression.");
            const res = await fetch('/balancing_symbol/check?expr=' + encodeURIComponent(expr));
            const data = await res.json();

            steps = data.steps;
            result = data.result;
            index = 0;
            document.getElementById('status').innerText = "";
            document.getElementById('desc').innerText = "";
            drawStep();
            const interval = setInterval(() => {
                if (index < steps.length) {
                    drawStep();
                    index++;
                } else {
                    clearInterval(interval);
                    document.getElementById('status').innerText = result ?
                        "✅ Expression is BALANCED" : "❌ Expression is NOT balanced";
                }
            }, 900);
        }

        function drawStep() {
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (index >= steps.length) return;
            const step = steps[index];
            document.getElementById('desc').innerText = step.description;

            ctx.font = "20px Arial";
            ctx.fillText("Step " + (index + 1), 50, 40);
            if (step.char)
                ctx.fillText("Processing Symbol: '" + step.char + "'", 200, 40);

            // Draw stack visually
            const stack = step.stack;
            let x = 450, y = 350;

            ctx.font = "18px Arial";
            for (let i = 0; i < stack.length; i++) {
                ctx.fillStyle = "#87CEEB";
                ctx.strokeStyle = "#333";
                ctx.lineWidth = 2;
                ctx.fillRect(x - 35, y - (i * 45), 70, 40);
                ctx.strokeRect(x - 35, y - (i * 45), 70, 40);
                ctx.fillStyle = "#000";
                ctx.fillText(stack[i], x - 5, y - (i * 45) + 25);
            }

            // Label and action highlight
            ctx.font = "16px Arial";
            if (step.action === "push") {
                ctx.fillStyle = "blue";
                ctx.fillText("🧱 PUSH operation → added symbol to stack", 250, 80);
            } else if (step.action === "pop") {
                ctx.fillStyle = "green";
                ctx.fillText("✔ POP operation → matched pair found", 250, 80);
            } else if (step.action === "skip") {
                ctx.fillStyle = "gray";
                ctx.fillText("⏭ Non-symbol character skipped", 250, 80);
            } else if (step.action === "error") {
                ctx.fillStyle = "red";
                ctx.fillText("❌ ERROR → mismatch or missing symbol", 250, 80);
            } else if (step.action === "done") {
                ctx.fillStyle = "green";
                ctx.fillText("✅ SUCCESS → all symbols balanced", 250, 80);
            }
        }
    </script>
</body>
</html>
    """)

@balancing_symbol_bp.route('/check')
def check():
    expr = request.args.get("expr", "")
    balanced, steps = is_balanced(expr)
    return jsonify({"result": balanced, "steps": steps})
