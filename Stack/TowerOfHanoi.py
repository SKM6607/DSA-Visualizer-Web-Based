from flask import Blueprint, jsonify, render_template_string, request, Blueprint

app = Blueprint('towerOfHanoi',__name__,url_prefix='tower_of_hanoi')

# ---- Tower of Hanoi Logic ----
moves = []
towers = {"A": [], "B": [], "C": []}
disk_colors = ["#FF5733", "#FFC300", "#33FF57", "#3380FF", "#DA33FF", "#33FFF5", "#FF8C00", "#A569BD"]
stem_colors = {"A": "#6A0DAD", "B": "#1E8449", "C": "#2874A6"}


def tower_of_hanoi(n, from_rod, to_rod, aux_rod):
    """Recursive Tower of Hanoi algorithm"""
    if n == 1:
        moves.append((from_rod, to_rod))
        return
    tower_of_hanoi(n - 1, from_rod, aux_rod, to_rod)
    moves.append((from_rod, to_rod))
    tower_of_hanoi(n - 1, aux_rod, to_rod, from_rod)


def reset_towers(n):
    """Initialize towers with n disks"""
    global towers, moves
    towers = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    moves = []


@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Tower of Hanoi Visualizer</title>
    <style>
        body { font-family: Arial; text-align: center; background: #f0f2f5; }
        canvas { background: white; border: 2px solid #333; margin-top: 20px; }
        input, button { padding: 10px 15px; margin: 5px; font-size: 16px; }
        h1 { margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🧩 Tower of Hanoi Visualizer</h1>
    <div>
        <label for="diskInput"><b>Enter number of disks:</b></label>
        <input type="number" id="diskInput" min="3" max="8" value="4">
        <button onclick="startSimulation()">Start Simulation</button>
    </div>
    <canvas id="canvas" width="900" height="400"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let towers = {};
        let moves = [];
        let moveIndex = 0;
        let diskColors = [];
        let stemColors = {};

        async function startSimulation() {
            const n = document.getElementById('diskInput').value;
            const response = await fetch('/start?n=' + n);
            const data = await response.json();

            towers = data.towers;
            moves = data.moves;
            diskColors = data.disk_colors;
            stemColors = data.stem_colors;
            moveIndex = 0;
            drawTowers();

            const interval = setInterval(() => {
                if (moveIndex < moves.length) {
                    const [from, to] = moves[moveIndex];
                    if (towers[from].length > 0) {
                        const disk = towers[from].pop();
                        towers[to].push(disk);
                    }
                    moveIndex++;
                    drawTowers();
                } else {
                    clearInterval(interval);
                }
            }, 800);
        }

        function drawTowers() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const towerX = [200, 450, 700];
            const towerNames = ["A", "B", "C"];
            const towerColor = [stemColors["A"], stemColors["B"], stemColors["C"]];

            // Draw stems
            for (let i = 0; i < 3; i++) {
                ctx.fillStyle = towerColor[i];
                ctx.fillRect(towerX[i] - 10, 100, 20, 200);
                ctx.fillStyle = "#333";
                ctx.fillText(towerNames[i], towerX[i] - 5, 320);
            }

            // Draw disks
            for (let i = 0; i < towerNames.length; i++) {
                const tower = towers[towerNames[i]];
                for (let j = 0; j < tower.length; j++) {
                    const diskNum = tower[j];
                    const diskWidth = diskNum * 30;
                    const x = towerX[i] - diskWidth / 2;
                    const y = 280 - j * 25;
                    ctx.fillStyle = diskColors[(diskNum - 1) % diskColors.length];
                    ctx.fillRect(x, y, diskWidth, 20);
                    ctx.strokeRect(x, y, diskWidth, 20);
                }
            }
        }
    </script>
</body>
</html>
    ''')


@app.route('/start')
def start():
    """Start the simulation based on user input"""
    n = int(request.args.get('n', 4))
    reset_towers(n)
    tower_of_hanoi(n, "A", "C", "B")
    return jsonify({
        "towers": towers,
        "moves": moves,
        "disk_colors": disk_colors,
        "stem_colors": stem_colors
    })


if __name__ == '__main__':
    reset_towers(4)
    app.run(debug=True)
