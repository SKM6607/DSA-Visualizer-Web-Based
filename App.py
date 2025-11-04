from flask import Flask, render_template_string
from AVL import avl_bp
from BST import bst_bp
from Btree import btree_bp
from Spanning import spanning_bp
from TreeRotation import rotation_bp
from TreeTravel import traversal_bp
from U3stackarray import stack_array
from U3balancingsymbol import balancing_symbol
from U5dijkstra import dijkstra_
app = Flask(__name__)

# Register all blueprints
app.register_blueprint(avl_bp)
app.register_blueprint(bst_bp)
app.register_blueprint(btree_bp)
app.register_blueprint(spanning_bp)
app.register_blueprint(rotation_bp)
app.register_blueprint(traversal_bp)
app.register_blueprint(stack_array)
app.register_blueprint(balancing_symbol)
app.register_blueprint(dijkstra_)
# Modern home page with cards
HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Structure Visualizer Control Panel</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }

        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            padding: 20px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }

        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }

        .card-icon {
            font-size: 3rem;
            margin-bottom: 15px;
            display: block;
        }

        .card h2 {
            color: #333;
            font-size: 1.5rem;
            margin-bottom: 10px;
        }

        .card p {
            color: #666;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .card-avl { border-top: 4px solid #667eea; }
        .card-stack_array { border-top: 4px solid #667eea; }
        .card-bst { border-top: 4px solid #f093fb; }
        .card-btree { border-top: 4px solid #4facfe; }
        .card-balancing-symbol{ border-top: 4px solid #4facfe; }
        .card-spanning { border-top: 4px solid #43e97b; }
        .card-rotation { border-top: 4px solid #fa709a; }
        .card-traversal { border-top: 4px solid #feca57; }
        .card-dijkstra { border-top: 4px solid #feca57; }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌳 Data Structure Visualizer</h1>
            <p>Interactive visualization and algorithm demonstrations</p>
        </div>

        <div class="grid">
            <a href="/avl" class="card card-avl">
                <span class="card-icon">⚖️</span>
                <h2>AVL Tree Visualizer</h2>
                <p>Self-balancing binary search tree with automatic rotations. Watch real-time balancing operations and explore LL, RR, LR, and RL rotation cases.</p>
            </a>

            <a href="/stack_array" class="card card-stack_array">
                <span class="card-icon">⚖️</span>
                <h2>Stack Array Visualizer</h2>
                <p>Self-balancing binary search tree with automatic rotations. Watch real-time balancing operations and explore LL, RR, LR, and RL rotation cases.</p>
            </a>

            <a href="/balancing_symbol" class="card card-balancing-symbol">
                <span class="card-icon">⚖️</span>
                <h2>Balancing Symbol</h2>
                <p>Self-balancing binary search tree with automatic rotations. Watch real-time balancing operations and explore LL, RR, LR, and RL rotation cases.</p>
            </a>

            <a href="/bst" class="card card-bst">
                <span class="card-icon">🌲</span>
                <h2>Binary Search Tree</h2>
                <p>Classic BST implementation with insertion and deletion operations. Step-by-step explanations of node placement and tree restructuring.</p>
            </a>

            <a href="/btree" class="card card-btree">
                <span class="card-icon">📊</span>
                <h2>B-Tree Visualizer</h2>
                <p>Multi-way search tree with automatic node splitting. Perfect for understanding database indexing and file systems with visual split operations.</p>
            </a>

            <a href="/spanning" class="card card-spanning">
                <span class="card-icon">🕸️</span>
                <h2>Spanning Tree Generator</h2>
                <p>Visualize Minimum Spanning Trees using Kruskal's and Prim's algorithms. Compare different spanning trees with DFS and randomized approaches.</p>
            </a>

            <a href="/rotation" class="card card-rotation">
                <span class="card-icon">🔄</span>
                <h2>Tree Rotation Practice</h2>
                <p>Master tree rotations with interactive demonstrations. Practice left, right, left-right, and right-left rotations with visual feedback.</p>
            </a>

            <a href="/dijkstra" class="card card-dijkstra">
                <span class="card-icon">⚖️</span>
                <h2>Balancing Symbol</h2>
                <p>Self-balancing binary search tree with automatic rotations. Watch real-time balancing operations and explore LL, RR, LR, and RL rotation cases.</p>
            </a>
            <a href="/traversal" class="card card-traversal">
                <span class="card-icon">🔍</span>
                <h2>Tree Traversal Methods</h2>
                <p>Explore all tree traversal techniques: inorder, preorder, postorder, BFS, and DFS. See the visiting order with detailed step-by-step explanations.</p>
            </a>
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HOME_PAGE)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
