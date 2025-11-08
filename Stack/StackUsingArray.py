from flask import Blueprint, request, jsonify, render_template_string

#avl_bp = Blueprint('avl', __name__, url_prefix='/avl'
stack_array = Blueprint('stackArr', __name__, url_prefix='/stack_array')

# ------------------------------
# Data Structure: Stack using Array
# ------------------------------

class Stack:
    def __init__(self, size=10):
        self.stack = []
        self.max_size = size

    def push(self, value):
        if len(self.stack) >= self.max_size:
            return "Stack Overflow! Cannot push more elements."
        self.stack.append(value)
        return f"Pushed value {value} onto the stack."

    def pop(self):
        if not self.stack:
            return "Stack Underflow! Stack is empty."
        value = self.stack.pop()
        return f"Popped value {value} from the stack."

    def to_list(self):
        """Return stack representation with index and address"""
        result = []
        for i, value in enumerate(self.stack):
            result.append({
                "index": i,
                "value": value,
                "addr": hex(id(value))
            })
        return result


# Global stack instance
stack = Stack(size=7)

# ------------------------------
# Flask Routes
# ------------------------------

@stack_array.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stack Visualization (Array Implementation)</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
            #status { font-size: 16px; color: #222; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>📦 Stack Visualization (Array-Based Implementation)</h2>
        <div>
            <input type="text" id="stackValue" placeholder="Enter value">
            <button onclick="pushValue()">Push</button>
            <button onclick="popValue()">Pop</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="600" height="500"></canvas>

        <script>
            async function pushValue() {
                let val = document.getElementById("stackValue").value;
                if (!val) return alert("Enter a value to push.");
                let res = await fetch('/stack_array/push?value=' + val);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawStack(data.stack);
            }

            async function popValue() {
                let res = await fetch('/stack_array/pop');
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawStack(data.stack);
            }

            function drawStack(stack) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                let startY = 400;
                let boxHeight = 60;
                let boxWidth = 200;

                ctx.font = "15px Arial";
                ctx.fillText("Top →", 260, startY - (stack.length * boxHeight) - 20);

                if (stack.length === 0) {
                    ctx.font = "20px Arial";
                    ctx.fillText("Stack is empty", 220, 250);
                    return;
                }

                for (let i = stack.length - 1; i >= 0; i--) {
                    let node = stack[i];
                    let y = startY - ((stack.length - 1 - i) * boxHeight);

                    // Draw box
                    ctx.strokeStyle = "#333";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(200, y - boxHeight, boxWidth, boxHeight);

                    // Draw text (value and address)
                    ctx.font = "14px Arial";
                    ctx.fillText("Value: " + node.value, 210, y - 30);
                    ctx.fillText("Addr: " + node.addr, 210, y - 10);

                    if (i === stack.length - 1) {
                        ctx.fillStyle = "blue";
                        ctx.fillText("← Top", 410, y - 30);
                        ctx.fillStyle = "black";
                    }
                }
            }
        </script>
    </body>
    </html>
    """)

@stack_array.route('/push',methods=['GET','POST'])
def push_value():
    value = request.args.get('value')
    if value:
        msg = stack.push(value)
    else:
        msg = "No value provided for push."
    return jsonify({"message": msg, "stack": stack.to_list()})

@stack_array.route('/pop',methods=['GET','POST'])
def pop_value():
    msg = stack.pop()
    return jsonify({"message": msg, "stack": stack.to_list()})

# ------------------------------
# Run Flask App
# ------------------------------
