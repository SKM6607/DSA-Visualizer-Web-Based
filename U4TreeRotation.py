from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# ----------------------------
# Binary Search Tree Node
# ----------------------------
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


# ----------------------------
# Binary Search Tree with Rotations and Explanations
# ----------------------------
class BST:
    def __init__(self):
        self.root = None
        self.highlight_nodes = {}  # {key: color}

    # ---------- INSERT ----------
    def insert(self, key):
        explanation = []
        self.highlight_nodes.clear()
        if not self.root:
            self.root = Node(key)
            explanation.append(f"Tree is empty. Inserting {key} as root node.")
            self.highlight_nodes[key] = "green"
            return True, explanation
        result, explanation = self._insert(self.root, key, explanation)
        self.highlight_nodes[key] = "green"
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
        self.highlight_nodes.clear()
        self.root, deleted, explanation = self._delete(self.root, key, explanation)
        self.highlight_nodes[key] = "red"
        return deleted, explanation

    def _delete(self, node, key, explanation):
        if not node:
            explanation.append(f"{key} not found in the tree.")
            return node, False, explanation
        if key < node.key:
            explanation.append(f"{key} < {node.key}: searching LEFT subtree.")
            node.left, deleted, explanation = self._delete(node.left, key, explanation)
        elif key > node.key:
            explanation.append(f"{key} > {node.key}: searching RIGHT subtree.")
            node.right, deleted, explanation = self._delete(node.right, key, explanation)
        else:
            explanation.append(f"Node {key} found — starting deletion process.")
            deleted = True
            if not node.left:
                explanation.append(f"{key} has no LEFT child — replace with RIGHT child.")
                return node.right, deleted, explanation
            elif not node.right:
                explanation.append(f"{key} has no RIGHT child — replace with LEFT child.")
                return node.left, deleted, explanation
            else:
                explanation.append(f"{key} has TWO children — finding inorder successor.")
                succ = node.right
                while succ.left:
                    succ = succ.left
                self.highlight_nodes[succ.key] = "yellow"
                explanation.append(f"Inorder successor of {key} is {succ.key}. Replacing {key} with {succ.key}.")
                node.key = succ.key
                node.right, _, explanation = self._delete(node.right, succ.key, explanation)
        return node, deleted, explanation

    # ---------- ROTATIONS ----------
    def left_rotate(self, key):
        explanation = [f"Starting LEFT rotation at node {key}."]
        self.highlight_nodes.clear()
        self.highlight_nodes[key] = "blue"
        self.root, explanation = self._left_rotate(self.root, key, explanation)
        return explanation

    def _left_rotate(self, node, key, explanation):
        if not node:
            explanation.append(f"Node {key} not found.")
            return node, explanation
        if key < node.key:
            node.left, explanation = self._left_rotate(node.left, key, explanation)
        elif key > node.key:
            node.right, explanation = self._left_rotate(node.right, key, explanation)
        else:
            if not node.right:
                explanation.append(f"Cannot rotate LEFT — node {key} has no RIGHT child.")
                return node, explanation
            new_root = node.right
            explanation.append(f"Performing LEFT rotation: {node.key} moves down, {new_root.key} becomes new parent.")
            self.highlight_nodes[new_root.key] = "green"
            node.right = new_root.left
            new_root.left = node
            return new_root, explanation
        return node, explanation

    def right_rotate(self, key):
        explanation = [f"Starting RIGHT rotation at node {key}."]
        self.highlight_nodes.clear()
        self.highlight_nodes[key] = "blue"
        self.root, explanation = self._right_rotate(self.root, key, explanation)
        return explanation

    def _right_rotate(self, node, key, explanation):
        if not node:
            explanation.append(f"Node {key} not found.")
            return node, explanation
        if key < node.key:
            node.left, explanation = self._right_rotate(node.left, key, explanation)
        elif key > node.key:
            node.right, explanation = self._right_rotate(node.right, key, explanation)
        else:
            if not node.left:
                explanation.append(f"Cannot rotate RIGHT — node {key} has no LEFT child.")
                return node, explanation
            new_root = node.left
            explanation.append(f"Performing RIGHT rotation: {node.key} moves down, {new_root.key} becomes new parent.")
            self.highlight_nodes[new_root.key] = "green"
            node.left = new_root.right
            new_root.right = node
            return new_root, explanation
        return node, explanation

    def left_right_rotate(self, key):
        explanation = [f"Starting LEFT-RIGHT rotation at node {key}."]
        self.highlight_nodes.clear()
        self.highlight_nodes[key] = "blue"
        explanation.append("Step 1: Perform LEFT rotation on LEFT child.")
        self.root, explanation = self._left_right_rotate(self.root, key, explanation)
        return explanation

    def _left_right_rotate(self, node, key, explanation):
        if not node:
            explanation.append(f"Node {key} not found.")
            return node, explanation
        if key < node.key:
            node.left, explanation = self._left_right_rotate(node.left, key, explanation)
        elif key > node.key:
            node.right, explanation = self._left_right_rotate(node.right, key, explanation)
        else:
            if not node.left:
                explanation.append(f"Cannot perform LEFT-RIGHT rotation — node {key} has no LEFT child.")
                return node, explanation
            explanation.append(f"Performing LEFT rotation on LEFT child ({node.left.key}).")
            node.left, _ = self._left_rotate(node.left, node.left.key, explanation)
            explanation.append("Now performing RIGHT rotation on node itself.")
            node, _ = self._right_rotate(node, key, explanation)
            explanation.append(f"LEFT-RIGHT rotation completed at node {key}.")
        return node, explanation

    def right_left_rotate(self, key):
        explanation = [f"Starting RIGHT-LEFT rotation at node {key}."]
        self.highlight_nodes.clear()
        self.highlight_nodes[key] = "blue"
        explanation.append("Step 1: Perform RIGHT rotation on RIGHT child.")
        self.root, explanation = self._right_left_rotate(self.root, key, explanation)
        return explanation

    def _right_left_rotate(self, node, key, explanation):
        if not node:
            explanation.append(f"Node {key} not found.")
            return node, explanation
        if key < node.key:
            node.left, explanation = self._right_left_rotate(node.left, key, explanation)
        elif key > node.key:
            node.right, explanation = self._right_left_rotate(node.right, key, explanation)
        else:
            if not node.right:
                explanation.append(f"Cannot perform RIGHT-LEFT rotation — node {key} has no RIGHT child.")
                return node, explanation
            explanation.append(f"Performing RIGHT rotation on RIGHT child ({node.right.key}).")
            node.right, _ = self._right_rotate(node.right, node.right.key, explanation)
            explanation.append("Now performing LEFT rotation on node itself.")
            node, _ = self._left_rotate(node, key, explanation)
            explanation.append(f"RIGHT-LEFT rotation completed at node {key}.")
        return node, explanation

    # ---------- TREE TO DICT ----------
    def to_dict(self):
        def node_to_dict(n):
            if not n:
                return None
            color = self.highlight_nodes.get(n.key, "white")
            d = {"name": str(n.key), "color": color}
            children = []
            if n.left:
                children.append(node_to_dict(n.left))
            if n.right:
                children.append(node_to_dict(n.right))
            if children:
                d["children"] = children
            return d
        return node_to_dict(self.root) if self.root else {}


