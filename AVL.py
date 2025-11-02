from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# ----------------------------
# AVL TREE NODE
# ----------------------------
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # For balance factor tracking


# ----------------------------
# AVL TREE CLASS
# ----------------------------
class AVLTree:
    def __init__(self):
        self.root = None
        self.steps = []
        self.highlight_nodes = {}

    # --------- Utility ---------
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    # --------- Insertion ---------
    def insert(self, key):
        self.steps.clear()
        self.highlight_nodes.clear()
        self.steps.append(f"Starting insertion of {key}.")
        self.root = self._insert(self.root, key)
        self.highlight_nodes[key] = "green"
        return self.steps

    def _insert(self, node, key):
        if not node:
            self.steps.append(f"Inserted {key} as a new node.")
            return Node(key)
        if key < node.key:
            self.steps.append(f"{key} < {node.key}: inserting into LEFT subtree.")
            node.left = self._insert(node.left, key)
        elif key > node.key:
            self.steps.append(f"{key} > {node.key}: inserting into RIGHT subtree.")
            node.right = self._insert(node.right, key)
        else:
            self.steps.append(f"{key} already exists. Skipping.")
            return node

        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Balance check
        balance = self.get_balance(node)
        self.steps.append(f"Node {node.key} balance = {balance}.")

        # Rotation Cases
        # LL
        if balance > 1 and key < node.left.key:
            self.steps.append(f"Left-Left (LL) imbalance detected at {node.key}. Performing RIGHT rotation.")
            self.highlight_nodes[node.key] = "blue"
            node = self.right_rotate(node)
        # RR
        elif balance < -1 and key > node.right.key:
            self.steps.append(f"Right-Right (RR) imbalance detected at {node.key}. Performing LEFT rotation.")
            self.highlight_nodes[node.key] = "blue"
            node = self.left_rotate(node)
        # LR
        elif balance > 1 and key > node.left.key:
            self.steps.append(f"Left-Right (LR) imbalance detected at {node.key}. Performing LEFT rotation on left child, then RIGHT rotation.")
            self.highlight_nodes[node.key] = "blue"
            node.left = self.left_rotate(node.left)
            node = self.right_rotate(node)
        # RL
        elif balance < -1 and key < node.right.key:
            self.steps.append(f"Right-Left (RL) imbalance detected at {node.key}. Performing RIGHT rotation on right child, then LEFT rotation.")
            self.highlight_nodes[node.key] = "blue"
            node.right = self.right_rotate(node.right)
            node = self.left_rotate(node)

        return node

    # --------- Deletion ---------
    def delete(self, key):
        self.steps.clear()
        self.highlight_nodes.clear()
        self.steps.append(f"Starting deletion of {key}.")
        self.root = self._delete(self.root, key)
        self.highlight_nodes[key] = "red"
        return self.steps

    def _delete(self, node, key):
        if not node:
            self.steps.append(f"{key} not found in tree.")
            return node
        if key < node.key:
            self.steps.append(f"{key} < {node.key}: searching LEFT subtree.")
            node.left = self._delete(node.left, key)
        elif key > node.key:
            self.steps.append(f"{key} > {node.key}: searching RIGHT subtree.")
            node.right = self._delete(node.right, key)
        else:
            self.steps.append(f"Found node {key}. Deleting it.")
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            succ = self.get_min(node.right)
            self.steps.append(f"Node {key} has two children. Inorder successor is {succ.key}. Replacing value.")
            node.key = succ.key
            self.highlight_nodes[succ.key] = "yellow"
            node.right = self._delete(node.right, succ.key)

        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)
        self.steps.append(f"Node {node.key} balance after deletion = {balance}.")

        # Rebalance
        # LL
        if balance > 1 and self.get_balance(node.left) >= 0:
            self.steps.append(f"LL case detected at {node.key}. Performing RIGHT rotation.")
            return self.right_rotate(node)
        # LR
        if balance > 1 and self.get_balance(node.left) < 0:
            self.steps.append(f"LR case detected at {node.key}. Performing LEFT rotation on left child, then RIGHT rotation.")
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # RR
        if balance < -1 and self.get_balance(node.right) <= 0:
            self.steps.append(f"RR case detected at {node.key}. Performing LEFT rotation.")
            return self.left_rotate(node)
        # RL
        if balance < -1 and self.get_balance(node.right) > 0:
            self.steps.append(f"RL case detected at {node.key}. Performing RIGHT rotation on right child, then LEFT rotation.")
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def get_min(self, node):
        while node.left:
            node = node.left
        return node

    # --------- Rotations ---------
    def left_rotate(self, z):
        self.steps.append(f"Left rotation: {z.key} becomes left child of {z.right.key}.")
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        self.highlight_nodes[y.key] = "green"
        return y

    def right_rotate(self, z):
        self.steps.append(f"Right rotation: {z.key} becomes right child of {z.left.key}.")
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        self.highlight_nodes[y.key] = "green"
        return y

    # --------- To Dictionary for Visualization ---------
    def to_dict(self):
        def to_dict(node):
            if not node:
                return None
            color = self.highlight_nodes.get(node.key, "white")
            d = {"name": str(node.key), "color": color}
            children = []
            if node.left:
                children.append(to_dict(node.left))
            if node.right:
                children.append(to_dict(node.right))
            if children:
                d["children"] = children
            return d
        return to_dict(self.root)


