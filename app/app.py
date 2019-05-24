import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from io import BytesIO
import prepare_data as prepare_data
import base64
import io

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
        'https://github.com/plotly/dash-salesforce-crm/blob/master/static/s8.css',
        'https://github.com/plotly/dash-salesforce-crm/blob/master/static/s4.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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

    html.Div(id='output-data-upload')
])




@app.callback(
Output('output-data-upload', 'children'),
[Input('upload-data', 'contents')])
def update(contents):
    pass
    if contents is not None:
        return prepare_data.convert_dash_content_to_txt(contents)
    


if __name__ == '__main__':
    app.run_server(debug=True)
