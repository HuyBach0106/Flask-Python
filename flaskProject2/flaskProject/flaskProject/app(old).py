from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('SearchWithCSSData.html', search_text="")
@app.route('/searchData', methods=['POST'])
def searchData():
    search_text = request.form['searchInput']
    html_table = load_data(search_text)
    print(html_table)
    return render_template('SearchWithCSSData.html', search_text=search_text, table=html_table)

def load_data(search_text):
    import pandas as pd
    df = pd.read_csv('gradedata.csv')
    dfX = df
    if search_text != "":
        dfX = df[(df["fname"] == search_text) | (df["lname"] == search_text)]
        print(dfX)
    html_table = dfX.to_html(classes='data', escape=False)
    return html_table


@app.route("/")
def index() :
    return render_template("index.html")

@app.route("/loadAccount")
def loadAccount() :
    acc = "Felix"
    return render_template("account.html", account=acc)

@app.route("/loadPage01")
def loadPage01() :
    lst = [0, 1, 2, 3]
    return render_template("page_01_for.html", seq = lst)

@app.route("/loadPage02")
def loadPage02() :
    lst = [["alpha", "alpha.html"],
           ["omega", "omega.html"],
           ["gamma", "gamma.html"]]
    return render_template("Page_02_For Menu.html", seq = lst)


@app.route("/")
def loadPage03() :
    import pandas as pd
    data = {
        'Name':     ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 24, 35, 32],
        'City': ['New York', 'Paris', 'Berlin', 'London']
    }
    df = pd.DataFrame(data)
    html_data = df.to_html(classes='data', escape=False);
    return render_template('Page_03_Table.html', table=html_data)

@app.route("/")
def load_data() :
    import pandas as pd
    df = pd.read_csv('gradedata.csv')
    # Chỉ hiện 5 bản ghi
    html_table = df.iloc[:5].to_html(classes='data', escape=False)
    return html_table

@app.route("/loadPage04")
def Introduction() :
    html_table = load_data();
    return render_template('Page_04_Table.html', tables=html_table, titles=html_table.columns.values)

if __name__ == '__main__':
    app.run()

