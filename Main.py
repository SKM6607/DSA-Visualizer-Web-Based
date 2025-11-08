from  ImportsForMain import *

app = Flask(__name__)

# Register all blueprints
app.register_blueprint(avl_bp)
app.register_blueprint(bst_bp)
app.register_blueprint(btree_bp)
app.register_blueprint(spanning_bp)
app.register_blueprint(rotation_bp)
app.register_blueprint(traversal_bp)
app.register_blueprint(stack_array)
# app.register_blueprint(balancing_symbol)
app.register_blueprint(dijkstra_, url_prefix="/dijkstra")
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

        .section {
            background: rgba(255,255,255,0.15);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            color: white;
        }

        .section h2 {
            font-size: 2rem;
            margin-bottom: 20px;
            border-left: 6px solid #feca57;
            padding-left: 10px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
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

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Data Structure Visualizer</h1>
            <p>Interactive visualization and algorithm demonstrations</p>
        </div>

        <!-- ================= TREE ================= -->
        <div class="section">
            <h2>Tree</h2>
            <div class="grid">
                <a href="/rotation" class="card card-rotation">
                    <span class="card-icon">🔄</span>
                    <h2>Tree Rotation Practice</h2>
                    <p>Master tree rotations with interactive demonstrations. Practice left, right, left-right, and right-left rotations with visual feedback.</p>
                </a>

                <a href="/traversal" class="card card-traversal">
                    <span class="card-icon">🔍</span>
                    <h2>Tree Traversal Methods</h2>
                    <p>Explore all tree traversal techniques: inorder, preorder, postorder, BFS, and DFS. See the visiting order with detailed explanations.</p>
                </a>
            </div>
        </div>

        <!-- ================= BST ================= -->
        <div class="section">
            <h2>BST</h2>
            <div class="grid">
                <a href="/bst" class="card card-bst">
                    <span class="card-icon">🌲</span>
                    <h2>Binary Search Tree</h2>
                    <p>Classic BST implementation with insertion and deletion operations. Step-by-step explanations of node placement and restructuring.</p>
                </a>
            </div>
        </div>

        <!-- ================= STACK ================= -->
        <div class="section">
            <h2>Stack</h2>
            <div class="grid">
                <a href="/stack_array" class="card card-stack_array">
                    <span class="card-icon">📚</span>
                    <h2>Stack Array Visualizer</h2>
                    <p>Visualize stack operations (push, pop, peek) in an array representation with real-time animations.</p>
                </a>

                <a href="/balancing_symbol" class="card card-balancing-symbol">
                    <span class="card-icon">⚖️</span>
                    <h2>Balancing Symbols</h2>
                    <p>Check for balanced parentheses and symbols using stack-based processing.</p>
                </a>
            </div>
        </div>

        <!-- ================= GRAPH ================= -->
        <div class="section">
            <h2>Graph</h2>
            <div class="grid">
                <a href="/spanning" class="card card-spanning">
                    <span class="card-icon">🕸️</span>
                    <h2>Spanning Tree Generator</h2>
                    <p>Visualize Minimum Spanning Trees using Kruskal's and Prim's algorithms.</p>
                </a>

                <a href="/dijkstra" class="card card-dijkstra">
                    <span class="card-icon">🚦</span>
                    <h2>Dijkstra’s Shortest Path</h2>
                    <p>Visualize Dijkstra’s algorithm step-by-step with animations and highlights.</p>
                </a>
            </div>
        </div>

        <!-- ================= LINKED LIST ================= -->
        <div class="section">
            <h2>Linked List</h2>
            <div class="grid">
                <a href="/linkedlist" class="card card-linkedlist">
                    <span class="card-icon">🔗</span>
                    <h2>Linked List Visualizer</h2>
                    <p>Understand singly, doubly, and circular linked list operations through live visuals.</p>
                </a>
            </div>
        </div>

        <!-- ================= QUEUE ================= -->
        <div class="section">
            <h2>Queue</h2>
            <div class="grid">
                <a href="/queue" class="card card-queue">
                    <span class="card-icon">📤</span>
                    <h2>Queue Visualizer</h2>
                    <p>Visualize enqueue and dequeue operations dynamically in queue data structure.</p>
                </a>
            </div>
        </div>

        <!-- ================= DYNAMIC MEMORY ALLOCATION ================= -->
        <div class="section">
            <h2>Dynamic Memory Allocation</h2>
            <div class="grid">
                <a href="/memory" class="card card-memory">
                    <span class="card-icon">💾</span>
                    <h2>Memory Allocation Visualizer</h2>
                    <p>Understand memory allocation techniques (malloc, calloc, realloc, free) visually with step-by-step representation.</p>
                </a>
            </div>
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
