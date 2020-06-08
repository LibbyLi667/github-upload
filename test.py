''' Create a simple genomics data stats dashboard.
Choose pages to show in the drop down widgets, and make selections

on the plots to update the summary and histograms accordingly.
.. note::
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve --show --port 5109 /Users/xli677/Dropbox (Uni of Auckland)/xli677/Projects/MyTardis/Visualisation_with_Bokeh/test.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/stocks
.. _README: https://github.com/bokeh/bokeh/blob/master/examples/app/stocks/README.md
'''
from functools import lru_cache
from os.path import dirname, join

from math import pi
import pandas as pd
import numpy as np

from bokeh.io import curdoc, output_file, show
from bokeh.layouts import layout, column, row, widgetbox
from bokeh.models import ColumnDataSource, PreText, Select, Dropdown, HoverTool, Label, LabelSet, LinearAxis, Text
from bokeh.plotting import figure, curdoc
from bokeh.transform import cumsum


def dict_extract_all(datatype_list, dic, item):  ### count the number of true/false and return a dictionary for all data types 
    list_return_all = []
    for i in datatype_list:
        i = join(i + '_' + item)
        list_return_all += dic[i]
        
    if item == 'Biopipeline': 
        dict_return_all = dict((x,list_return_all.count(x))for x in status_list)
    else:                                  
        dict_return_all = dict((x,list_return_all.count(x)) for x in [True,False])

    return dict_return_all

def dict_extract(datatype_name, dic, item):  ### given data type, dictionary, to count the number of true/false and return a dictionary containg the number for each data type 
    list_return = dic[datatype_name + '_' + item]   
    if item == 'Biopipeline': 
        dict_return = dict((x,list_return.count(x))for x in status_list)
    else:                                  
        dict_return= dict((x,list_return.count(x)) for x in [True,False])

    return dict_return

def angle(data):
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    return 


chart_colors = ['#007bff','#e29e44','#44e5e2','#eeeeee','#d8e244','#e244db']

def make_plot_all():
    data = dict_extract_all(data_types, dictA, ticker1.value)
    data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'status'})
    angle(data2)
    data2['color'] = chart_colors[:len(data)]
    column_sum = data2['value'].sum()
    data2['percentage'] = (data2['value']/column_sum)
    data2['label'] = ["{:.2%}".format(p) for p in data2['percentage']]
    data2['label'] = data2['label'].astype(str)
    data2['label'] = data2['label'].str.pad(20, side = "left")
    source = ColumnDataSource(data2)
    
    hover = HoverTool(tooltips="@status: @percentage{0.00%}; @value")
    start_angle=cumsum('angle', include_zero=True)
    end_angle=cumsum('angle')
    color = 'color'
    legend="status"
    
    fig = figure(plot_height=350, plot_width=430, title= 'OVERALL '+ticker1.value+' Rate', toolbar_location=None,
        x_range=(-0.5, 1.0))
    fig.title.align = 'center'
    fig.add_tools(hover)
    fig.wedge(x=0, y=1, radius=0.4,
        start_angle=start_angle, end_angle=end_angle,
        line_color="white", fill_color=color, legend=legend, source=source)
    
    labels = LabelSet(x=0, y=1, text="label", angle=start_angle,
            text_font_size="10pt", text_color="black",
            source=source)

    fig.add_layout(labels)
    fig.axis.axis_label=None
    fig.axis.visible=False
    fig.grid.grid_line_color = None
   
    plots = []
    n = 0
    for i in data_types:
        data = dict_extract(i, dictA, ticker1.value)
        data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'status'})
        data2['color'] = chart_colors[:len(data)]
        angle(data2)
        column_sum = data2['value'].sum()
        data2['percentage'] = (data2['value']/column_sum)
        data2['label'] = ["{:.2%}".format(p) for p in data2['percentage']]
        data2['label'] = data2['label'].astype(str)
        data2['label'] = data2['label'].str.pad(20, side = "left")
        source = ColumnDataSource(data2)
        
        p = figure(plot_height=350, plot_width=430, title= 'OVERALL ' +ticker1.value + ' Rate of ' + i, toolbar_location=None,
            x_range=(-0.5, 1.0))
        p.title.align = 'center'
        p.add_tools(hover)
        p.wedge(x=0, y=1, radius=0.4,
            start_angle=start_angle, end_angle=end_angle,
            line_color="white", fill_color=color, legend=legend, source=source)
        
        labels = LabelSet(x=0, y=1, text="label", angle=start_angle,
                text_font_size="10pt", text_color="black",
                source=source)

        p.add_layout(labels)
        
        p.xaxis.visible = False
        p.yaxis.visible=False
        p.grid.grid_line_color = None
        plots.append(p)

    return row(fig,*plots)


