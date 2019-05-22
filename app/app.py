import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from io import BytesIO
import prepare_data as prep_data
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

    html.H4('Enter a path to pdf file'),
    html.Div(dcc.Input(
        id='data_path',
        placeholder='Enter a path to pdf file',
        type='text',
        value=''
    )),

    html.Div(id='data_output'),

    html.Div(id='output-data-upload')
])


@app.callback(Output('data_output', 'children'),
              [Input('data_path', 'value')])
def update_output(data_path):
    return prep_data.convert_pdf_to_txt(data_path)


@app.callback(
Output('output-data-upload', 'children'),
[Input('upload-data', 'contents')])#,
#[State('upload-data', 'filename'),
#State('upload-data', 'last_modified')])
def update(content):
    pass
    # if content is not None:
    #     content_type, content_string = content.split(',')
    #     decoded = base64.b64decode(content_string)
    #     print(decoded)
    #     print(io.BytesIO(decoded))
        #d = prep_data.convert_pdf_to_txt(io.BytesIO(decoded))
        #children = [
    #        parse_contents(c, n, d) for c, n, d in
    #        zip(list_of_contents, list_of_names, list_of_dates)]
    #children
    # if content is not None:
    #     #print(content)
    #     print(type(content))
    #     print(type(str.encode(content)))
    #     print(prep_data.convert_pdf_to_txt(content))

    #pass
    #print(type(content))
    #print(type(str.encode(content)))
    # creating a pdf reader object
    #pdf = pdftotext.PDF((BytesIO(str.encode(content))))
    #el_of_list = ''
    #Ponieważ page in pdf  - to jest strona z artykułu to łącze stringi, pewnie to można lepiej
    #for page in pdf:
    #    el_of_list = el_of_list+page

if __name__ == '__main__':
    app.run_server(debug=True)
