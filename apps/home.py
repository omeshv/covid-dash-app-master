import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
# external_stylesheets = [dbc.themes.LUX]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from sqlalchemy import create_engine
# pip install mysql-connector-python-rf
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="report_defn"
)

mycursor = mydb.cursor()

db_user = 'root'
db_pwd = 'root'
db_server = '127.0.0.1'
db_name = 'report_defn'
db_port = '3306'


def mysql_engine(user=db_user, password=db_pwd, host=db_server, port=db_port, database=db_name):
    connStr = "mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4".format(user, password, host, port, database)
    #
    # connStr = connStr+", connect_args={'connect_timeout': 600}"
    # print(connStr)
    engine = create_engine(connStr)
    return engine

df_section_list = pd.read_sql("""
            select * from report_sections_dim where is_active=1 order by section_seq;
            """, con=mysql_engine())  # return your first five rows


report_sections = []
for i in range(len(df_section_list)):
    report_list_buttons = []
    sqlString = 'select * from report_dim where is_active=1 and section_id='+str(df_section_list.loc[i,'id']) +' order by section_id,report_seq;'
    #print(sqlString);
    df_report_list = pd.read_sql(sqlString, con=mysql_engine())
    df_report_list.head(3)
    for j in range(len(df_report_list)):
        report_list_buttons.append(dbc.Col(dbc.Button(df_report_list.loc[j, 'report_name'],
                                                            href=df_report_list.loc[j, 'report_page_key'],
                                                            color="info",
                                                            className="mt-3",
                                                            target="_blank",
                                                            block=True,
                                                            style={'width': '300px','font-size': '80%','height': '35px',}
                                                      )
                                         )
                                   )
    report_sections.append(dbc.Col(
                            dbc.Card(children=[html.Img(src=df_section_list.loc[i, 'section_image'], height="150px"),
                                        html.H4(children=df_section_list.loc[i, 'section_name'],
                                        className="text-center"),
                                        dbc.Row(report_list_buttons),
                                        html.H6(children=df_section_list.loc[i, 'section_description']),
                                        ],
                                    body=True, color="info", outline=True
                                    )
                              , width=4, className="mb-4",
                              style={"height": "600"},
                        )
                )

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to DGS One Dashboard", className="text-center"), className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This app is just for POC for DGS One Dashboard with Python! ')
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(
                html.H5(children='For the PoC, there are two reports being tested. The reports will be further defined '
                                 'through database, where the graph type and layout will be defined and data will be '
                                 'taken in from the database.')
                , className="mb-5")
        ]),
        dbc.Row(report_sections,
                className="mb-5"),

        html.A("Copyright Ericsson.",
               href="http://www.ericsson.com")

    ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
