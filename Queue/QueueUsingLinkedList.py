from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------
# Queue Data Structure
# ------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.addr = hex(id(self))  # simulated memory address
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        """Add an element to the rear of the queue"""
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
            return f"Enqueued {data} as the first node (addr: {new_node.addr})"
        self.rear.next = new_node
        self.rear = new_node
        return f"Enqueued {data} at rear (addr: {new_node.addr})"

    def dequeue(self):
        """Remove an element from the front of the queue"""
        if self.front is None:
            return "Queue Underflow — No element to dequeue."
        removed_node = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return f"Dequeued {removed_node.data} (addr: {removed_node.addr})"

    def to_list(self):
        """Return all queue elements as list of dicts"""
        result = []
        curr = self.front
        while curr:
            result.append({
                "data": curr.data,
                "addr": curr.addr,
                "next": curr.next.addr if curr.next else None
            })
            curr = curr.next
        return result


# Create global queue instance
queue = Queue()

# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Queue Visualization</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2>📦 Queue Visualization (Enqueue & Dequeue with Front and Rear)</h2>

        <div>
            <input type="text" id="value" placeholder="Enter value">
            <button onclick="enqueue()">Enqueue</button>
            <button onclick="dequeue()">Dequeue</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="1200" height="500"></canvas>

        <script>
            async function enqueue() {
                let val = document.getElementById("value").value;
                if (!val) return alert("Enter a value to enqueue");
                let res = await fetch('/enqueue?value=' + val);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawQueue(data.queue);
            }

            async function dequeue() {
                let res = await fetch('/dequeue');
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawQueue(data.queue);
            }

            function drawQueue(queue) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                if (queue.length === 0) {
                    ctx.font = "20px Arial";
                    ctx.fillText("Queue is empty", 500, 250);
                    return;
                }

                let x = 150, y = 200;
                let boxWidth = 150, boxHeight = 80;

                ctx.font = "14px Arial";

                for (let i = 0; i < queue.length; i++) {
                    let node = queue[i];

                    // Draw node box
                    ctx.strokeStyle = "#000";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, boxWidth, boxHeight);

                    // Draw data and address
                    ctx.fillText("Data: " + node.data, x + 15, y + 30);
                    ctx.fillText("Addr: " + node.addr, x + 15, y + 55);

                    // Draw arrow to next node
                    if (i < queue.length - 1) {
                        ctx.beginPath();
                        ctx.moveTo(x + boxWidth, y + boxHeight / 2);
                        ctx.lineTo(x + boxWidth + 30, y + boxHeight / 2);
                        ctx.stroke();

                        // Arrowhead
                        ctx.beginPath();
                        ctx.moveTo(x + boxWidth + 30, y + boxHeight / 2);
                        ctx.lineTo(x + boxWidth + 20, y + boxHeight / 2 - 5);
                        ctx.lineTo(x + boxWidth + 20, y + boxHeight / 2 + 5);
                        ctx.fill();
                    }

                    x += boxWidth + 40;
                }

                // Draw Front and Rear labels
                ctx.fillStyle = "red";
                ctx.font = "16px Arial";
                ctx.fillText("Front →", 100, y + boxHeight / 2 + 5);
                ctx.fillText("Rear →", x - boxWidth - 10, y + boxHeight / 2 + 5);
            }

            // Load initial queue state
            window.onload = async function() {
                let res = await fetch('/status');
                let data = await res.json();
                drawQueue(data.queue);
            };
        </script>
    </body>
    </html>
    """)


@app.route('/enqueue')
def enqueue_value():
    value = request.args.get('value')
    msg = queue.enqueue(value) if value else "No value provided."
    return jsonify({"message": msg, "queue": queue.to_list()})


@app.route('/dequeue')
def dequeue_value():
    msg = queue.dequeue()
    return jsonify({"message": msg, "queue": queue.to_list()})


@avl_.route('/status')
def get_status():
    return jsonify({"queue": queue.to_list()})


# ------------------------------
# Run Server
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
