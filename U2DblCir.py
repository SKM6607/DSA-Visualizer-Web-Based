from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------
# Data Structure: Doubly Circular Linked List
# ------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
        self.addr = hex(id(self))  # Simulated memory address


class DoublyCircularLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        """Insert a new node at the end of the circular doubly linked list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            return f"Inserted {data} as head node (circular doubly linked)"
        current = self.head
        while current.next != self.head:
            current = current.next
        current.next = new_node
        new_node.prev = current
        new_node.next = self.head
        self.head.prev = new_node
        return f"Inserted node with value {data}"

    def delete(self, data):
        """Delete a node by value"""
        if not self.head:
            return "List is empty — nothing to delete."
        current = self.head

        # Case 1: deleting head
        if current.data == data:
            if current.next == self.head:
                deleted_addr = current.addr
                self.head = None
                return f"Deleted the only node {data} (addr: {deleted_addr})"
            else:
                deleted_addr = current.addr
                tail = self.head.prev
                self.head = self.head.next
                self.head.prev = tail
                tail.next = self.head
                return f"Deleted head node {data} (addr: {deleted_addr})"

        # Case 2: deleting non-head
        current = self.head.next
        while current != self.head:
            if current.data == data:
                current.prev.next = current.next
                current.next.prev = current.prev
                return f"Deleted node with value {data} (addr: {current.addr})"
            current = current.next
        return f"Node with value {data} not found."

    def to_list(self):
        """Return structured list with data + address info"""
        result = []
        if not self.head:
            return result
        current = self.head
        while True:
            result.append({
                "data": current.data,
                "addr": current.addr,
                "next": current.next.addr if current.next else None,
                "prev": current.prev.addr if current.prev else None
            })
            current = current.next
            if current == self.head:
                break
        return result


# Create global circular doubly linked list instance
dll = DoublyCircularLinkedList()

# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Doubly Circular Linked List Visualizer</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2>🔁 Doubly Circular Linked List Visualization (Insert & Delete with Addresses)</h2>

        <div>
            <input type="text" id="nodeValue" placeholder="Enter node value">
            <button onclick="insertNode()">Insert Node</button>
            <button onclick="deleteNode()">Delete Node</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="1400" height="500"></canvas>

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

                if(list.length === 0) {
                    ctx.font = "20px Arial";
                    ctx.fillText("Doubly Circular Linked List is empty", 450, 250);
                    return;
                }

                let x = 60, y = 180;

                for(let i=0; i<list.length; i++) {
                    let node = list[i];

                    // Node box
                    ctx.strokeStyle = "#333";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, 200, 100);

                    // Divide for prev / data+addr / next
                    ctx.beginPath();
                    ctx.moveTo(x + 60, y);
                    ctx.lineTo(x + 60, y + 100);
                    ctx.moveTo(x + 140, y);
                    ctx.lineTo(x + 140, y + 100);
                    ctx.stroke();

                    // Data
                    ctx.font = "14px Arial";
                    ctx.fillText("Data: " + node.data, x + 65, y + 35);
                    ctx.fillText("Addr: " + node.addr, x + 65, y + 70);

                    // Prev and Next fields
                    ctx.font = "11px Arial";
                    ctx.fillText("Prev", x + 5, y + 25);
                    ctx.fillText(node.prev || "None", x + 5, y + 70);
                    ctx.fillText("Next", x + 145, y + 25);
                    ctx.fillText(node.next || "None", x + 145, y + 70);

                    // Forward arrow (next)
                    if (i < list.length - 1) {
                        ctx.beginPath();
                        ctx.moveTo(x + 200, y + 50);
                        ctx.lineTo(x + 240, y + 50);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(x + 240, y + 50);
                        ctx.lineTo(x + 230, y + 45);
                        ctx.moveTo(x + 240, y + 50);
                        ctx.lineTo(x + 230, y + 55);
                        ctx.stroke();

                        // Backward arrow (prev)
                        ctx.beginPath();
                        ctx.moveTo(x + 240, y + 65);
                        ctx.lineTo(x + 200, y + 65);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(x + 200, y + 65);
                        ctx.lineTo(x + 210, y + 60);
                        ctx.moveTo(x + 200, y + 65);
                        ctx.lineTo(x + 210, y + 70);
                        ctx.stroke();
                    } else {
                        // Circular arrows
                        ctx.beginPath();
                        ctx.moveTo(x + 200, y + 50);
                        ctx.bezierCurveTo(x + 250, y - 80, 40, y - 80, 60, y + 20);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(60, y + 20);
                        ctx.lineTo(70, y + 15);
                        ctx.moveTo(60, y + 20);
                        ctx.lineTo(70, y + 25);
                        ctx.stroke();

                        // Backward circular arrow
                        ctx.beginPath();
                        ctx.moveTo(60, y + 65);
                        ctx.bezierCurveTo(20, y + 150, x + 250, y + 150, x + 200, y + 80);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(x + 200, y + 80);
                        ctx.lineTo(x + 190, y + 75);
                        ctx.moveTo(x + 200, y + 80);
                        ctx.lineTo(x + 190, y + 85);
                        ctx.stroke();
                    }

                    x += 250;
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