# ----------------------------
# Flask + D3.js Visualization
# ----------------------------
HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AVL Tree Visualizer</title>
  <style>
    body { font-family: Arial; margin: 10px; }
    input, button { padding: 6px; margin: 3px; }
    #tree { width: 100%; height: 600px; border: 1px solid #ccc; margin-top:10px; }
    #steps { background:#f9f9f9; border:1px solid #ccc; padding:10px; margin-top:10px; height:180px; overflow-y:scroll; }
  </style>
</head>
<body>
  <h2>AVL Tree Visualizer (Insert, Delete, Auto-Balancing Rotations)</h2>
  <input id="key" type="number" placeholder="Enter key">
  <button onclick="insertNode()">Insert</button>
  <button onclick="deleteNode()">Delete</button>
  <div id="steps">Explanation will appear here...</div>
  <div id="tree"></div>

  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
    async function getTree(){ const r=await fetch('/tree'); return await r.json(); }

    async function insertNode(){
      const key=document.getElementById('key').value;
      const r=await fetch('/insert',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key})});
      const d=await r.json(); showSteps(d.steps); draw();
    }

    async function deleteNode(){
      const key=document.getElementById('key').value;
      const r=await fetch('/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key})});
      const d=await r.json(); showSteps(d.steps); draw();
    }

    function showSteps(lines){
      document.getElementById('steps').innerHTML = lines.map(l=>`<div>➡️ ${l}</div>`).join('');
    }

    async function draw(){
      const data=await getTree();
      const div=document.getElementById('tree'); div.innerHTML='';
      if(!data){ div.innerHTML='<p>Empty tree</p>'; return; }
      const width=div.clientWidth,height=600;
      const svg=d3.select('#tree').append('svg').attr('width',width).attr('height',height);
      const g=svg.append('g').attr('transform','translate(40,20)');
      const root=d3.hierarchy(data); d3.tree().size([width-80,height-120])(root);
      g.selectAll('.link').data(root.links()).join('path')
        .attr('fill','none').attr('stroke','#aaa')
        .attr('d',d3.linkVertical().x(d=>d.x).y(d=>d.y));
      const n=g.selectAll('.node').data(root.descendants()).join('g')
        .attr('transform',d=>`translate(${d.x},${d.y})`);
      n.append('circle').attr('r',18).attr('stroke','black').attr('fill',d=>d.data.color);
      n.append('text').attr('dy',4).attr('text-anchor','middle').text(d=>d.data.name);
    }
    draw();
  </script>
</body>
</html>
"""
def get_page():
    avlIn = AVLTree()
    for value in [30, 10, 50, 5, 20, 40, 60]:
        avlIn.insert(value)

    return HTML
avl = AVLTree()
for val in [30, 10, 50, 5, 20, 40, 60]:
    avl.insert(val)
@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/tree')
def tree():
    return jsonify(avl.to_dict())

@app.route('/insert', methods=['POST'])
def insert():
    key = int(request.json['key'])
    steps = avl.insert(key)
    return jsonify({"steps": steps})

@app.route('/delete', methods=['POST'])
def delete():
    key = int(request.json['key'])
    steps = avl.delete(key)
    return jsonify({"steps": steps})

if __name__ == '__main__':
    app.run(debug=True)
