from flask import Flask, jsonify, render_template_string, request
from collections import deque

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
            if not node.left:
                explanation.append(f"{key} has no LEFT child — replacing with RIGHT child.")
                return node.right, deleted, explanation
            elif not node.right:
                explanation.append(f"{key} has no RIGHT child — replacing with LEFT child.")
                return node.left, deleted, explanation
            else:
                explanation.append(f"{key} has TWO children — finding inorder successor.")
                succ = node.right
                while succ.left:
                    succ = succ.left
                explanation.append(f"Inorder successor of {key} is {succ.key}. Replacing {key} with {succ.key}.")
                node.key = succ.key
                node.right, _, explanation = self._delete(node.right, succ.key, explanation)
        return node, deleted, explanation

    # ---------- TRAVERSALS ----------
    def inorder(self):
        res, steps = [], []
        steps.append("Starting Inorder Traversal (Left → Root → Right).")
        self._inorder(self.root, res, steps)
        return res, steps

    def _inorder(self, node, res, steps):
        if node:
            self._inorder(node.left, res, steps)
            res.append(node.key)
            steps.append(f"Visited node {node.key}.")
            self._inorder(node.right, res, steps)

    def preorder(self):
        res, steps = [], []
        steps.append("Starting Preorder Traversal (Root → Left → Right).")
        self._preorder(self.root, res, steps)
        return res, steps

    def _preorder(self, node, res, steps):
        if node:
            res.append(node.key)
            steps.append(f"Visited node {node.key}.")
            self._preorder(node.left, res, steps)
            self._preorder(node.right, res, steps)

    def postorder(self):
        res, steps = [], []
        steps.append("Starting Postorder Traversal (Left → Right → Root).")
        self._postorder(self.root, res, steps)
        return res, steps

    def _postorder(self, node, res, steps):
        if node:
            self._postorder(node.left, res, steps)
            self._postorder(node.right, res, steps)
            res.append(node.key)
            steps.append(f"Visited node {node.key}.")

    def bfs(self):
        res, steps = [], []
        if not self.root:
            steps.append("Tree is empty.")
            return res, steps
        steps.append("Starting Breadth-First Search (Level Order).")
        q = deque([self.root])
        while q:
            node = q.popleft()
            res.append(node.key)
            steps.append(f"Visited node {node.key}.")
            if node.left:
                steps.append(f"Enqueue LEFT child {node.left.key}.")
                q.append(node.left)
            if node.right:
                steps.append(f"Enqueue RIGHT child {node.right.key}.")
                q.append(node.right)
        return res, steps

    def dfs(self):
        res, steps = [], []
        if not self.root:
            steps.append("Tree is empty.")
            return res, steps
        steps.append("Starting Depth-First Search (using Stack).")
        stack = [self.root]
        while stack:
            node = stack.pop()
            res.append(node.key)
            steps.append(f"Visited node {node.key}.")
            if node.right:
                steps.append(f"Pushed RIGHT child {node.right.key}.")
                stack.append(node.right)
            if node.left:
                steps.append(f"Pushed LEFT child {node.left.key}.")
                stack.append(node.left)
        return res, steps

    # ---------- CONVERT TREE ----------
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


# Create global BST
bst = BST()
for v in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(v)

# ----------------------------
# Flask Routes
# ----------------------------
HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>BST Traversal Visualizer with Explanation</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 10px; }
    input, button { padding: 6px; margin: 4px; }
    #tree { width: 100%; height: 600px; border: 1px solid #ddd; margin-top:10px; }
    #explanation { background: #f9f9f9; border: 1px solid #ccc; padding: 10px; margin-top: 10px; height: 180px; overflow-y: scroll; }
  </style>
