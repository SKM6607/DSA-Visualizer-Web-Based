from flask import Blueprint, request, jsonify, render_template_string

circular_singly_linked_list_bp = Blueprint('singlyCircularLinkedList', __name__, url_prefix='/singly_circular_linkedlist')

# ------------------------------
# Data Structure: Singly Circular Linked List
# ------------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.addr = hex(id(self))  # Simulated memory address


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        """Insert a new node at the end of the circular linked list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = new_node  # Point to itself
            return f"Inserted {data} as head node (circular link to itself)"
        current = self.head
        while current.next != self.head:
            current = current.next
        current.next = new_node
        new_node.next = self.head
        return f"Inserted node with value {data}"

    def delete(self, data):
        """Delete the first node with given data"""
        if not self.head:
            return "List is empty — nothing to delete."
        current = self.head
        prev = None

        # Case 1: deleting head
        if current.data == data:
            # If only one node in the list
            if current.next == self.head:
                deleted_addr = current.addr
                self.head = None
                return f"Deleted the only node {data} (addr: {deleted_addr})"
            else:
                # Find last node to update its next pointer
                while current.next != self.head:
                    current = current.next
                deleted_addr = self.head.addr
                current.next = self.head.next
                self.head = self.head.next
                return f"Deleted head node {data} (addr: {deleted_addr})"

        # Case 2: deleting non-head node
        prev = self.head
        current = self.head.next
        while current != self.head:
            if current.data == data:
                prev.next = current.next
                return f"Deleted node with value {data} (addr: {current.addr})"
            prev = current
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
                "next": current.next.addr if current.next else None
            })
            current = current.next
            if current == self.head:
                break
        return result


# Create global circular linked list instance
circular_list = CircularLinkedList()

# ------------------------------
# Flask Routes
# ------------------------------

@circular_singly_linked_list_bp.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Singly Circular Linked List Visualizer</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2>🔄 Singly Circular Linked List Visualization (Insert & Delete with Addresses)</h2>

        <div>
            <input type="text" id="nodeValue" placeholder="Enter node value">
            <button onclick="insertNode()">Insert Node</button>
            <button onclick="deleteNode()">Delete Node</button>
        </div>

        <p id="status"></p>
        <canvas id="canvas" width="1200" height="450"></canvas>

        <script>
            async function insertNode() {
                let val = document.getElementById("nodeValue").value;
                if(!val) return alert("Enter a value");
                let res = await fetch('/singly_circular_linkedlist/insert?value=' + val);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawList(data.list);
            }

            async function deleteNode() {
                let val = document.getElementById("nodeValue").value;
                if(!val) return alert("Enter a value to delete");
                let res = await fetch('/singly_circular_linkedlist/delete?value=' + val);
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
                    ctx.fillText("Circular Linked List is empty", 400, 200);
                    return;
                }

                let x = 60, y = 150;

                for(let i=0; i<list.length; i++) {
                    let node = list[i];

                    // Node box (larger)
                    ctx.strokeStyle = "#333";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, 170, 100);

                    // Divider between data and next pointer
                    ctx.beginPath();
                    ctx.moveTo(x + 120, y);
                    ctx.lineTo(x + 120, y + 100);
                    ctx.stroke();

                    // Data (top center)
                    ctx.font = "14px Arial";
                    ctx.fillText("Data: " + node.data, x + 10, y + 30);

                    // Address (below)
                    ctx.font = "13px Arial";
                    ctx.fillText("Addr: " + node.addr, x + 10, y + 65);

                    // Next field
                    ctx.font = "12px Arial";
                    ctx.fillText("Next →", x + 125, y + 30);
                    if (node.next)
                        ctx.fillText(node.next, x + 125, y + 65);
                    else
                        ctx.fillText("None", x + 125, y + 65);

                    // Arrow to next node (or loop to first)
                    if (i < list.length - 1) {
                        ctx.beginPath();
                        ctx.moveTo(x + 170, y + 50);
                        ctx.lineTo(x + 210, y + 50);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(x + 210, y + 50);
                        ctx.lineTo(x + 200, y + 45);
                        ctx.moveTo(x + 210, y + 50);
                        ctx.lineTo(x + 200, y + 55);
                        ctx.stroke();
                    } else {
                        // Draw circular arrow back to head
                        ctx.beginPath();
                        ctx.moveTo(x + 170, y + 50);
                        ctx.bezierCurveTo(x + 200, y - 50, 50, y - 50, 60, y + 10);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(60, y + 10);
                        ctx.lineTo(70, y + 5);
                        ctx.moveTo(60, y + 10);
                        ctx.lineTo(70, y + 15);
                        ctx.stroke();
                    }

                    x += 220;
                }
            }
        </script>
    </body>
    </html>
    """)

@circular_singly_linked_list_bp.route('/insert')
def insert_node():
    value = request.args.get('value')
    if value:
        msg = circular_list.insert(value)
    else:
        msg = "No value provided."
    return jsonify({"message": msg, "list": circular_list.to_list()})

@circular_singly_linked_list_bp.route('/delete')
def delete_node():
    value = request.args.get('value')
    if value:
        msg = circular_list.delete(value)
    else:
        msg = "No value provided for deletion."
    return jsonify({"message": msg, "list": circular_list.to_list()})
