from flask import Flask, request, jsonify, render_template_string
import json, math

app = Flask(__name__)

# -------------------------------
# Prim's Algorithm Implementation
# -------------------------------
def prim_mst(graph):
    n = len(graph)
    selected = [False] * n
    selected[0] = True
    edges = []
    steps = []
    step_number = 1

    while len(edges) < n - 1:
        minimum = math.inf
        x = y = 0
        for i in range(n):
            if selected[i]:
                for j in range(n):
                    if not selected[j] and graph[i][j]:
                        if minimum > graph[i][j]:
                            minimum = graph[i][j]
                            x, y = i, j
        selected[y] = True
        edges.append((x, y, graph[x][y]))

        steps.append({
            "step": step_number,
            "selected_edge": (x, y, graph[x][y]),
            "selected_nodes": [i for i, s in enumerate(selected) if s]
        })
        step_number += 1

    total_cost = sum(w for _, _, w in edges)
    return edges, steps, total_cost


# -------------------------------
# Flask Routes
# -------------------------------
@app.route('/')
def index():
    default_matrix = """0,2,0,6,0
2,0,3,8,5
0,3,0,0,7
6,8,0,0,9
0,5,7,9,0"""  # Default graph

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prim's Minimum Spanning Tree Visualization</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #eef2f3; text-align: center; padding: 20px; }}
            canvas {{ border: 2px solid #333; margin-top: 20px; background: white; }}
            textarea {{ margin: 5px; padding: 5px; width: 400px; height: 120px; }}
            button {{ padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }}
            button:hover {{ background: #45a049; }}
            .step-info {{ background: #fff; margin: 10px auto; width: 60%; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <h1>Prim's Minimum Spanning Tree (MST) Visualizer</h1>
        <p>Enter adjacency matrix (comma separated rows):</p>
        <textarea id="matrix">{default_matrix}</textarea><br>
        <button onclick="computeMST()">Compute MST</button>
        <h3 id="status"></h3>
        <canvas id="graphCanvas" width="800" height="500"></canvas>
        <div id="steps"></div>

        <script>
            async function computeMST() {{
                const matrixInput = document.getElementById('matrix').value.trim();
                if (!matrixInput) return alert("Please enter adjacency matrix!");

                const rows = matrixInput.split("\\n").map(r => r.split(',').map(Number));
                const res = await fetch('/prims', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ graph: rows }})
                }});
                const data = await res.json();

                drawGraph(data.steps, rows.length, rows);
                showSteps(data.steps, data.total_cost);
                document.getElementById('status').innerText = "✅ MST Computed Successfully! Total Cost = " + data.total_cost;
            }}

            function drawGraph(steps, n, graph) {{
                const canvas = document.getElementById('graphCanvas');
                const ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                const centerX = canvas.width / 2;
                const centerY = canvas.height / 2;
                const radius = 180;
                const nodes = [];

                for (let i = 0; i < n; i++) {{
                    const angle = (2 * Math.PI / n) * i;
                    const x = centerX + radius * Math.cos(angle);
                    const y = centerY + radius * Math.sin(angle);
                    nodes.push({{ x, y }});
                }}

                // Draw all edges lightly with weights
                ctx.strokeStyle = '#ccc';
                ctx.lineWidth = 1;
                ctx.font = '13px Arial';
                for (let i = 0; i < n; i++) {{
                    for (let j = i + 1; j < n; j++) {{
                        if (graph[i][j] !== 0) {{
                            ctx.beginPath();
                            ctx.moveTo(nodes[i].x, nodes[i].y);
                            ctx.lineTo(nodes[j].x, nodes[j].y);
                            ctx.stroke();
                            // Weight label
                            const midX = (nodes[i].x + nodes[j].x) / 2;
                            const midY = (nodes[i].y + nodes[j].y) / 2;
                            ctx.fillStyle = "gray";
                            ctx.fillText(graph[i][j], midX, midY);
                        }}
                    }}
                }}

                // Draw MST edges step-by-step
                let delay = 1000;
                steps.forEach((step, index) => {{
                    setTimeout(() => {{
                        const [x, y] = step.selected_edge;
                        ctx.strokeStyle = 'green';
                        ctx.lineWidth = 3;
                        ctx.beginPath();
                        ctx.moveTo(nodes[x].x, nodes[x].y);
                        ctx.lineTo(nodes[y].x, nodes[y].y);
                        ctx.stroke();

                        // Highlight selected nodes
                        ctx.fillStyle = 'lightgreen';
                        step.selected_nodes.forEach(idx => {{
                            ctx.beginPath();
                            ctx.arc(nodes[idx].x, nodes[idx].y, 25, 0, 2 * Math.PI);
                            ctx.fill();
                        }});

                        // Redraw node labels
                        ctx.fillStyle = 'black';
                        ctx.font = '16px Arial';
                        for (let i = 0; i < n; i++) {{
                            ctx.beginPath();
                            ctx.arc(nodes[i].x, nodes[i].y, 25, 0, 2 * Math.PI);
                            ctx.stroke();
                            ctx.fillText("V" + i, nodes[i].x - 10, nodes[i].y + 5);
                        }}
                    }}, delay * index);
                }});
            }}

            function showSteps(steps, totalCost) {{
                const stepsDiv = document.getElementById('steps');
                stepsDiv.innerHTML = '<h3>Step-by-Step Process</h3>';
                steps.forEach(st => {{
                    const div = document.createElement('div');
                    div.className = 'step-info';
                    div.innerHTML = `<b>Step ${'{'}st.step{'}'}</b>: Added Edge (${ '{'}st.selected_edge[0]{'}'}, ${'{'}st.selected_edge[1]{'}'}) 
                                     with Weight ${'{'}st.selected_edge[2]{'}'}<br>
                                     Selected Nodes: ${'{'}st.selected_nodes.join(', '){'}'}`;
                    stepsDiv.appendChild(div);
                }});
                const total = document.createElement('div');
                total.className = 'step-info';
                total.innerHTML = `<b>Total MST Cost: ${'{'}totalCost{'}'}</b>`;
                stepsDiv.appendChild(total);
            }}
        </script>
    </body>
    </html>
    """)

@app.route('/prims', methods=['POST'])
def run_prims():
    data = request.get_json()
    graph = data['graph']
    edges, steps, total_cost = prim_mst(graph)
    return jsonify({"edges": edges, "steps": steps, "total_cost": total_cost})


if __name__ == '__main__':
    app.run(debug=True)
