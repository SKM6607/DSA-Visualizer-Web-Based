from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------
# Data Structure: Queue using Array
# ------------------------------

class Queue:
    def __init__(self, size=7):
        self.queue = []
        self.max_size = size

    def enqueue(self, value):
        if len(self.queue) >= self.max_size:
            return "Queue Overflow! Cannot enqueue more elements."
        self.queue.append(value)
        return f"Enqueued value {value} to the queue."

    def dequeue(self):
        if not self.queue:
            return "Queue Underflow! Queue is empty."
        value = self.queue.pop(0)
        return f"Dequeued value {value} from the queue."

    def to_list(self):
        """Return structured data with index and address"""
        result = []
        for i, value in enumerate(self.queue):
            result.append({
                "index": i,
                "value": value,
                "addr": hex(id(value))
            })
        return result

# Global queue instance
queue = Queue(size=7)

# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Queue Visualization (Array Implementation)</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
            #status { font-size: 16px; color: #222; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h2>🚉 Queue Visualization (Array-Based Implementation)</h2>
        <div>
            <input type="text" id="queueValue" placeholder="Enter value">
            <button onclick="enqueueValue()">Enqueue</button>
            <button onclick="dequeueValue()">Dequeue</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="1000" height="400"></canvas>

        <script>
            async function enqueueValue() {
                let val = document.getElementById("queueValue").value;
                if (!val) return alert("Enter a value to enqueue.");
                let res = await fetch('/enqueue?value=' + val);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawQueue(data.queue);
            }

            async function dequeueValue() {
                let res = await fetch('/dequeue');
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawQueue(data.queue);
            }

            function drawQueue(queue) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                let x = 80, y = 150;
                let boxWidth = 150, boxHeight = 80;

                if (queue.length === 0) {
                    ctx.font = "20px Arial";
                    ctx.fillText("Queue is empty", 400, 200);
                    return;
                }

                for (let i = 0; i < queue.length; i++) {
                    let node = queue[i];

                    // Draw box
                    ctx.strokeStyle = "#333";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, boxWidth, boxHeight);

                    // Data and Address
                    ctx.font = "14px Arial";
                    ctx.fillText("Value: " + node.value, x + 10, y + 30);
                    ctx.fillText("Addr: " + node.addr, x + 10, y + 55);

                    // Draw arrows between boxes
                    if (i < queue.length - 1) {
                        ctx.beginPath();
                        ctx.moveTo(x + boxWidth, y + boxHeight / 2);
                        ctx.lineTo(x + boxWidth + 30, y + boxHeight / 2);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(x + boxWidth + 30, y + boxHeight / 2);
                        ctx.lineTo(x + boxWidth + 20, y + boxHeight / 2 - 5);
                        ctx.moveTo(x + boxWidth + 30, y + boxHeight / 2);
                        ctx.lineTo(x + boxWidth + 20, y + boxHeight / 2 + 5);
                        ctx.stroke();
                    }

                    // Front and Rear labels
                    if (i === 0) {
                        ctx.fillStyle = "red";
                        ctx.fillText("Front", x + 40, y - 10);
                        ctx.fillStyle = "black";
                    }
                    if (i === queue.length - 1) {
                        ctx.fillStyle = "blue";
                        ctx.fillText("Rear", x + 50, y + boxHeight + 20);
                        ctx.fillStyle = "black";
                    }

                    x += boxWidth + 40;
                }
            }
        </script>
    </body>
    </html>
    """)

@app.route('/enqueue')
def enqueue_value():
    value = request.args.get('value')
    if value:
        msg = queue.enqueue(value)
    else:
        msg = "No value provided for enqueue."
    return jsonify({"message": msg, "queue": queue.to_list()})

@app.route('/dequeue')
def dequeue_value():
    msg = queue.dequeue()
    return jsonify({"message": msg, "queue": queue.to_list()})

# ------------------------------
# Run Flask App
# ------------------------------

if __name__ == '__main__':
    app.run(debug=True)
