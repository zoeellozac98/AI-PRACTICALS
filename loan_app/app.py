from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Create the bank operation graph
bank = {
    "Bank": ["Account", "Apply Loan"],
    "Account": ["Savings Account", "Current Account"],
    "Apply Loan": ["Home Loan", "Car Loan"],
    "Savings Account": [],
    "Current Account": [],
    "Home Loan": [],
    "Car Loan": []
}


# Perform Depth First Search
def dfs(graph, node, visited=None):

    if visited is None:
        visited = []

    visited.append(node)

    for next_node in graph[node]:
        if next_node not in visited:
            dfs(graph, next_node, visited)

    return visited

# Start DFS from Bank
dfs_result = dfs(bank, "Bank")

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>NovaBank | Smart Banking</title>

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }

            body {
                min-height: 100vh;
                background:
                    radial-gradient(circle at top right, #3b2a14, transparent 35%),
                    linear-gradient(135deg, #090909, #151515);
                color: white;
            }

            .container {
                width: 90%;
                max-width: 1150px;
                margin: auto;
            }

            /* Navigation */

            nav {
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid rgba(255,255,255,0.08);
            }

            .logo {
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 1px;
            }

            .logo span {
                color: #d6a84f;
            }

            .status {
                font-size: 13px;
                color: #b8b8b8;
            }

            .status::before {
                content: "●";
                color: #55d66b;
                margin-right: 7px;
            }

            /* Hero */

            .hero {
                padding: 70px 0 45px;
                display: grid;
                grid-template-columns: 1.3fr 1fr;
                gap: 50px;
                align-items: center;
            }

            .hero h1 {
                font-size: 55px;
                line-height: 1.05;
                margin-bottom: 20px;
            }

            .hero h1 span {
                color: #d6a84f;
            }

            .hero p {
                color: #a9a9a9;
                line-height: 1.7;
                max-width: 560px;
            }

            .badge {
                display: inline-block;
                padding: 8px 14px;
                border: 1px solid rgba(214,168,79,0.4);
                border-radius: 30px;
                color: #d6a84f;
                font-size: 12px;
                margin-bottom: 20px;
                letter-spacing: 1px;
            }

            /* Banking card */

            .bank-card {
                padding: 30px;
                border-radius: 24px;
                background: linear-gradient(145deg, #242424, #111111);
                border: 1px solid rgba(214,168,79,0.25);
                box-shadow: 0 25px 60px rgba(0,0,0,0.45);
                position: relative;
                overflow: hidden;
            }

            .bank-card::before {
                content: "";
                position: absolute;
                width: 180px;
                height: 180px;
                border-radius: 50%;
                background: rgba(214,168,79,0.12);
                right: -70px;
                top: -70px;
            }

            .card-title {
                color: #aaa;
                font-size: 13px;
                margin-bottom: 30px;
            }

            .balance {
                font-size: 34px;
                font-weight: bold;
                margin-bottom: 30px;
            }

            .card-bottom {
                display: flex;
                justify-content: space-between;
                color: #888;
                font-size: 12px;
            }

            /* Sections */

            .section-title {
                margin-bottom: 25px;
                font-size: 24px;
            }

            .operations {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                padding-bottom: 60px;
            }

            .operation {
                background: rgba(255,255,255,0.045);
                border: 1px solid rgba(255,255,255,0.08);
                padding: 28px;
                border-radius: 18px;
                transition: 0.25s;
            }

            .operation:hover {
                transform: translateY(-5px);
                border-color: rgba(214,168,79,0.5);
                background: rgba(214,168,79,0.06);
            }

            .icon {
                font-size: 28px;
                margin-bottom: 15px;
            }

            .operation h3 {
                margin-bottom: 8px;
            }

            .operation p {
                color: #999;
                font-size: 14px;
                line-height: 1.6;
                margin-bottom: 18px;
            }

            .options {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }

            button {
                border: none;
                padding: 11px 17px;
                border-radius: 9px;
                cursor: pointer;
                background: #d6a84f;
                color: #111;
                font-weight: bold;
                transition: 0.2s;
            }

            button:hover {
                transform: scale(1.04);
                background: #f0c66e;
            }

            .secondary {
                background: rgba(255,255,255,0.08);
                color: white;
            }

            footer {
                border-top: 1px solid rgba(255,255,255,0.08);
                padding: 25px 0;
                color: #666;
                font-size: 12px;
                text-align: center;
            }

            @media (max-width: 800px) {
                .hero {
                    grid-template-columns: 1fr;
                }

                .hero h1 {
                    font-size: 42px;
                }

                .operations {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>

    <body>

        <div class="container">

            <nav>
                <div class="logo">NOVA<span>BANK</span></div>
                <div class="status">System Online</div>
            </nav>

            <section class="hero">

                <div>
                    <div class="badge">SMART BANKING SYSTEM • DFS</div>

                    <h1>
                        Banking made<br>
                        <span>intelligent.</span>
                    </h1>

                    <p>
                        Explore banking services through an intelligent
                        department navigation system powered by
                        Depth First Search.
                    </p>
                </div>

                <div class="bank-card">

                    <div class="card-title">
                        NOVABANK DIGITAL ACCOUNT
                    </div>

                    <div class="balance">
                        Secure Banking
                    </div>

                    <div class="card-bottom">
                        <span>DFS ENABLED</span>
                        <span>AI LAB • 2026</span>
                    </div>

                </div>

            </section>

            <h2 class="section-title">Bank Operations</h2>

            <section class="operations">

                <div class="operation">

                    <div class="icon">🏦</div>

                    <h3>Account Services</h3>

                    <p>
                        Navigate through available account
                        services and choose the account type
                        you want to access.
                    </p>

                    <div class="options">
                        <button>Savings Account</button>
                        <button class="secondary">Current Account</button>
                    </div>

                </div>



                <div class="operation">

                    <div class="icon">💳</div>

                    <h3>Apply for a Loan</h3>

                    <p>
                        Explore available loan products and
                        begin your application through the
                        banking system.
                    </p>

                    <div class="options">
                        <button>Home Loan</button>
                        <button class="secondary">Car Loan</button>
                    </div>

                </div>

            </section>

            <section class="dfs-section">

    <h2>DFS Analysis</h2>

    <p>
        Traverse the banking operation graph using
        Depth First Search.
    </p>

    <a href="/dfs">
        <button>Run DFS</button>
    </a>

</section> 

        </div>

        <footer>
            NovaBank Smart Banking System • Depth First Search Practical
        </footer>

    </body>
    </html>
    """

@app.get("/dfs", response_class=HTMLResponse)
def show_dfs():

    result = " → ".join(dfs_result)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NovaBank DFS Result</title>

        <style>
            body {{
                background: #111;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 80px 20px;
            }}

            h1 {{
                color: #d6a84f;
                margin-bottom: 30px;
            }}

            .result {{
                max-width: 900px;
                margin: auto;
                padding: 25px;
                border: 1px solid #d6a84f;
                border-radius: 15px;
                font-size: 20px;
            }}
        </style>
    </head>

    <body>

        <h1>DFS Bank Operation</h1>

        <div class="result">
            {result}
        </div>

    </body>
    </html>
    """