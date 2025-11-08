from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML Template with visualization and input form
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Kruskal's Minimum Spanning Tree Visualizer</title>
    <style>
        body { font-family: Arial; background: #f0f4f8; text-align: center; }
        .container { margin-top: 20px; }
        canvas { border: 2px solid #333; background: #fff; margin-top: 20px; }
        input, button { padding: 10px; margin: 5px; }
        .edge-step { font-size: 18px; margin: 10px; }
    </style>
</head>
<body>
    <h1>🌳 Kruskal's Minimum Spanning Tree Visualizer</h1>
    <div class="container">
        <p>Enter edges as (u, v, weight) separated by commas. Example: A B 3, A C 1, B C 2</p>
        <input type="text" id="edgesInput" size="60" placeholder="Enter graph edges">
        <button onclick="startKruskal()">Run Kruskal</button>
        <div id="steps"></div>
        <canvas id="graphCanvas" width="800" height="500"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("graphCanvas");
        const ctx = canvas.getContext("2d");

        let nodes = {};
        let positions = {};
        const radius = 20;

        function drawNode(name, x, y, color = "#66ccff") {
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = "#000";
            ctx.stroke();
            ctx.fillStyle = "#000";
            ctx.font = "bold 16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(name, x, y + 5);
        }

        function drawEdge(u, v, w, color = "#aaa") {
            const [x1, y1] = positions[u];
            const [x2, y2] = positions[v];
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.fillStyle = "#000";
            ctx.fillText(w, (x1 + x2) / 2, (y1 + y2) / 2 - 5);
        }

        function clearCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        async function startKruskal() {
            const input = document.getElementById("edgesInput").value.trim();
            const response = await fetch("/kruskal", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({edges: input})
            });
            const data = await response.json();
            visualizeSteps(data);
        }

        async function visualizeSteps(data) {
            const {nodesList, edges, steps} = data;
            const stepDiv = document.getElementById("steps");
            stepDiv.innerHTML = "";

            const angleStep = (2 * Math.PI) / nodesList.length;
            const centerX = 400, centerY = 250, radiusCircle = 180;

            // Assign node positions in circular layout
            positions = {};
            nodesList.forEach((node, i) => {
                const angle = i * angleStep;
                positions[node] = [centerX + radiusCircle * Math.cos(angle),
                                   centerY + radiusCircle * Math.sin(angle)];
            });

            // Draw initial graph
            clearCanvas();
            edges.forEach(e => drawEdge(e[0], e[1], e[2]));
            nodesList.forEach(n => drawNode(n));

            // Step-by-step MST formation
            for (let s of steps) {
                await new Promise(r => setTimeout(r, 1000));
                clearCanvas();
                edges.forEach(e => drawEdge(e[0], e[1], e[2], "#bbb"));
                s.mst.forEach(e => drawEdge(e[0], e[1], e[2], "#28a745"));
                nodesList.forEach(n => drawNode(n));
                const msg = document.createElement("div");
                msg.className = "edge-step";
                msg.innerHTML = "✅ Added Edge: " + s.edge.join(" - ") + " (Weight " + s.weight + ")";
                stepDiv.appendChild(msg);
            }

            const total = steps.reduce((sum, s) => sum + s.weight, 0);
            const msg = document.createElement("h2");
            msg.innerHTML = "🌟 MST Complete! Total Weight = " + total;
            stepDiv.appendChild(msg);
        }
    </script>
</body>
</html>
"""

# ---- Kruskal Algorithm ----
def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/kruskal", methods=["POST"])
def kruskal():
    data = request.get_json()
    raw_edges = data["edges"]
    edges = []
    nodes = set()

    for part in raw_edges.split(","):
        u, v, w = part.strip().split()
        w = int(w)
        edges.append((u, v, w))
        nodes.add(u)
        nodes.add(v)

    edges = sorted(edges, key=lambda e: e[2])
    parent = {}
    rank = {}
    for node in nodes:
        parent[node] = node
        rank[node] = 0

    mst = []
    steps = []
    for u, v, w in edges:
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            mst.append((u, v, w))
            union(parent, rank, x, y)
            steps.append({"edge": (u, v), "weight": w, "mst": mst.copy()})

    return jsonify({
        "nodesList": list(nodes),
        "edges": edges,
        "steps": steps
    })

if __name__ == "__main__":
    app.run(debug=True)
