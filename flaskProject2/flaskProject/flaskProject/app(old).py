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



if __name__ == '__main__':
    app.run()

