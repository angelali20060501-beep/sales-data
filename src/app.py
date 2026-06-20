import pandas as pd
from flask import Flask, Response, render_template, request, jsonify


app = Flask(__name__, static_folder='static')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Bar-Graph-Page.html')
def bar_graph_page():
    return render_template('Bar-Graph-Page.html')

@app.route('/Line-Graph-Page.html')
def line_graph_page():
    return render_template('Line-Graph-Page.html')

@app.route('/plotBar', methods=['GET'])
def plotBar():
    game = request.args.get('game')
    data = pd.read_csv("vgsales.csv").dropna()
    if game:
        game_name = game.split(" (")[0]
        game_data = data[data["Name"] == game_name]
        row = game_data.iloc[0]
        return jsonify({
            "x": ["NA", "EU", "JP", "Other"],
            "y_na": float(row["NA_Sales"]),
            "y_eu": float(row["EU_Sales"]),
            "y_jp": float(row["JP_Sales"]),
            "y_other": float(row["Other_Sales"])
        })


@app.route('/BarCompanies', methods=['GET'])
def BarCompanies():
    data = pd.read_csv("vgsales.csv")
    data = data.dropna().sort_values(by=["Publisher"])
    publishers = data["Publisher"].unique().tolist()
    return jsonify(publishers)

@app.route('/BarGames', methods=['GET'])
def BarGames():
    publisher = request.args.get('publisher')
    if not publisher:
        return jsonify({"error": "No publisher provided"}), 400
    data = pd.read_csv("vgsales.csv")
    data = data.dropna().sort_values(by=["Name"])
    data["Games_By_Platform"] = data["Name"] + " (" + data["Platform"] + ")"
    games = data[data["Publisher"] == publisher]["Games_By_Platform"].tolist()
    return jsonify(games)


@app.route('/BarYear', methods=["GET"])
def BarYear():
    data = pd.read_csv("vgsales.csv").dropna()
    years = data["Year"].sort_values().unique().tolist()
    return jsonify(years)


@app.route('/plotYear', methods=['GET'])
def plotYear():
    year = request.args.get('year')
    data = pd.read_csv("vgsales.csv").dropna()
    if year:
        year = float(year)
        year_data = data[data["Year"] == year]
        total = year_data[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum()
        return jsonify({
            "x": ["NA", "EU", "JP", "Other"],
            "y_na": float(total["NA_Sales"]),
            "y_eu": float(total["EU_Sales"]),
            "y_jp": float(total["JP_Sales"]),
            "y_other": float(total["Other_Sales"])
        })


@app.route('/LineCompanies', methods=['GET'])
def LineCompanies():
    data = pd.read_csv("vgsales.csv")
    data = data.dropna().sort_values(by=["Publisher"])
    publishers = data["Publisher"].unique().tolist()
    return jsonify(publishers)

@app.route('/plotHistory', methods=['GET'])
def plotHistory():
    company = request.args.get('company')
    data = pd.read_csv("vgsales.csv")
    company_data = data[data["Publisher"] == company]
    sales_by_year = company_data.groupby("Year")["Global_Sales"].sum().reset_index()
    return jsonify({
        "x": sales_by_year["Year"].tolist(),
        "y": sales_by_year["Global_Sales"].tolist()
    })

@app.route('/BarHighest', methods=["GET"])
def BarHighest():
    data = pd.read_csv("vgsales.csv").dropna()
    years = data["Year"].sort_values().unique().tolist()
    return jsonify(years)

@app.route('/BarPlotHighest', methods=['GET'])
def BarPlotHighest():
    year = float(request.args.get('year'))
    data = pd.read_csv("vgsales.csv").dropna()
    year_data = data[data["Year"] == year]
    games = year_data["Name"].head(7).tolist()
    sales = year_data["Global_Sales"].tolist()
    return jsonify({"games": games, "sales": sales})

if __name__ == '__main__':
    app.run(debug=True)
