from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ------------------------------
# Data Structure: Dynamic Memory Allocation (First Fit)
# ------------------------------

class MemoryBlock:
    def __init__(self, start, size, allocated=False, process_id=None):
        self.start = start
        self.size = size
        self.allocated = allocated
        self.process_id = process_id
        self.end = start + size - 1

    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "size": self.size,
            "allocated": self.allocated,
            "process_id": self.process_id
        }


class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        self.blocks = [MemoryBlock(0, total_size)]  # initially one free block

    def allocate(self, process_id, size):
        """Allocate memory using First Fit strategy"""
        for block in self.blocks:
            if not block.allocated and block.size >= size:
                new_block = MemoryBlock(block.start, size, True, process_id)
                block.start += size
                block.size -= size
                if block.size == 0:
                    self.blocks.remove(block)
                self.blocks.append(new_block)
                self.blocks.sort(key=lambda x: x.start)
                return f"Process {process_id} allocated {size} units."
        return "Insufficient memory to allocate."

    def deallocate(self, process_id):
        """Free memory of a process"""
        for block in self.blocks:
            if block.allocated and block.process_id == process_id:
                block.allocated = False
                block.process_id = None
                self.merge_free_blocks()
                return f"Process {process_id} deallocated successfully."
        return f"No block found for Process {process_id}."

    def merge_free_blocks(self):
        """Merge adjacent free blocks"""
        self.blocks.sort(key=lambda x: x.start)
        merged = []
        for block in self.blocks:
            if merged and not block.allocated and not merged[-1].allocated and merged[-1].end + 1 == block.start:
                merged[-1].end = block.end
                merged[-1].size += block.size
            else:
                merged.append(block)
        self.blocks = merged

    def to_list(self):
        return [b.to_dict() for b in sorted(self.blocks, key=lambda x: x.start)]


# Create global memory manager
memory = MemoryManager(total_size=500)

# ------------------------------
# Flask Routes
# ------------------------------

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dynamic Memory Allocation Visualizer</title>
        <style>
            body { font-family: Arial; text-align: center; background: #f8fafc; margin-top: 50px; }
            canvas { border: 2px solid #333; background: white; margin-top: 20px; }
            input, button { padding: 8px; margin: 5px; font-size: 16px; }
            .legend { margin-top: 15px; }
            .box { display: inline-block; width: 20px; height: 20px; margin-right: 5px; border: 1px solid #333; vertical-align: middle; }
        </style>
    </head>
    <body>
        <h2>💾 Dynamic Memory Allocation (First Fit Simulation)</h2>

        <div>
            <input type="text" id="pid" placeholder="Process ID">
            <input type="number" id="size" placeholder="Memory Size">
            <button onclick="allocate()">Allocate</button>
            <button onclick="deallocate()">Deallocate</button>
        </div>

        <p id="status"></p>

        <div class="legend">
            <div class="box" style="background:#8ef58e"></div> Free Block
            <div class="box" style="background:#f58e8e"></div> Allocated Block
        </div>

        <canvas id="canvas" width="1100" height="400"></canvas>

        <script>
            async function allocate() {
                let pid = document.getElementById("pid").value;
                let size = parseInt(document.getElementById("size").value);
                if(!pid || !size) return alert("Enter process ID and size.");
                let res = await fetch(`/allocate?pid=${pid}&size=${size}`);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawMemory(data.memory);
            }

            async function deallocate() {
                let pid = document.getElementById("pid").value;
                if(!pid) return alert("Enter process ID to deallocate.");
                let res = await fetch(`/deallocate?pid=${pid}`);
                let data = await res.json();
                document.getElementById("status").innerText = data.message;
                drawMemory(data.memory);
            }

            function drawMemory(blocks) {
                let canvas = document.getElementById("canvas");
                let ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                let x = 50, y = 150;
                let scale = 2;  // pixels per memory unit

                ctx.font = "14px Arial";
                ctx.fillText("Memory Start (0)", 50, 130);

                for (let block of blocks) {
                    let width = block.size * scale;
                    ctx.beginPath();
                    ctx.rect(x, y, width, 80);
                    ctx.fillStyle = block.allocated ? "#f58e8e" : "#8ef58e";
                    ctx.fill();
                    ctx.stroke();

                    ctx.fillStyle = "#000";
                    ctx.font = "12px Arial";
                    ctx.fillText(
                        block.allocated
                            ? `P${block.process_id} (${block.size})`
                            : `Free (${block.size})`,
                        x + 5, y + 45
                    );
                    ctx.fillText(`${block.start}`, x, y + 100);
                    ctx.fillText(`${block.end}`, x + width - 30, y + 100);

                    x += width + 10;
                }

                ctx.fillStyle = "#000";
                ctx.fillText(`Memory End (${blocks[blocks.length-1].end})`, x - 20, 130);
            }

            // Initialize
            window.onload = async function() {
                let res = await fetch('/status');
                let data = await res.json();
                drawMemory(data.memory);
            };
        </script>
    </body>
    </html>
    """)

@app.route('/allocate')
def allocate():
    pid = request.args.get('pid')
    size = request.args.get('size', type=int)
    if pid and size:
        msg = memory.allocate(pid, size)
    else:
        msg = "Provide process ID and size."
    return jsonify({"message": msg, "memory": memory.to_list()})

@app.route('/deallocate')
def deallocate():
    pid = request.args.get('pid')
    if pid:
        msg = memory.deallocate(pid)
    else:
        msg = "Provide process ID to deallocate."
    return jsonify({"message": msg, "memory": memory.to_list()})

@app.route('/status')
def status():
    return jsonify({"memory": memory.to_list()})

# ------------------------------
# Run Server
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
