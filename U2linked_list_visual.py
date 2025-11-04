from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------
# Data Structure: Singly Linked List
# ------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.addr = hex(id(self))  # Simulated memory address

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        """Insert a new node at the end of the linked list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return f"Inserted {data} as head node"
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        return f"Inserted node with value {data}"

    def delete(self, data):
        """Delete the first node with given data"""
        if not self.head:
            return "List is empty — nothing to delete."
        if self.head.data == data:
            deleted_addr = self.head.addr
            self.head = self.head.next
            return f"Deleted head node with value {data} (addr: {deleted_addr})"
        current = self.head
        prev = None
        while current and current.data != data:
            prev = current
            current = current.next
        if current is None:
            return f"Node with value {data} not found."
        prev.next = current.next
        return f"Deleted node with value {data} (addr: {current.addr})"

    def to_list(self):
        """Return structured list with data + address info"""
        result = []
        current = self.head
        while current:
            result.append({
                "data": current.data,
                "addr": current.addr,
                "next": current.next.addr if current.next else None
            })
            current = current.next
        return result


# Create global linked list instance
linked_list = LinkedList()

# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Singly Linked List Visualizer</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
            .info { font-size: 14px; color: #333; }
        </style>
    </head>
    <body>
        <h2>🧠 Singly Linked List Visualization (Data on Top, Address Below)</h2>

        <div>
            <input type="text" id="nodeValue" placeholder="Enter node value">
            <button onclick="insertNode()">Insert Node</button>
            <button onclick="deleteNode()">Delete Node</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="1500" height="500"></canvas>

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
                    ctx.fillText("Linked List is empty", 550, 250);
                    return;
                }

                for(let i=0; i<list.length; i++) {
                    let node = list[i];

                    // Node box (bigger size)
                    let nodeWidth = 200;
                    let nodeHeight = 100;

                    // Outer box
                    ctx.strokeStyle = "#333";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, nodeWidth, nodeHeight);

                    // Divider between node data and next pointer section
                    ctx.beginPath();
                    ctx.moveTo(x + 140, y);
                    ctx.lineTo(x + 140, y + nodeHeight);
                    ctx.stroke();

                    // Data (top center)
                    ctx.font = "18px Arial";
                    ctx.textAlign = "center";
                    ctx.fillText(node.data, x + 70, y + 35);

                    // Address (below data)
                    ctx.font = "14px Arial";
                    ctx.fillText(node.addr, x + 70, y + 65);

                    // Next pointer section (right side)
                    ctx.textAlign = "left";
                    ctx.font = "14px Arial";
                    ctx.fillText("Next →", x + 150, y + 35);
                    if (node.next)
                        ctx.fillText(node.next, x + 150, y + 65);
                    else
                        ctx.fillText("None", x + 150, y + 65);

                    // Arrow to next node
                    if (i < list.length - 1) {
                        ctx.beginPath();
                        ctx.moveTo(x + nodeWidth, y + nodeHeight / 2);
                        ctx.lineTo(x + nodeWidth + 60, y + nodeHeight / 2);
                        ctx.stroke();

                        // Arrowhead
                        ctx.beginPath();
                        ctx.moveTo(x + nodeWidth + 60, y + nodeHeight / 2);
                        ctx.lineTo(x + nodeWidth + 50, y + nodeHeight / 2 - 5);
                        ctx.moveTo(x + nodeWidth + 60, y + nodeHeight / 2);
                        ctx.lineTo(x + nodeWidth + 50, y + nodeHeight / 2 + 5);
                        ctx.stroke();
                    }

                    x += 280;  // spacing between nodes
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
        msg = linked_list.insert(value)
    else:
        msg = "No value provided."
    return jsonify({"message": msg, "list": linked_list.to_list()})


@app.route('/delete')
def delete_node():
    value = request.args.get('value')
    if value:
        msg = linked_list.delete(value)
    else:
        msg = "No value provided for deletion."
    return jsonify({"message": msg, "list": linked_list.to_list()})


# ------------------------------
# Run Server
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
