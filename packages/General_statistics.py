import pandas as pd
import plotly.express as px
import json, datetime
import plotly.graph_objects as go

class generalStatistics:
    def __init__(self):
        init = 0 
    
    def piePlatform (data):
        plaform_U = list(set(data))
        size = [data.count(i) for  i in plaform_U]
        pull = []
        for i in size:
            if float(i/sum(size)) > 0.01:
                pull.append(0)
            else:
                pull.append(0.2)
        for i in range(len(plaform_U)):
            if plaform_U[i] == '-1':
                plaform_U[i] = 'None'
        fig = go.Figure(data=[go.Pie(labels=plaform_U, values=size, pull=pull)])
        fig.update_layout(
            autosize=False,
            width=620,
            height=500,
            legend_title_text='Instrument Platform',
            legend=dict(font=dict(size=16), x=1, y=1, orientation='v')
            )
        return fig
    
    def create_earliest_row( df, cols, result_type):
        # Identify earliest date and set to 0
        earliest = df['first_created'].iloc[0] + '-01'
        earliest = datetime.datetime.strptime(earliest, '%Y-%m-%d')
        lastMonth = earliest - datetime.timedelta(days=1)
        lastMonth = str(lastMonth.date())[:-3]

        # Create a new row of data and add to the first row of the data frame
        row = pd.DataFrame([[lastMonth, 0, 0, result_type]], columns=cols)
        updated_df = pd.concat([row, df]).reset_index(drop=True)
        return updated_df
    
    def submission_count(date_read_run , date_analysis):
        date_read_run = list(date_read_run.str[:-3])
        date_analysis = list(date_analysis.str[:-3])
        date= sorted(list(set(date_read_run + date_analysis)) , reverse=False)
        date = [i for i in date if len(i) == 7]
        start = date[0]
        end = date[len(date)-1]
        all_dates = pd.date_range(start=start, end=end, freq='M').strftime('%Y-%m').tolist()
        new_data = {'dates':[],'read_run_count':[],'read_run_cum':[],'analysis_count':[],'analysis_cum':[]}
        new_data['dates'] = all_dates
        for i in range(len(all_dates)):
            new_data['read_run_count'].append(date_read_run.count(all_dates[i]))
            new_data['analysis_count'].append(date_analysis.count(all_dates[i]))
            if i == 0:
                new_data['read_run_cum'].append(date_read_run.count(all_dates[i]))
                new_data['analysis_cum'].append(date_analysis.count(all_dates[i]))
            else:
                new_data['read_run_cum'].append(new_data['read_run_cum'][i-1]+date_read_run.count(all_dates[i]))
                new_data['analysis_cum'].append(new_data['analysis_cum'][i-1]+date_analysis.count(all_dates[i]))
        return pd.DataFrame(new_data)


    def generate_figures(dataframe,username):
        # Figure 1: read_run_count and analysis_count 
        fig1 = px.line(dataframe, x='dates', y=['read_run_count', 'analysis_count'],markers=True)
        fig1.update_layout(title={'text':'Raw Number of Submissions per Month for {}'.format(username),'x': 0.5,'xanchor': 'center' }, xaxis_title='Month-Year', yaxis_title='No. of submissions', legend_title_text='Type of data',  xaxis_range=[0, None], yaxis_range=[0, None])
        fig1.data[0].marker.symbol = 'circle'
        fig1.data[1].marker.symbol = 'diamond'
        
        # Figure 2: read_run_cum and analysis_cum
        fig2 = px.line(dataframe, x='dates', y=['read_run_cum', 'analysis_cum'],markers=True)
        fig2.update_layout(title={'text':'Cumulative Number of Submissions per Month for {}'.format(username),'x': 0.5,'xanchor': 'center' }, xaxis_title='Month-Year', yaxis_title='No. of Cumulative Submissions',legend_title_text='Type of data', xaxis_range=[0, None], yaxis_range=[0, None])
        fig2.data[0].marker.symbol = 'circle'
        fig2.data[1].marker.symbol = 'diamond'
    
        return fig1, fig2

    def submissionsEvo(data_read_run, data_analysis, username):
        data = generalStatistics.submission_count (data_read_run['first_created'], data_analysis['first_created'] )
        fig1, fig2 = generalStatistics.generate_figures(data,username)
        return fig1 , fig2

