from flask import Flask, render_template, url_for, request
import pandas as pd
from scrape import Scrape


app = Flask(__name__)

scraper = Scrape()


@app.route('/')
def index():
    return render_template('index.html', show_form = True)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == "POST":
        success, msg = scraper.createData()
        if success:
            imdbTop = pd.read_excel('data/IMDB Top Rated Movies.xlsx')
            return render_template('index.html', headings= list(imdbTop.columns), data=imdbTop.values.tolist(), show_form = False)
        else:
            return str(msg)
    else:
        return render_template('index.html', show_form = True)


if __name__ == "__main__":
    app.run(debug=True)
