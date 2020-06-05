import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    'background': '#000099',
    'text': '#FFFFFF'
}
df = pd.read_csv('users.csv', encoding='unicode_escape')
df['gender'].replace(0, 'Female',inplace=True)
df['gender'].replace(1, 'Male',inplace=True)
site_lat = df.latitude
site_lon = df.longitude
locations_name = df.districts

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(3, 252, 186)',
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    ))


fig.update_layout(
    title={'text':'DISTRICTS WITH DEXCONNECTED INDIVIDUALS',
                        'y':0.9,
                        'x':0.5,
                        'xanchor':'center',
                        'yanchor':'top'},
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken="pk.eyJ1IjoieWFzaGkyNyIsImEiOiJja2IwbzI3bDAwOXhyMnhueTIyYngwaG10In0.-QYnPiWR4dYGc9wYNWsflA",
        bearing=0,
        center=dict(
            lat=20.59,
            lon=78.96
        ),
        pitch=0,
        zoom=5,
        style='dark'
    ),
)
fi = px.histogram(df, x="age",labels={'age':'AGE','count':'COUNT'})
fi.update_traces(marker_color='rgb(153,0,153)',
                  marker_line_width=1.5, opacity=0.6)
fi.update_layout(title={'text':'AGE OF DEXCONNECTED INDIVIDUALS',
                        'y':0.9,
                        'x':0.5,
                        'xanchor':'center',
                        'yanchor':'top'})

# fi.update_yaxes(automargin=True)

d = pd.DataFrame(data={'dexConnected':df.groupby(['demographic']).count()['id']}) 

inst= pd.DataFrame(data={'dexConnected':df.groupby(['institute']).count()['id']}) 

#fig = px.bar(d, x='index', y='dexConnected',color='lifeExp')
f = go.Figure([go.Bar(x=d.index, y=d.dexConnected,marker_color="green")])
#fig.update_traces(overwrite=True, marker={"opacity": 0.4})
# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }
e = pd.DataFrame(data={'dexConnected':df.groupby(['gender']).count()['id']}) 

g = go.Figure([go.Bar(x=e.index, y=e.dexConnected)])
g.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

t = go.Figure(data=[go.Table(
    header=dict(values=["ID", "NAME", "GENDER", "AGE", "DEMOGRAPHIC", "DISTRICTS", "INSTITUTES"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[ df.id, df.name, df.gender, df.age, df.demographic, df.districts, df.institute],
               fill_color='lavender',
               align='left'))
])

inst_t=go.Figure(data=[go.Table(
    header=dict(values=["INSTITUTES","DEXCONNECTED"],
   fill_color='paleturquoise',
    align='left'),
    cells=dict(values=[inst.index, inst.dexConnected],
    fill_color='lavender',
    align='left')
)])

f.update_layout(title={'text':'DEMOGRAPHICS',
                        'y':0.9,
                        'x':0.5,
                        'xanchor':'center',
                        'yanchor':'top'})
f.update_traces(marker_color='rgb(102,204,0)', marker_line_color='rgb(0,102,0)',
                  marker_line_width=1.5, opacity=0.6)
t.update_layout(width=1000, height=800,title={'text':'DEXCONNECTED INDIVIDUALS DATA',
                        'y':0.9,
                        'x':0.5,
                        'xanchor':'center',
                        'yanchor':'top'})
g.update_layout(width=400, height=500,title={'text':'GENDER',
                        'y':0.9,
                        'x':0.5,
                        'xanchor':'center',
                        'yanchor':'top'})
inst_t.update_layout(width=400)
app.layout = html.Div(children=[
    html.H1(
        children='Dexterity Global',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': colors['background'],
            'margin':0
        }
    ),
    html.Div(children='A 21st century leadership movement powering the next generation of leaders for India and the world.', style={
        'textAlign': 'center',
         'color': colors['text'],
         'backgroundColor': colors['background'],
         'margin':0
    }),
    
    html.Div(
        [
            dbc.Row([
                # map
                dbc.Col(
                    html.Div(
                        dcc.Graph(figure=fig)
                    )
                )
            ]),
            dbc.Row([
                
                 dbc.Col(
                     
                    html.Div(
                        dcc.Graph(figure=fi)
                        
                    )
                 ),

                dbc.Col(
                    html.Div(
                        dcc.Graph(figure=f)
                       
                    )
                )
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(figure=t)
                    ),
                    width=8
                ),
              dbc.Col(
                [    dbc.Row(
                        dcc.Graph(figure=g)                    
                    ),
                    dbc.Row(
                        dcc.Graph(figure=inst_t)   
                    )]
              )  
            ])
        ]
    )
    #html.H4(children='USERS DATA'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
