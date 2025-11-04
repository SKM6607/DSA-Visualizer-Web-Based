from flask import Blueprint, render_template_string, request, jsonify

dijkstra_ = Blueprint("/dijkstra", __name__)

# --- HTML and Visualization Template ---
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Dijkstra's Shortest Path Visualizer</title>
    <style>
        body { font-family: Arial; background: #eef3f9; text-align: center; }
        .container { margin-top: 20px; }
        canvas { border: 2px solid #333; background: #fff; margin-top: 20px; }
        input, button { padding: 10px; margin: 5px; }
        .step-info { font-size: 18px; margin: 10px; }
    </style>
</head>
<body>
    <h1>🚦 Dijkstra's Shortest Path Visualizer</h1>
    <div class="container">
        <p>Enter edges as (u, v, weight). Example: A B 4, A C 2, B C 5, B D 10, C D 3</p>
        <input type="text" id="edgesInput" size="60" placeholder="Enter graph edges">
        <input type="text" id="sourceInput" size="10" placeholder="Source Node">
        <button onclick="runDijkstra()">Run Dijkstra</button>
        <div id="steps"></div>
        <canvas id="graphCanvas" width="800" height="500"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("graphCanvas");
        const ctx = canvas.getContext("2d");
        let positions = {};
        const radius = 22;

        function drawNode(name, x, y, color = "#66ccff", textColor = "#000") {
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = "#000";
            ctx.stroke();
            ctx.fillStyle = textColor;
            ctx.font = "bold 16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(name, x, y + 5);
        }

        function drawEdge(u, v, w, color = "#bbb") {
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

        async function runDijkstra() {
            const edges = document.getElementById("edgesInput").value.trim();
            const source = document.getElementById("sourceInput").value.trim();
            const response = await fetch("/dijkstra", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({edges: edges, source: source})
            });
            const data = await response.json();
            visualizeSteps(data);
        }

        async function visualizeSteps(data) {
            const {nodes, edges, steps, distances, source} = data;
            const stepDiv = document.getElementById("steps");
            stepDiv.innerHTML = "";

            const angleStep = (2 * Math.PI) / nodes.length;
            const centerX = 400, centerY = 250, radiusCircle = 180;
            positions = {};

            // Arrange nodes in a circular layout
            nodes.forEach((node, i) => {
                const angle = i * angleStep;
                positions[node] = [centerX + radiusCircle * Math.cos(angle),
                                   centerY + radiusCircle * Math.sin(angle)];
            });

            // Draw initial graph
            clearCanvas();
            edges.forEach(e => drawEdge(e[0], e[1], e[2]));
            nodes.forEach(n => drawNode(n));

            for (let s of steps) {
                await new Promise(r => setTimeout(r, 1000));
                clearCanvas();

                // Redraw edges
                edges.forEach(e => drawEdge(e[0], e[1], e[2], "#ccc"));
                // Highlight current edge
                drawEdge(s.u, s.v, s.weight, "#ff4444");

                // Draw nodes with color coding
                nodes.forEach(n => {
                    let color = n === s.u ? "#ffcc00" : n === s.v ? "#ff8888" : "#66ccff";
                    drawNode(n, positions[n][0], positions[n][1], color);
                });

                // Step info
                const msg = document.createElement("div");
                msg.className = "step-info";
                msg.innerHTML = `🔹 Checking edge (${s.u}, ${s.v}) | New Dist(${s.v}) = ${s.newDist}`;
                stepDiv.appendChild(msg);
            }

            const msg = document.createElement("h2");
            msg.innerHTML = "✅ Final Shortest Distances from " + source + ": " + JSON.stringify(distances);
            stepDiv.appendChild(msg);
        }
    </script>
</body>
</html>
"""

# --- Dijkstra Algorithm Backend ---
@dijkstra_.route("/")
def home():
    return render_template_string(html_template)

@dijkstra_.route("/dijkstra", methods=["POST"])
def dijkstra():
    data = request.get_json()
    raw_edges = data["edges"]
    source = data["source"].strip()

    edges = []
    nodes = set()
    for part in raw_edges.split(","):
        u, v, w = part.strip().split()
        w = int(w)
        edges.append((u, v, w))
        edges.append((v, u, w))  # undirected
        nodes.add(u)
        nodes.add(v)

    graph = {n: [] for n in nodes}
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = {n: float("inf") for n in nodes}
    dist[source] = 0
    visited = set()
    steps = []

    while len(visited) < len(nodes):
        u = min((n for n in nodes if n not in visited), key=lambda n: dist[n], default=None)
        if u is None or dist[u] == float("inf"):
            break
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                steps.append({"u": u, "v": v, "weight": w, "newDist": dist[v]})

    return jsonify({
        "nodes": list(nodes),
        "edges": [(u, v, w) for u, v, w in edges if u < v],
        "steps": steps,
        "distances": dist,
        "source": source
    })
