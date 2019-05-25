import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from io import BytesIO
import prepare_data as prepare_data
import base64
import io
import json
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
import pandas as pd
from lime.lime_text import LimeTextExplainer
from sklearn.pipeline import make_pipeline
import dash_dangerously_set_inner_html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
#         'https://github.com/plotly/dash-salesforce-crm/blob/master/static/s8.css',
#         'https://github.com/plotly/dash-salesforce-crm/blob/master/static/s4.css']

app = dash.Dash(__name__)#, #external_stylesheets=external_stylesheets)

lasso = joblib.load("../logistic_simple_model.h5")
cv = joblib.load("vectorizer_1gram.h5")

pp = make_pipeline(cv, lasso)
explainer = LimeTextExplainer()


with open("../columns.json", "r") as f:
    column_names = json.load(f)

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
    html.Div(id="explain-frame"),
    html.Div(id='output-data-upload',  style={"height": "600px", "overflow-y": "scroll"}),
])




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
    exp = explainer.explain_instance(X, pp.predict_proba, num_features=6)
    exp.save_to_file("explain.html")
    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(exp.as_html())


if __name__ == '__main__':
    app.run_server(debug=True)
