from flask import Flask, render_template_string,send_from_directory
from Tree.AVL import avl_bp
from BST.BinarySearchTree import bst_bp
from Tree.Btree import btree_bp
from Graph.Spanning import spanning_bp
from Tree.TreeRotation import rotation_bp
from Tree.TreeTravel import traversal_bp
from Stack.StackUsingArray import stack_array
from Graph.Dijkstra import dijkstra_bp
from DynamicMemoryAllocation.DMA import memory_bp
from Graph.Kruskal import kruskal_bp
from Graph.Prims import prims_bp
from Queue.QueueUsingArray import queue_bp
from Queue.QueueUsingLinkedList import queue_linked_list_bp
from Stack.BalancingSymbol import balancing_symbol_bp
app = Flask(__name__)
# Register all blueprints
app.register_blueprint(avl_bp)
app.register_blueprint(bst_bp)
app.register_blueprint(btree_bp)
app.register_blueprint(spanning_bp)
app.register_blueprint(rotation_bp)
app.register_blueprint(traversal_bp)
app.register_blueprint(stack_array)
# kruskal_bp.register_blueprint(balancing_symbol_bp)
app.register_blueprint(memory_bp)
app.register_blueprint(kruskal_bp)
app.register_blueprint(dijkstra_bp)
app.register_blueprint(prims_bp)
app.register_blueprint(queue_bp)
app.register_blueprint(balancing_symbol_bp)
app.register_blueprint(queue_linked_list_bp)
HTML = open("Main.html", encoding="utf-8").read()
@app.route('/')
def home():
    return render_template_string(HTML)
@app.route('/Style.css')
def css():
    return send_from_directory('.', 'Style.css')