from flask import Blueprint, request, jsonify, render_template_string

app = Blueprint('stackLL',__name__,url_prefix='/stack_linked_list')

# ------------------------------
# Stack Data Structure
# ------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.addr = hex(id(self))  # Simulated memory address
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        """Push an element onto the stack"""
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        return f"Pushed {data} onto stack (addr: {new_node.addr})"

    def pop(self):
        """Pop the top element from the stack"""
        if not self.top:
            return "Stack Underflow — No element to pop."
        popped = self.top
        self.top = self.top.next
        return f"Popped {popped.data} from stack (addr: {popped.addr})"

    def to_list(self):
        """Return all stack elements from top to bottom"""
        result = []
        curr = self.top
        while curr:
            result.append({
                "data": curr.data,
                "addr": curr.addr,
                "next": curr.next.addr if curr.next else None
            })
            curr = curr.next
        return result


# Create global stack instance
stack = Stack()

# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stack Visualization</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2>🧱 Stack Visualization (Push & Pop with Memory Addresses)</h2>

        <div>
            <input type="text" id="value" placeholder="Enter value">
            <button onclick="push()">Push</button>
            <button onclick="pop()">Pop</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="1000" height="600"></canvas>

        <script>
            async function push() {
                let val = document.getElementById("value").value;
                if (!val) return alert("Enter a value to push");
                let res = await fetch('/push?value=' + val);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawStack(data.stack);
            }

            async function pop() {
                let res = await fetch('/pop');
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawStack(data.stack);
            }

            function drawStack(stack) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                let x = 450, y = 500;
                let boxHeight = 70;

                ctx.font = "14px Arial";

                if (stack.length === 0) {
                    ctx.fillText("Stack is empty", 430, 300);
                    return;
                }

                for (let i = 0; i < stack.length; i++) {
                    let node = stack[i];

                    // Draw stack box
                    ctx.strokeStyle = "#000";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y - boxHeight * i, 120, boxHeight);

                    // Draw data (top) and address (bottom)
                    ctx.fillText("Data: " + node.data, x + 10, y - boxHeight * i + 25);
                    ctx.fillText("Addr: " + node.addr, x + 10, y - boxHeight * i + 50);

                    // Draw link (next pointer)
                    if (node.next) {
                        ctx.beginPath();
                        ctx.moveTo(x + 60, y - boxHeight * i);
                        ctx.lineTo(x + 60, y - boxHeight * (i + 1));
                        ctx.stroke();

                        // Arrowhead
                        ctx.beginPath();
                        ctx.moveTo(x + 55, y - boxHeight * (i + 1) + 10);
                        ctx.lineTo(x + 60, y - boxHeight * (i + 1));
                        ctx.lineTo(x + 65, y - boxHeight * (i + 1) + 10);
                        ctx.stroke();
                    }
                }

                // Label top pointer
                ctx.fillStyle = "red";
                ctx.fillText("Top →", x - 70, y - boxHeight * (stack.length - 1) + 35);
            }

            // Load current stack on page load
            window.onload = async function() {
                let res = await fetch('/status');
                let data = await res.json();
                drawStack(data.stack);
            };
        </script>
    </body>
    </html>
    """)


@app.route('/push')
def push_value():
    value = request.args.get('value')
    msg = stack.push(value) if value else "No value provided."
    return jsonify({"message": msg, "stack": stack.to_list()})


@app.route('/pop')
def pop_value():
    msg = stack.pop()
    return jsonify({"message": msg, "stack": stack.to_list()})


@app.route('/status')
def get_status():
    return jsonify({"stack": stack.to_list()})


# ------------------------------
# Run the Server
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
