from flask import Flask, jsonify, render_template_string, request
import math

app = Flask(__name__)

# ---------------------------------
# B-Tree Node Class
# ---------------------------------
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # minimum degree
        self.leaf = leaf
        self.keys = []      # keys
        self.children = []  # children references


# ---------------------------------
# B-Tree Class
# ---------------------------------
class BTree:
    def __init__(self, t=2):
        self.root = BTreeNode(t, True)
        self.t = t
        self.steps = []
        self.highlight_nodes = {}

    # ---------------------------------
    # Insert a key
    # ---------------------------------
    def insert(self, k):
        self.steps.clear()
        self.highlight_nodes.clear()
        self.steps.append(f"Starting insertion of key {k}.")
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            self.steps.append("Root is full. Creating a new root and splitting.")
            new_root = BTreeNode(self.t, False)
            new_root.children.insert(0, root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)
        self.highlight_nodes[k] = "green"
        return self.steps

    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
            self.steps.append(f"Inserted key {k} into leaf node {node.keys}.")
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            self.steps.append(f"Moving to child index {i} of node {node.keys}.")
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.steps.append(f"Child {i} is full. Splitting child.")
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, parent, i):
        t = self.t
        y = parent.children[i]
        z = BTreeNode(t, y.leaf)
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])
        self.steps.append(f"Splitting node {y.keys}, promoting key {y.keys[t - 1]}.")
        z.keys = y.keys[t:(2 * t) - 1]
        y.keys = y.keys[0:t - 1]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]
        self.highlight_nodes[parent.keys[i]] = "yellow"

    # ---------------------------------
    # Search
    # ---------------------------------
    def search(self, k):
        self.steps.clear()
        self.highlight_nodes.clear()
        res = self._search(self.root, k)
        if res:
            self.steps.append(f"Key {k} found in node {res.keys}.")
            self.highlight_nodes[k] = "green"
        else:
            self.steps.append(f"Key {k} not found in the tree.")
        return self.steps

    def _search(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return node
        if node.leaf:
            return None
        self.steps.append(f"Searching key {k} in child {i} of node {node.keys}.")
        return self._search(node.children[i], k)

    # ---------------------------------
    # Convert tree to JSON structure for D3
    # ---------------------------------
    def to_dict(self):
        def node_to_dict(node):
            color = "white"
            for key in node.keys:
                if key in self.highlight_nodes:
                    color = self.highlight_nodes[key]
            d = {
                "name": "|".join(map(str, node.keys)),
                "color": color,
                "children": []
            }
            if not node.leaf:
                for child in node.children:
                    d["children"].append(node_to_dict(child))
            return d
        return node_to_dict(self.root)


# ---------------------------------
# Flask + D3 Frontend
# ---------------------------------
HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>B-Tree Visualizer</title>
  <style>
    body { font-family: Arial; margin: 10px; }
    input, button { padding: 6px; margin: 3px; }
    #tree { width: 100%; height: 600px; border: 1px solid #ccc; margin-top:10px; }
    #steps { background:#f9f9f9; border:1px solid #ccc; padding:10px; margin-top:10px; height:180px; overflow-y:scroll; }
  </style>
</head>
<body>
  <h2>B-Tree Visualizer (Insertion, Search, Auto-Splitting)</h2>
  <input id="key" type="number" placeholder="Enter key">
  <button onclick="insertKey()">Insert</button>
  <button onclick="searchKey()">Search</button>
  <div id="steps">Steps will appear here...</div>
  <div id="tree"></div>

  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
    async function getTree(){ const r=await fetch('/tree'); return await r.json(); }

    async function insertKey(){
      const key=document.getElementById('key').value;
      const r=await fetch('/insert',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key})});
      const d=await r.json(); showSteps(d.steps); draw();
    }

    async function searchKey(){
      const key=document.getElementById('key').value;
      const r=await fetch('/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key})});
      const d=await r.json(); showSteps(d.steps); draw();
    }

    function showSteps(lines){
      document.getElementById('steps').innerHTML = lines.map(l=>`<div>➡️ ${l}</div>`).join('');
    }

    async function draw(){
      const data = await getTree();
      const div = document.getElementById('tree'); div.innerHTML='';
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
      n.append('rect').attr('width',60).attr('height',30).attr('x',-30).attr('y',-15)
        .attr('stroke','black').attr('fill',d=>d.data.color);
      n.append('text').attr('dy',4).attr('text-anchor','middle').text(d=>d.data.name);
    }
    draw();
  </script>
</body>
</html>
"""

btree = BTree(t=2)
for val in [10, 20, 5, 6, 12, 30, 7, 17]:
    btree.insert(val)

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/tree')
def tree():
    return jsonify(btree.to_dict())

@app.route('/insert', methods=['POST'])
def insert():
    key = int(request.json['key'])
    steps = btree.insert(key)
    return jsonify({"steps": steps})

@app.route('/search', methods=['POST'])
def search():
    key = int(request.json['key'])
    steps = btree.search(key)
    return jsonify({"steps": steps})

if __name__ == '__main__':
    app.run(debug=True)