def make_plot_project(): ### show the figure with the project name such as 'P1', 'P2'
    
    dictP = group.get_group(ticker2.value).set_index('ProjectName').to_dict('list')
    data = dict_extract_all(data_types, dictP, ticker1.value)
    data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'status'})
    angle(data2)
    data2['color'] = chart_colors[:len(data)]
    column_sum = data2['value'].sum()
    data2['percentage'] = (data2['value']/column_sum)
    data2['label'] = ["{:.2%}".format(p) for p in data2['percentage']]
    data2['label'] = data2['label'].astype(str)
    data2['label'] = data2['label'].str.pad(20, side = "left")
    source = ColumnDataSource(data2)
    
    hover = HoverTool(tooltips="@status: @percentage{0.00%}; @value")
    start_angle=cumsum('angle', include_zero=True)
    end_angle=cumsum('angle')
    color = 'color'
    legend='status'
    
    fig = figure(plot_height=350, plot_width=430, title= ticker2.value + ' OVERALL ' + ticker1.value +' Rate', 
                 title_location="above", toolbar_location=None,
                x_range=(-0.5, 1.0))
    fig.title.align = 'center'
    fig.add_tools(hover)
    fig.wedge(x=0, y=1, radius=0.4,
            start_angle=start_angle, end_angle=end_angle,
            line_color="white", fill_color=color, legend=legend, source=source)
    labels = LabelSet(x=0, y=1, text="label", angle=start_angle,
            text_font_size="10pt", text_color="black",
            source=source)
    fig.add_layout(labels)
    
    fig.axis.axis_label=None
    fig.axis.visible=False
    fig.grid.grid_line_color = None

    plots = []
    n = 0    
    for i in data_types:
        dictP = group.get_group(ticker2.value).set_index('ProjectName').to_dict('list')
        data = dict_extract(i, dictP, ticker1.value)
        data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'status'})
        data2['color'] = chart_colors[:len(data)]
        angle(data2)
        column_sum = data2['value'].sum()
        data2['percentage'] = (data2['value']/column_sum)
        source = ColumnDataSource(data2)
    
        p = figure(plot_height=350, plot_width=430, title= ticker2.value+ ' '+ ticker1.value +' Rate of ' + i,
                   title_location="above",toolbar_location=None,
                    x_range=(-0.5, 1.0))
        p.title.align = 'center'
        p.add_tools(hover)
        p.wedge(x=0, y=1, radius=0.4,
            start_angle=start_angle, end_angle=end_angle,
            line_color="white", fill_color=color, legend=legend, source=source)
        
        labels = LabelSet(x=0, y=1, text="label", angle=start_angle,
                text_font_size="10pt", text_color="black",
                source=source)

        p.add_layout(labels)
        p.xaxis.visible=False
        p.yaxis.visible=False
        p.grid.grid_line_color = None
        plots.append(p)

    return row(fig,*plots)

data = pd.read_csv("/Users/xli677/Dropbox (Uni of Auckland)/xli677/Projects/MyTardis/Visualisation_with_Bokeh/SampleSheet_Bokeh_test.csv")
data2 = data.set_index('ProjectName')
group = data.groupby('ProjectName')    
dictA = data2.to_dict('list')

item_list = ['Returned', 'PassQC', 'Biopipeline']
data_types = ['RNA_seq','DNA_seq','Methyl_seq']
project_list = ['P1','P2','P3','All']
status_list = ['Complete','Under Processing' ,'Awaiting Processing']

def update(attr, old, new):
    my_layout.children[1] = make_plot_all() 
    my_layout.children[2] = make_plot_project() 
    
# set up widgets
ticker1 = Select(title="Pages:", value='Returned', options=item_list)
ticker1.on_change('value', update)

ticker2 = Select(title="Projects:", value='P1', options=project_list)
ticker2.on_change('value', update)

widgets = column(ticker1, ticker2, sizing_mode="fixed",height=110, width=150)
#layout = row(widgets, make_plot_all(),make_plot_project())

my_layout = column(children=[widgets, 
                              make_plot_all(),
                              make_plot_project()],
                              sizing_mode='stretch_width')
curdoc().add_root(my_layout)
curdoc().title = "test"