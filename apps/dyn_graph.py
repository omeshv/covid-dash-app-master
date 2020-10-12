import configparser as Cp
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from . import baselib as lib
from app import app

# needed if running single page dash app instead
# external_stylesheets = [dbc.themes.LUX]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
import os
# "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
config = Cp.ConfigParser()
config.read('C:/LocalData/DS/Activity/dynGraph/covid-dash-app-master/assets/config.txt')
print('Sections are ->',config.sections())
try:
    showLegend = config['DEFAULT']['ShowLegend']
except:
    showLegend = True
try:
    Template =  config['DEFAULT']['Template']
except:
    Template = 'simple_white'

pio.templates.default = Template


showLegend = True if showLegend=='True' else False

print('showLegend', showLegend)


def convertListToDict(lst, df):
    res_dct = {}
    for i in range(0, len(lst)):
        subReportsCount = len(df[df['Category'] == lst[i]]['KPI Name'].unique())
        res_dct[lst[i]] = subReportsCount
    return res_dct


def getReportList(category_name, access_name, df):
    # print('Called GetReportList with Access ',access_name, ' and Category ',category_name)
    reqReports = df[(df['Access'].str.contains(access_name)) & (df['Category'] == category_name)]
    # print("xxxx",reqReports.head(2))
    return reqReports['KPI Name'].unique()


global_df = pd.read_excel('sample_input.xlsx', sheet_name='graphs')
# df = pd.read_excel("C:/LocalData/DS/Activity/MMEA_Dashboard/sample_input.xlsx", sheet_name='graphs')
reportList = convertListToDict(global_df['Category'].unique(), global_df)
print(reportList)
accessList = global_df['Access'].unique()
myArr = []
newArr = []
for recs in range(len(accessList)):
    if "," in accessList[recs]:
        newArr = accessList[recs].split(",")
        valExists = 0
        for j in range(len(newArr)):
            valExists = 1 if newArr[j].strip() in myArr else 0
            if valExists == 0:
                myArr.append(newArr[j].strip())
    else:
        if accessList[recs] in myArr:
            valExists = 1
        #        elif not myArr:
        #            myArr[0] = accessList[recs]
        else:
            myArr.append(accessList[recs].strip())

myAccessList = {}
for i in range(0, len(myArr)):
    myAccessList[myArr[i].strip()] = myArr[i].strip()

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3(children='Dynamic Graph Tool'), className="mb-2", width=4),
            dbc.Col(html.Div(id='intermediate-value', style={'display': 'none'})),
            # ], justify='center'),
            # dbc.Col(html.Plaintext(children='(c) Ericsson'), className="mb-4"),
            dbc.Col(dcc.Dropdown(
                id='reportAccess',
                options=[{'label': i, 'value': i} for i in myAccessList.keys()],
                value=list(myAccessList.keys())[0],
                # multi=True,
                style={'width': '100%'}
            ),
            ),
            dbc.Col(dcc.Dropdown(
                id='reportCategory',
                options=[{'label': i, 'value': i} for i in global_df['Category'].unique()],
                value=list(reportList.keys())[0],
                # multi=True,
                style={'width': '100%'}
            ),
            ),
            dbc.Col(html.Button('Refresh Data', id='refreshData', n_clicks=0, style={'Background-color': '#4CAF50'})),
        ]),

        # choose between cases or deaths
        dbc.Row([
            dbc.Col(html.H3(children=''), className="mb-4")
        ])
    ]),
    dbc.Row([html.H6(children=''), ]),
    dcc.Graph(id='reportGraphArea'),
])


# page callbacks
# output, if multiple, to be added in array[]
@app.callback(Output('intermediate-value', 'value'),
              [Input('refreshData', 'n_clicks')],
              )
def update_data(n_clicks):
    df = pd.read_excel('sample_input.xlsx', sheet_name='graphs')
    return df.to_json(date_format='iso', orient='split')


@app.callback(Output('reportGraphArea', 'figure'),
              [Input('reportAccess', 'value')],
              [Input('reportCategory', 'value')],
              [Input('intermediate-value', 'value')]
              )
# {:,.2f} thousand with decimal
# {:,} thousand

