import numpy as np
import pandas as pd 
import plotly.graph_objects as go
from datetime import datetime


def make_dataframe(data):
	df = pd.DataFrame(data)
	df['date'] = pd.to_datetime(df['date'], format="%d.%m.%Y")
	return df

def group_data(data, start, stop, date_window):

	df = data[start <= data['date']].copy()

	
	df = df[df['date'] <= stop]
	
	
	df['date'] = df['date'].apply(lambda x: (x - start).total_seconds())


	df['date'] = df['date'] // (date_window *  24 * 3600)
	
	date_range = pd.date_range(start=start, end=stop, freq=str(date_window) + 'D')
	date_range_dict = {i: datetime.strftime(x, format="%d.%m.%Y") for i, x in enumerate(date_range)}

	df['date'] = df['date'].replace(date_range_dict)
	
	result = df[['date', 'category', 'amount']].groupby(['date', 'category']).sum()
	return result


def plot_heatmap(data, start, stop, date_window): 

	df = make_dataframe(data)

	start = pd.to_datetime(start, format="%d.%m.%Y")
	stop = pd.to_datetime(stop, format="%d.%m.%Y")
	date_window = float(date_window)
	
	grouped_data = group_data(df, start, stop, date_window)

	table = pd.pivot_table(grouped_data, index='category', columns='date', values='amount', aggfunc=np.sum)

	fig = go.Figure(
	    data=go.Heatmap(
		z=table,  # данные
		x=table.columns,  # имена столбцов 
		y=table.index,  # имена строк
		colorscale='Viridis'  # цветовая схема
	    )
	)

	fig.update_layout(
	    title='Расходы по периодам',
	    xaxis_nticks=len(table.index)
	)

	fig.write_html("templates/analysis.html")
	
	return 0