</head>
<body>
  <h2>Binary Search Tree Visualizer (Insert, Delete, Traversals)</h2>
  <div>
    <input id="keyInput" type="number" placeholder="Enter key" />
    <button onclick="insertKey()">Insert</button>
    <button onclick="deleteKey()">Delete</button>
    <button onclick="traverse('inorder')">Inorder</button>
    <button onclick="traverse('preorder')">Preorder</button>
    <button onclick="traverse('postorder')">Postorder</button>
    <button onclick="traverse('bfs')">BFS</button>
    <button onclick="traverse('dfs')">DFS</button>
  </div>
  <div id="explanation">Explanation will appear here...</div>
  <div id="tree"></div>

  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
    async function fetchTree() {
      const resp = await fetch('/tree');
      return await resp.json();
    }

    async function insertKey(){
      const val = document.getElementById('keyInput').value;
      const resp = await fetch('/insert', {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({key: parseInt(val)})});
      const res = await resp.json();
      showExplanation(res.explanation);
      refreshTree();
    }

    async function deleteKey(){
      const val = document.getElementById('keyInput').value;
      const resp = await fetch('/delete', {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({key: parseInt(val)})});
      const res = await resp.json();
      showExplanation(res.explanation);
      refreshTree();
    }

    async function traverse(type){
      const resp = await fetch(`/traverse/${type}`);
      const res = await resp.json();
      showExplanation(res.steps);
      alert(`${type.toUpperCase()} Traversal: ${res.result.join(', ')}`);
    }

    function showExplanation(lines){
      const exp = document.getElementById('explanation');
      exp.innerHTML = lines.map(l => `<div>➡️ ${l}</div>`).join('');
    }

    async function refreshTree(){
      const data = await fetchTree();
      renderTree(data);
    }

    function renderTree(data){
      const container = document.getElementById('tree');
      container.innerHTML = '';
      if(!data || Object.keys(data).length === 0){
        container.innerHTML = '<p style="padding:10px;color:#666">Tree is empty</p>';
        return;
      }

      const width = container.clientWidth;
      const height = container.clientHeight || 600;
      const svg = d3.select('#tree').append('svg').attr('width', width).attr('height', height);
      const g = svg.append('g').attr('transform', 'translate(40,20)');
      const root = d3.hierarchy(data);
      const treeLayout = d3.tree().size([width - 80, height - 120]);
      treeLayout(root);

      g.selectAll('.link')
        .data(root.links())
        .join('path')
        .attr('stroke', '#ccc')
        .attr('fill', 'none')
        .attr('d', d3.linkVertical().x(d => d.x).y(d => d.y));

      const node = g.selectAll('.node')
        .data(root.descendants())
        .join('g')
        .attr('transform', d => `translate(${d.x},${d.y})`);

      node.append('circle').attr('r', 18).attr('stroke', 'steelblue').attr('fill', 'white');
      node.append('text').attr('dy', 4).attr('text-anchor', 'middle').text(d => d.data.name);
    }

    refreshTree();
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/tree')
def get_tree():
    return jsonify(bst.to_dict())

@app.route('/insert', methods=['POST'])
def insert():
    key = int(request.json['key'])
    ok, explanation = bst.insert(key)
    return jsonify({'success': ok, 'explanation': explanation})

@app.route('/delete', methods=['POST'])
def delete():
    key = int(request.json['key'])
    deleted, explanation = bst.delete(key)
    return jsonify({'success': deleted, 'explanation': explanation})

@app.route('/traverse/<mode>')
def traverse(mode):
    if mode == 'inorder':
        res, steps = bst.inorder()
    elif mode == 'preorder':
        res, steps = bst.preorder()
    elif mode == 'postorder':
        res, steps = bst.postorder()
    elif mode == 'bfs':
        res, steps = bst.bfs()
    elif mode == 'dfs':
        res, steps = bst.dfs()
    else:
        return jsonify({'error': 'Invalid mode'})
    return jsonify({'result': res, 'steps': steps})
def get_page():
    return HTML_PAGE
if __name__ == '__main__':
    app.run(debug=True)
