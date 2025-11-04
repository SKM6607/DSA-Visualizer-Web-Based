from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------
# Data Structure: Doubly Linked List
# ------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        self.addr = hex(id(self))  # Simulated memory address

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        """Insert a new node at the end"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return f"Inserted {data} as head node"
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        new_node.prev = current
        return f"Inserted node with value {data}"

    def delete(self, data):
        """Delete the first node with given data"""
        if not self.head:
            return "List is empty — nothing to delete."
        current = self.head
        while current and current.data != data:
            current = current.next
        if not current:
            return f"Node with value {data} not found."
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        if current.next:
            current.next.prev = current.prev
        return f"Deleted node with value {data} (addr: {current.addr})"

    def to_list(self):
        """Return structured list with data + address info"""
        result = []
        current = self.head
        while current:
            result.append({
                "data": current.data,
                "addr": current.addr,
                "prev": current.prev.addr if current.prev else None,
                "next": current.next.addr if current.next else None
            })
            current = current.next
        return result


# Create global doubly linked list instance
dll = DoublyLinkedList()

# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Doubly Linked List Visualizer</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
            .info { font-size: 14px; color: #333; }
        </style>
    </head>
    <body>
        <h2>🔗 Doubly Linked List Visualization (Data on Top, Address Below)</h2>

        <div>
            <input type="text" id="nodeValue" placeholder="Enter node value">
            <button onclick="insertNode()">Insert Node</button>
            <button onclick="deleteNode()">Delete Node</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="1600" height="500"></canvas>

        <script>
            async function insertNode() {
                let val = document.getElementById("nodeValue").value;
                if(!val) return alert("Enter a value");
                let res = await fetch('/insert?value=' + val);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawList(data.list);
            }

            async function deleteNode() {
                let val = document.getElementById("nodeValue").value;
                if(!val) return alert("Enter a value to delete");
                let res = await fetch('/delete?value=' + val);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawList(data.list);
            }

            function drawList(list) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                let x = 50, y = 150;

                if(list.length === 0) {
                    ctx.font = "22px Arial";
                    ctx.fillText("Doubly Linked List is empty", 600, 250);
                    return;
                }

                for(let i=0; i<list.length; i++) {
                    let node = list[i];

                    // Node box dimensions
                    let nodeWidth = 220;
                    let nodeHeight = 100;

                    // Outer box
                    ctx.strokeStyle = "#333";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, nodeWidth, nodeHeight);

                    // Dividers for Prev | Data+Addr | Next
                    ctx.beginPath();
                    ctx.moveTo(x + 60, y);
                    ctx.lineTo(x + 60, y + nodeHeight);
                    ctx.moveTo(x + 160, y);
                    ctx.lineTo(x + 160, y + nodeHeight);
                    ctx.stroke();

                    // Prev pointer (left section)
                    ctx.font = "14px Arial";
                    ctx.textAlign = "center";
                    ctx.fillText("Prev", x + 30, y + 30);
                    if (node.prev)
                        ctx.fillText(node.prev, x + 30, y + 65);
                    else
                        ctx.fillText("None", x + 30, y + 65);

                    // Data and address (center section)
                    ctx.font = "18px Arial";
                    ctx.fillText(node.data, x + 110, y + 35);
                    ctx.font = "14px Arial";
                    ctx.fillText(node.addr, x + 110, y + 65);

                    // Next pointer (right section)
                    ctx.font = "14px Arial";
                    ctx.fillText("Next", x + 190, y + 30);
                    if (node.next)
                        ctx.fillText(node.next, x + 190, y + 65);
                    else
                        ctx.fillText("None", x + 190, y + 65);

                    // Forward arrow (next)
                    if (i < list.length - 1) {
                        ctx.beginPath();
                        ctx.moveTo(x + nodeWidth, y + nodeHeight / 2);
                        ctx.lineTo(x + nodeWidth + 60, y + nodeHeight / 2);
                        ctx.stroke();

                        // Arrowhead (forward)
                        ctx.beginPath();
                        ctx.moveTo(x + nodeWidth + 60, y + nodeHeight / 2);
                        ctx.lineTo(x + nodeWidth + 50, y + nodeHeight / 2 - 5);
                        ctx.moveTo(x + nodeWidth + 60, y + nodeHeight / 2);
                        ctx.lineTo(x + nodeWidth + 50, y + nodeHeight / 2 + 5);
                        ctx.stroke();
                    }

                    // Backward arrow (prev)
                    if (i > 0) {
                        ctx.beginPath();
                        ctx.moveTo(x, y + nodeHeight / 2 + 20);
                        ctx.lineTo(x - 60 + 220, y + nodeHeight / 2 + 20);
                        ctx.strokeStyle = "#777";
                        ctx.stroke();

                        // Arrowhead (backward)
                        ctx.beginPath();
                        ctx.moveTo(x - 60 + 220, y + nodeHeight / 2 + 20);
                        ctx.lineTo(x - 50 + 220, y + nodeHeight / 2 + 15);
                        ctx.moveTo(x - 60 + 220, y + nodeHeight / 2 + 20);
                        ctx.lineTo(x - 50 + 220, y + nodeHeight / 2 + 25);
                        ctx.strokeStyle = "#777";
                        ctx.stroke();
                    }

                    x += 300; // spacing between nodes
                    ctx.strokeStyle = "#333"; // reset stroke color
                }
            }
        </script>
    </body>
    </html>
    """)


@app.route('/insert')
def insert_node():
    value = request.args.get('value')
    if value:
        msg = dll.insert(value)
    else:
        msg = "No value provided."
    return jsonify({"message": msg, "list": dll.to_list()})


@app.route('/delete')
def delete_node():
    value = request.args.get('value')
    if value:
        msg = dll.delete(value)
    else:
        msg = "No value provided for deletion."
    return jsonify({"message": msg, "list": dll.to_list()})


# ------------------------------
# Run Server
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
