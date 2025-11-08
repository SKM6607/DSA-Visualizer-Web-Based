from flask import Blueprint, request, jsonify, render_template_string

sparse_matrix_bp = Blueprint('sparseMatrix', __name__, url_prefix='/sparse_matrix')

#
class Node:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val
        self.next = None

class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.head = None

    def insert(self, row, col, val):
        """Insert a non-zero element in sorted order (row-major)."""
        if val == 0:
            return "Zero value not stored in sparse matrix."

        new_node = Node(row, col, val)
        if self.head is None or (row < self.head.row or (row == self.head.row and col < self.head.col)):
            new_node.next = self.head
            self.head = new_node
            return f"Inserted value {val} at ({row}, {col})."

        prev = None
        curr = self.head
        while curr and (curr.row < row or (curr.row == row and curr.col < col)):
            prev = curr
            curr = curr.next

        # If the element already exists, update
        if curr and curr.row == row and curr.col == col:
            curr.val = val
            return f"Updated value at ({row}, {col}) to {val}."

        new_node.next = curr
        prev.next = new_node
        return f"Inserted value {val} at ({row}, {col})."

    def delete(self, row, col):
        """Delete an element from the sparse matrix."""
        if self.head is None:
            return "Matrix is empty."
        curr = self.head
        prev = None
        while curr:
            if curr.row == row and curr.col == col:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return f"Deleted element at ({row}, {col})."
            prev = curr
            curr = curr.next
        return f"No element found at ({row}, {col})."

    def to_list(self):
        """Return all non-zero elements as list of dicts."""
        result = []
        curr = self.head
        while curr:
            result.append({
                "row": curr.row,
                "col": curr.col,
                "val": curr.val
            })
            curr = curr.next
        return result

matrix = SparseMatrix(rows=5, cols=5)

@sparse_matrix_bp.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sparse Matrix Visualization</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f7fafc; margin-top: 40px; }
            canvas { border: 2px solid #333; margin-top: 20px; background: white; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2>🧮 Sparse Matrix Visualization (Triplet Linked Representation)</h2>

        <div>
            <input type="number" id="row" placeholder="Row (0-based)" min="0">
            <input type="number" id="col" placeholder="Col (0-based)" min="0">
            <input type="number" id="val" placeholder="Value">
            <button onclick="insert()">Insert</button>
            <button onclick="deleteElement()">Delete</button>
        </div>

        <p id="status"></p>

        <canvas id="canvas" width="1200" height="600"></canvas>

        <script>
            async function insert() {
                let row = parseInt(document.getElementById("row").value);
                let col = parseInt(document.getElementById("col").value);
                let val = parseInt(document.getElementById("val").value);
                if (isNaN(row) || isNaN(col) || isNaN(val)) {
                    alert("Please enter row, column, and value!");
                    return;
                }
                let res = await fetch(`/sparse_matrix/insert?row=${row}&col=${col}&val=${val}`);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawMatrix(data.elements);
            }

            async function deleteElement() {
                let row = parseInt(document.getElementById("row").value);
                let col = parseInt(document.getElementById("col").value);
                if (isNaN(row) || isNaN(col)) {
                    alert("Please enter row and column!");
                    return;
                }
                let res = await fetch(`/sparse_matrix/delete?row=${row}&col=${col}`);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawMatrix(data.elements);
            }

            function drawMatrix(elements) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                const rows = 5, cols = 5;
                const cellSize = 80;
                const startX = 100, startY = 100;

                // Draw grid
                ctx.strokeStyle = "#000";
                ctx.font = "16px Arial";
                for (let i = 0; i < rows; i++) {
                    for (let j = 0; j < cols; j++) {
                        ctx.strokeRect(startX + j * cellSize, startY + i * cellSize, cellSize, cellSize);
                        ctx.fillStyle = "#555";
                        ctx.fillText(`${i},${j}`, startX + j * cellSize + 20, startY + i * cellSize + 45);
                    }
                }

                // Draw non-zero elements as nodes
                let nodeX = 100;
                let nodeY = 520;

                for (let i = 0; i < elements.length; i++) {
                    const e = elements[i];
                    // Draw node box
                    ctx.beginPath();
                    ctx.rect(nodeX, nodeY, 90, 60);
                    ctx.fillStyle = "#a3e0ff";
                    ctx.fill();
                    ctx.stroke();

                    // Display value (inside)
                    ctx.fillStyle = "#000";
                    ctx.font = "14px Arial";
                    ctx.fillText(`Val: ${e.val}`, nodeX + 10, nodeY + 35);

                    // Display coordinates (above and below)
                    ctx.fillText(`(${e.row}, ${e.col})`, nodeX + 10, nodeY - 10);

                    // Draw arrow to next node
                    if (i < elements.length - 1) {
                        ctx.beginPath();
                        ctx.moveTo(nodeX + 90, nodeY + 30);
                        ctx.lineTo(nodeX + 120, nodeY + 30);
                        ctx.stroke();
                        ctx.beginPath();
                        ctx.moveTo(nodeX + 115, nodeY + 25);
                        ctx.lineTo(nodeX + 120, nodeY + 30);
                        ctx.lineTo(nodeX + 115, nodeY + 35);
                        ctx.stroke();
                    }

                    nodeX += 120;
                }

                // Highlight non-zero elements in matrix grid
                ctx.fillStyle = "red";
                elements.forEach(e => {
                    ctx.fillRect(startX + e.col * cellSize + 10, startY + e.row * cellSize + 10, 60, 60);
                    ctx.fillStyle = "white";
                    ctx.fillText(e.val, startX + e.col * cellSize + 35, startY + e.row * cellSize + 50);
                    ctx.fillStyle = "red";
                });
            }

            // Load initial matrix
            window.onload = async function() {
                let res = await fetch('/sparse_matrix/status');
                let data = await res.json();
                drawMatrix(data.elements);
            };
        </script>
    </body>
    </html>
    """)


@sparse_matrix_bp.route('/insert')
def insert():
    row = request.args.get('row', type=int)
    col = request.args.get('col', type=int)
    val = request.args.get('val', type=int)
    msg = matrix.insert(row, col, val)
    return jsonify({"message": msg, "elements": matrix.to_list()})

@sparse_matrix_bp.route('/delete')
def delete():
    row = request.args.get('row', type=int)
    col = request.args.get('col', type=int)
    msg = matrix.delete(row, col)
    return jsonify({"message": msg, "elements": matrix.to_list()})

@sparse_matrix_bp.route('/status')
def status():
    return jsonify({"elements": matrix.to_list()})
