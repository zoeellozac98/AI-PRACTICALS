from flask import Flask, render_template

app = Flask(__name__)

# Water tank states represented as a graph
water_tank = {
    "Tank": ["Normal", "Warning", "Overflow"],
    "Normal": ["25%", "50%"],
    "Warning": ["75%"],
    "Overflow": ["100%"],
    "25%": [],
    "50%": [],
    "75%": [],
    "100%": []
}


# Depth-Limited Search
def dls(graph, current, target, depth, path=None):

    if path is None:
        path = []

    path.append(current)

    # Target found
    if current == target:
        return path

    # Depth limit reached
    if depth == 0:
        path.pop()
        return None

    for next_node in graph[current]:

        if next_node not in path:

            result = dls(
                graph,
                next_node,
                target,
                depth - 1,
                path
            )

            if result is not None:
                return result

    path.pop()
    return None


@app.route("/")
def home():

    # Search for overflow using DLS
    result = dls(
        water_tank,
        "Tank",
        "100%",
        3
    )

    if result:
        alert = "OVERFLOW ALERT!"
        status = "Danger"
        path = " → ".join(result)
    else:
        alert = "Water Level Normal"
        status = "Safe"
        path = "Overflow not detected within depth limit."

    return render_template(
        "index.html",
        alert=alert,
        status=status,
        path=path
    )


if __name__ == "__main__":
    app.run(debug=True)