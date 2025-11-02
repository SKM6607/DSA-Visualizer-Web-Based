from flask import Flask
import AVL, BST, Btree, Spanning, TreeRotation, TreeTravel

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html><body>
    <h1>Welcome to the Unified Flask App</h1>
    <ul>
      <li><a href="/page1">Page 1</a></li>
      <li><a href="/page2">Page 2</a></li>
      <li><a href="/page3">Page 3</a></li>
      <li><a href="/page4">Page 4</a></li>
      <li><a href="/page5">Page 5</a></li>
      <li><a href="/page6">Page 6</a></li>
    </ul>
    </body></html>
    """

@app.route('/page1')
def show_page1():
    return AVL.get_page()

@app.route('/page2')
def show_page2():
    return BST.get_page()

@app.route('/page3')
def show_page3():
    return Btree.get_page()

@app.route('/page4')
def show_page4():
    return Spanning.get_page()

@app.route('/page5')
def show_page5():
    return TreeRotation.get_page()

@app.route('/page6')
def show_page6():
    return TreeTravel.get_page()

if __name__ == '__main__':
    app.run(debug=True)
