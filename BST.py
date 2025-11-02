from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# ----------------------------
# Binary Search Tree Structure
# ----------------------------
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key


class BST:
    def __init__(self):
        self.root = None

    # ---------- INSERT ----------
    def insert(self, key):
        explanation = []
        if self.root is None:
            self.root = Node(key)
            explanation.append(f"Tree is empty. Inserting {key} as root node.")
            return True, explanation
        result, explanation = self._insert(self.root, key, explanation)
        return result, explanation

    def _insert(self, node, key, explanation):
        explanation.append(f"At node {node.key}.")
        if key == node.key:
            explanation.append(f"{key} already exists — skipping insertion.")
            return False, explanation
        elif key < node.key:
            explanation.append(f"{key} < {node.key}: moving LEFT.")
            if node.left:
                return self._insert(node.left, key, explanation)
            else:
                node.left = Node(key)
                explanation.append(f"Inserted {key} as LEFT child of {node.key}.")
                return True, explanation
        else:
            explanation.append(f"{key} > {node.key}: moving RIGHT.")
            if node.right:
                return self._insert(node.right, key, explanation)
            else:
                node.right = Node(key)
                explanation.append(f"Inserted {key} as RIGHT child of {node.key}.")
                return True, explanation

    # ---------- DELETE ----------
    def delete(self, key):
        explanation = []
        self.root, deleted, explanation = self._delete(self.root, key, explanation)
        return deleted, explanation

    def _delete(self, node, key, explanation):
        if not node:
            explanation.append(f"Traversal ended: {key} not found.")
            return node, False, explanation

        if key < node.key:
            explanation.append(f"{key} < {node.key}: moving LEFT subtree.")
            node.left, deleted, explanation = self._delete(node.left, key, explanation)
        elif key > node.key:
            explanation.append(f"{key} > {node.key}: moving RIGHT subtree.")
            node.right, deleted, explanation = self._delete(node.right, key, explanation)
        else:
            explanation.append(f"Node {key} found — starting deletion process.")
            deleted = True
            # Case 1: No left child
            if not node.left:
                explanation.append(f"{key} has no LEFT child — replacing with RIGHT child.")
                return node.right, deleted, explanation
            # Case 2: No right child
            elif not node.right:
                explanation.append(f"{key} has no RIGHT child — replacing with LEFT child.")
                return node.left, deleted, explanation
            # Case 3: Two children
            else:
                explanation.append(f"{key} has TWO children — finding inorder successor.")
                succ = node.right
                while succ.left:
                    succ = succ.left
                explanation.append(f"Inorder successor of {key} is {succ.key}. Replacing {key} with {succ.key}.")
                node.key = succ.key
                node.right, _, explanation = self._delete(node.right, succ.key, explanation)
        return node, deleted, explanation

    # ---------- CONVERT TO DICT ----------
    def to_dict(self):
        def node_to_dict(n):
            if not n:
                return None
            d = {"name": str(n.key)}
            children = []
            if n.left:
                children.append(node_to_dict(n.left))
            if n.right:
                children.append(node_to_dict(n.right))
            if children:
                d["children"] = children
            return d
        if not self.root:
            return {}
        return node_to_dict(self.root)

    # ---------- INORDER TRAVERSAL ----------
    def inorder(self):
        res = []
        self._inorder(self.root, res)
        return res

    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)


# Create global BST and seed sample values
bst = BST()
for v in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(v)

# ----------------------------
# Flask Web Interface
# ----------------------------
INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>BST Visualizer with Explanation</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: Arial, sans-serif; margin: 10px; }
    input, button { padding: 6px; margin: 4px; }
    #tree { width: 100%; height: 600px; border: 1px solid #ddd; margin-top:10px; }
    #explanation { background: #f9f9f9; border: 1px solid #ccc; padding: 10px; margin-top: 10px; height: 180px; overflow-y: scroll; }
    .node circle { fill: #fff; stroke: steelblue; stroke-width: 2px; }
    .node text { font: 12px sans-serif; }
    .link { fill: none; stroke: #ccc; stroke-width: 2px; }
  </style>
</head>
<body>
  <h2>Binary Search Tree Visualizer (Insert & Delete Explanation)</h2>
  <div>
    <input id="keyInput" type="number" placeholder="Enter key value" />
    <button onclick="insertKey()">Insert</button>
    <button onclick="deleteKey()">Delete</button>
    <button onclick="refreshTree()">Refresh</button>
    <span id="msg" style="margin-left:10px;color:green;"></span>
  </div>

  <div id="explanation">Step-by-step explanation will appear here...</div>
  <div id="tree"></div>

  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
    async function fetchTree() {
      const resp = await fetch('/tree');
      return await resp.json();
    }

    async function insertKey(){
      const val = document.getElementById('keyInput').value;
      if(!val){ alert('Enter a key'); return; }
      const resp = await fetch('/insert', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({key: parseInt(val)})
      });
      const res = await resp.json();
      document.getElementById('msg').textContent = res.message;
      showExplanation(res.explanation);
      refreshTree();
    }

    async function deleteKey(){
      const val = document.getElementById('keyInput').value;
      if(!val){ alert('Enter a key'); return; }
      const resp = await fetch('/delete', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({key: parseInt(val)})
      });
      const res = await resp.json();
      document.getElementById('msg').textContent = res.message;
      showExplanation(res.explanation);
      refreshTree();
    }

    async function refreshTree(){
      const data = await fetchTree();
      renderTree(data);
    }

    function showExplanation(lines){
      const exp = document.getElementById('explanation');
      exp.innerHTML = lines.map(l => `<div>➡️ ${l}</div>`).join('');
    }

    function renderTree(sourceData){
      const container = document.getElementById('tree');
      container.innerHTML = '';
      if(!sourceData || Object.keys(sourceData).length === 0){
        container.innerHTML = '<p style="padding:10px;color:#666">Tree is empty</p>';
        return;
      }

      const width = container.clientWidth;
      const height = container.clientHeight || 600;

      const svg = d3.select('#tree').append('svg')
        .attr('width', width)
        .attr('height', height);

      const g = svg.append('g').attr('transform', 'translate(40,20)');
      const root = d3.hierarchy(sourceData);
      const treeLayout = d3.tree().size([width - 80, height - 120]);
      treeLayout(root);

      g.selectAll('.link')
        .data(root.links())
        .join('path')
        .attr('class', 'link')
        .attr('d', d3.linkVertical().x(d => d.x).y(d => d.y));

      const node = g.selectAll('.node')
        .data(root.descendants())
        .join('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.x},${d.y})`);

      node.append('circle').attr('r', 18);
      node.append('text')
        .attr('dy', 4)
        .attr('text-anchor', 'middle')
        .text(d => d.data.name);
    }

    refreshTree();
  </script>
</body>
</html>
"""

# ----------------------------
# Flask Routes
# ----------------------------
@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/tree')
def get_tree():
    return jsonify(bst.to_dict())

@app.route('/insert', methods=['POST'])
def insert():
    data = request.get_json()
    key = int(data['key'])
    ok, explanation = bst.insert(key)
    message = f"Inserted {key}" if ok else f"Key {key} already exists"
    return jsonify({'success': ok, 'message': message, 'explanation': explanation})

@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    key = int(data['key'])
    deleted, explanation = bst.delete(key)
    message = f"Deleted {key}" if deleted else f"Key {key} not found"
    return jsonify({'success': deleted, 'message': message, 'explanation': explanation})
def get_page():
    return INDEX_HTML
if __name__ == '__main__':
    app.run(debug=True)