def update_graph(reportAccess, reportCategory, jsonified_cleaned_data):
    df = pd.read_json(jsonified_cleaned_data, orient='split')
    donut_colors = ['rgb(79, 129, 102)', 'rgb(151, 179, 100)', 'rgb(175, 49, 35)', 'rgb(36, 73, 147)',
                    'rgb(146, 123, 21)', 'rgb(177, 180, 34)',
                    'rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                    'rgb(36, 55, 57)', 'rgb(6, 4, 4)', 'rgb(177, 127, 38)', 'rgb(205, 152, 36)',
                    'rgb(99, 79, 37)', 'rgb(129, 180, 179)', 'rgb(124, 103, 37)', 'rgb(33, 75, 99)',
                    'rgb(206, 206, 40)', 'rgb(175, 51, 21)', 'rgb(35, 36, 21)']

    reportList = getReportList(reportCategory, reportAccess, df)
    # print(df.head(5))
    # print('Report Category-> ', reportCategory, ' Access type->', reportAccess)
    # print('Report List is ', reportList)
    reportCount = len(reportList)

    maxRows, maxCols, specDef = lib.getSpecDef(reportCount)
    print(specDef)
    # print("Reports -", reportCount)
    graphType = ''
    for i in range(1, reportCount + 1):
        kpiName = reportList[i - 1]
        try:
            graphType = df[(df['Access'].str.contains(reportAccess)) &
                           (df['Category'] == reportCategory) &
                           (df['KPI Name'] == kpiName) &
                           (df['Graph Type'].str.contains('Dual'))]['Graph Type'].iloc[0]
        except:
            graphType = df[(df['Access'].str.contains(reportAccess)) &
                           (df['Category'] == reportCategory) &
                           (df['KPI Name'] == kpiName)]['Graph Type'].iloc[0]

        domainType, secAxis = lib.getGraphDomain_Axis(graphType)
        # print("KPI Name->", kpiName, "I->", i, " Domain Type ", domainType)
        # Enhance specDef.. L oop through the items in specDef, update the dict item for
        # the iTH position
        itemCounter = 0
        noneCount = 0
        #print('Length->', len(specDef))
        for arRow in range(len(specDef)):
            for arCol in range(len(specDef[arRow])):
                itemCounter = itemCounter + 1
                if specDef[arRow][arCol] is None:
                    noneCount = noneCount + 1
                    #print('NONE ItemCounter->', itemCounter, ' arRow->', arRow, ' arCol->', arCol, " i->", i)
                    itemCounter = itemCounter - 1
                else:
                    #print('ItemCounter->', itemCounter, ' arRow->', arRow, ' arCol->', arCol, " i->", i)
                    if itemCounter - 1 == (i - 1):
                        #print('Here itemCounter', itemCounter, " i ->", i)
                        specDef[arRow][arCol]['type'] = domainType
                        specDef[arRow][arCol]['secondary_y'] = secAxis
                        break

    # print(specDef)

    fig = make_subplots(rows=maxRows, cols=maxCols,
                        subplot_titles=reportList,
                        vertical_spacing=0.25, horizontal_spacing=0.06,
                        specs=specDef,
                        )

    annotArray = [None] * (reportCount)
    pd.options.display.float_format = '{:, .1f}'.format
    for i in range(1, reportCount + 1):
        kpiName = reportList[i - 1]
        # kpiName = df[(df['Category'] == reportCategory) & (df['Sequence'] == i)]['KPI Name'].unique()[0]
        df['TextFormat'] = df['TextFormat'].fillna('')
        for index, row in df[(df['Category'] == reportCategory) &
                             (df['KPI Name'] == kpiName) &
                             (df['Access'].str.contains(reportAccess))].sort_values(by=['Sequence']).iterrows():

            selColor = row['Color']
            graphType = row['Graph Type']
            rowName = row['Indicator']
            df_sub = df[(df['Category'] == reportCategory) &
                        (df['Access'].str.contains(reportAccess)) &
                        # (df['Sequence'] == i) &
                        (df['KPI Name'] == kpiName) & (
                                df['Indicator'] == rowName)]

            df_subT = df_sub.drop(
                ['MA', 'Access', 'TextFormat', 'CU', 'Category', 'Sequence', 'KPI Name', 'Graph Type', 'SubType',
                 'Color',
                 'Indicator'],
                axis=1).T.reset_index()
            df_subT.rename(columns={df_subT.columns[0]: "Date",
                                    df_subT.columns[1]: "Value"
                                    },
                           inplace=True
                           )
            #            df_subT['Value'] = df_subT['Value']  # .map(lib.formatNumbers)
            # For conditional formatting
            if "," in selColor:
                selColor = lib.barColorWithCondition(df_subT, selColor)

            rowPos, colPos = lib.getRowAndColPos(i, reportCount)
            # print('TextFormat is ->', row['TextFormat'])
            textFormat = str(row['TextFormat'])

            if row['TextFormat'] == '' or row['TextFormat'] is None:
                textFormat = '%{text:.4s}'
            elif 'text' in textFormat:
                textFormat = row['TextFormat']
            else:
                textFormat = ''
                df_subT = lib.getTextFormat(row['TextFormat'], df_subT)

            if graphType == 'Line':
                fig.add_trace(
                    go.Scatter(y=df_subT['Value'],
                               x=df_subT['Date'],
                               marker_color=selColor,
                               name=rowName,
                               hovertemplate='%{y:.1f}',
                               ),
                    row=rowPos,
                    col=colPos
                )
            elif graphType == 'Bar':
                fig.add_trace(
                    go.Bar(y=df_subT['Value'],
                           x=df_subT['Date'],
                           marker_color=selColor,
                           name=rowName,
                           text=df_subT['Value'],
                           textposition='auto',  # inside/outside/auto
                           texttemplate=textFormat,
                           textangle=90,
                           hovertemplate='%{y:.1f}',
                           ),
                    row=rowPos,
                    col=colPos,
                    secondary_y=False
                ),
                # fig.add_trace(
                #     go.Bar(x=df_subT['Date'], y=[0], showlegend=False, hoverinfo='none'),
                #     row=rowPos,
                #     col=colPos,
                #     secondary_y=True
                # ),
            elif graphType == 'BarDual':
                fig.add_trace(
                    go.Bar(x=df_subT['Date'], y=[0], yaxis='y2', showlegend=showLegend, hoverinfo='none'),
                    row=rowPos,
                    col=colPos,
                    secondary_y=True
                ),
                fig.add_trace(
                    go.Bar(y=df_subT['Value'],
                           x=df_subT['Date'],
                           marker_color=selColor,
                           name=rowName,
                           text=df_subT['Value'],
                           textposition='auto',  # inside/outside/auto
                           texttemplate='%{text:.3s}',
                           textangle=90,
                           hovertemplate='%{y:.1f}',
                           ),
                    row=rowPos,
                    col=colPos,
                    secondary_y=True
                )
            elif graphType == 'LineDual':
                fig.add_trace(
                    go.Scatter(y=df_subT['Value'],
                               x=df_subT['Date'],
                               marker_color=selColor,
                               name=rowName,
                               text=df_subT['Value'],
                               ),
                    row=rowPos,
                    col=colPos,
                    secondary_y=True
                )
            elif graphType == 'Pie':
                fig.add_trace(
                    go.Pie(
                        hoverinfo='label+percent',
                        values=df_subT['Value'],
                        # textposition='outside',
                        showlegend=False,
                        text=df_subT['Value'],
                        texttemplate=textFormat,
                        marker_colors=donut_colors,
                        # name=kpiName
                    ),
                    row=rowPos,
                    col=colPos
                )
            elif graphType == 'Donut':
                fig.add_trace(
                    go.Pie(
                        hoverinfo='label+percent',
                        hole=0.6,
                        values=df_subT['Value'],
                        text=df_subT['Value'],
                        texttemplate=textFormat,
                        textposition='auto',
                        showlegend=False,

                        marker_colors=donut_colors,
                        insidetextorientation='radial'
                        # name=kpiName
                    ),
                    row=rowPos,
                    col=colPos
                )
            # Ref: https://plotly.com/python/filled-area-plots/
            elif graphType == 'Area':
                fig.add_trace(
                    go.Scatter(y=df_subT['Value'],
                               x=df_subT['Date'],
                               line_color=selColor,
                               fill='tozeroy',  # if there are more than one element fill='tonexty'
                               name=rowName
                               ),
                    row=rowPos,
                    col=colPos,
                )
            # fig.update_layout(height=700, showlegend=False)
            if graphType == 'Pie' or graphType == 'Donut':
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor='rgba(0,0,0,0)',
                                  # annotations=[dict(text=kpiName, x=0.18, y=0.5, font_size=14, showarrow=False)],
                                  showlegend=showLegend,
                                  font=dict(size=12, color='black'),
                                  uniformtext_minsize=7,
                                  uniformtext_mode='hide',
                                  )
            elif graphType == 'BarDual' or graphType == 'LineDual':
                fig.update_layout(barmode='group',
                                  bargap=0.15,  # gap between bars of adjacent location coordinates.
                                  bargroupgap=0.1,
                                  )
            if reportCount > i:
                # print("Before Annot ", i)
                if graphType == 'Donut':
                    annotArray[i] = dict(text=kpiName, x=0.18, y=0.5, font_size=14, showarrow=False)
                else:
                    annotArray[i] = dict(text='', x=0.18, y=0.5, font_size=4, showarrow=False)
                # print("Annot Array i ", i, '->', annotArray[i])
    figHeight = 500 if maxRows <= 2 else 800
    fig.update_layout(height=figHeight,
                      # width = 1137,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      margin=go.layout.Margin(l=20, r=20, b=70, t=45, pad=2),
                      title_x=0.5,
                      xaxis_tickangle=-90,
                      xaxis_tickfont_size=8,
                      yaxis2=dict(side='right', overlaying='y', showline=True),
                      # yaxis=dict(side='left', overlaying='free', showline=True),
                      barmode='group',
                      # bargap=0.15,  # gap between bars of adjacent location coordinates.
                      title_text=reportCategory,
                      title=dict(text=reportCategory, font=dict(family='Arial', size=30, color='blue')),
                      showlegend=showLegend,
                      font=dict(size=12, color='black'),
                      annotations=[
                          go.layout.Annotation(
                              text='YTD: 2025',
                              align='right',
                              showarrow=False,
                              xref='paper',
                              yref='paper',
                              x=0.9,
                              y=1.0,
                              bordercolor='black',
                              borderwidth=1
                          )],
                      # annotations=annotArray,
                      xaxis=dict(
                          showgrid=False,
                          zeroline=True,
                          showline=True,
                          gridcolor='#bdbdbd',
                          gridwidth=2,
                          zerolinecolor='#969696',
                          zerolinewidth=2,
                          linecolor='#636363',
                          linewidth=2,
                          title='Period',
                          titlefont=dict(family='Arial, sans-serif', size=8, color='lightgrey'
                                         ),
                      )
                      )
    return fig

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
