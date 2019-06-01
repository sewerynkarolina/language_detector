import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from io import BytesIO
import prepare_data as prepare_data
import base64
import webbrowser
import io
import json
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
import pandas as pd
from lime.lime_text import LimeTextExplainer
from sklearn.pipeline import make_pipeline
import dash_dangerously_set_inner_html
import joblib

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
            "//fonts.googleapis.com/css?family=Raleway:400,300,600",
            "//fonts.googleapis.com/css?family=Dosis:Medium",
            "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]

app = dash.Dash(__name__)

lasso = joblib.load("model123.joblib")
cv = joblib.load("vectorizer_123gram.h5")

countries = [ 'China', 'France', 'Germany', 'Italy', 'Japan', 'Poland', 'Russia',
   'Spain', 'Turkey', 'UK',  'Vietnam', 'USA']
pp = make_pipeline(cv, lasso)
explainer = LimeTextExplainer(class_names=countries)#, bow=False)


with open("model123columns.json", "r") as f:
    column_names = json.load(f)

def layout_app(app):
    app.layout = html.Div([


                    html.H1('Language detector'),

                    html.Div('''
                        by: K. Banecki, K. Lorenc, J. Piega, M.Seliga, K.Seweryn
                    '''),

                    html.Div(dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            html.Button('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        multiple=False
                    )),
                    html.Div(id='display-selected-values'),
                    html.Div(id="explain-frame"),
                    html.Div(id='output-data-upload',  style={"height": "600px", "overflow-y": "scroll"}),



    ])
    for css in external_css:
        app.css.append_css({"external_url": css})

    return (app)


app = layout_app(app)


@app.callback(
Output('output-data-upload', 'children'),
[Input('upload-data', 'contents')])
def update(contents):
    if contents is not None:
        return prepare_data.convert_dash_content_to_txt(contents)

@app.callback(
Output('explain-frame', 'children'),
[Input('output-data-upload', 'children')])
def make_prediction(contents):
    if contents is None:
        return None
    pages = contents[1]
    X = prepare_data.prepare_to_model(contents[0], column_names, pages)
    #print(pp.predict_proba)
    exp = explainer.explain_instance(X, pp.predict_proba, num_features=10, top_labels=1)
    exp.save_to_file("explain.html")
    url = "explain.html"
    webbrowser.open(url,new=1)
    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(exp.as_html())


if __name__ == '__main__':
    app.run_server(debug=False)