# ----------------------------
# Flask Web App
# ----------------------------
HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Color-Coded BST Visualizer</title>
  <style>
    body { font-family: Arial; margin: 10px; }
    input, button { padding: 6px; margin: 3px; }
    #tree { width: 100%; height: 600px; border: 1px solid #ddd; margin-top:10px; }
    #explanation { background:#f9f9f9; border:1px solid #ccc; padding:10px; margin-top:10px; height:180px; overflow-y:scroll; }
  </style>
</head>
<body>
  <h2>Color-Coded BST Visualizer (Insert, Delete, Rotations)</h2>
  <input id="keyInput" type="number" placeholder="Enter key" />
  <button onclick="insertNode()">Insert</button>
  <button onclick="deleteNode()">Delete</button>
  <button onclick="rotate('left')">Left Rotate</button>
  <button onclick="rotate('right')">Right Rotate</button>
  <button onclick="rotate('left-right')">Left-Right Rotate</button>
  <button onclick="rotate('right-left')">Right-Left Rotate</button>
  <div id="explanation">Explanation will appear here...</div>
  <div id="tree"></div>

  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
    async function fetchTree(){ const res=await fetch('/tree'); return await res.json(); }

    async function insertNode(){ const k=document.getElementById('keyInput').value; const r=await fetch('/insert',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:k})}); const d=await r.json(); showExp(d.explanation); draw(); }
    async function deleteNode(){ const k=document.getElementById('keyInput').value; const r=await fetch('/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:k})}); const d=await r.json(); showExp(d.explanation); draw(); }
    async function rotate(t){ const k=document.getElementById('keyInput').value; const r=await fetch('/rotate/'+t,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:k})}); const d=await r.json(); showExp(d.explanation); draw(); }

    function showExp(lines){ document.getElementById('explanation').innerHTML = lines.map(l=>`<div>➡️ ${l}</div>`).join(''); }

    async function draw(){
      const data = await fetchTree();
      const div = document.getElementById('tree'); div.innerHTML='';
      if(!data || Object.keys(data).length===0){ div.innerHTML='<p>Empty tree</p>'; return; }
      const width=div.clientWidth,height=600;
      const svg=d3.select('#tree').append('svg').attr('width',width).attr('height',height);
      const g=svg.append('g').attr('transform','translate(40,20)');
      const root=d3.hierarchy(data); d3.tree().size([width-80,height-120])(root);
      g.selectAll('.link').data(root.links()).join('path').attr('fill','none').attr('stroke','#ccc').attr('d',d3.linkVertical().x(d=>d.x).y(d=>d.y));
      const n=g.selectAll('.node').data(root.descendants()).join('g').attr('transform',d=>`translate(${d.x},${d.y})`);
      n.append('circle').attr('r',18).attr('stroke','black').attr('fill',d=>d.data.color);
      n.append('text').attr('dy',4).attr('text-anchor','middle').text(d=>d.data.name);
    }
    draw();
  </script>
</body>
</html>
"""

bst = BST()
for v in [40, 20, 60, 10, 30, 50, 70]:
    bst.insert(v)


@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/tree')
def tree():
    return jsonify(bst.to_dict())

@app.route('/insert', methods=['POST'])
def insert():
    key = int(request.json['key'])
    _, exp = bst.insert(key)
    return jsonify({'explanation': exp})

@app.route('/delete', methods=['POST'])
def delete():
    key = int(request.json['key'])
    _, exp = bst.delete(key)
    return jsonify({'explanation': exp})

@app.route('/rotate/<mode>', methods=['POST'])
def rotate(mode):
    key = int(request.json['key'])
    if mode == 'left':
        exp = bst.left_rotate(key)
    elif mode == 'right':
        exp = bst.right_rotate(key)
    elif mode == 'left-right':
        exp = bst.left_right_rotate(key)
    else:
        exp = bst.right_left_rotate(key)
    return jsonify({'explanation': exp})

if __name__ == '__main__':
    app.run(debug=True)
