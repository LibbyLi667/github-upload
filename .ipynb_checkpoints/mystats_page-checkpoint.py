''' Create a simple genomics data stats dashboard.
Choose pages to show in the drop down widgets, and make selections

on the plots to update the summary and histograms accordingly.
.. note::
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve --show mystats_page.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/stocks
.. _README: https://github.com/bokeh/bokeh/blob/master/examples/app/stocks/README.md
'''
from functools import lru_cache
from os.path import dirname, join

from math import pi
import pandas as pd

from bokeh.io import curdoc, output_file, show
from bokeh.layouts import layout, column, row, widgetbox
from bokeh.models import ColumnDataSource, PreText, Select, Dropdown, HoverTool
from bokeh.plotting import figure, curdoc
from bokeh.transform import cumsum

item_list = ['Returned', 'PassQC', 'Processed']
data_types = ['RNA_seq','DNA_seq','Methyl_seq']
project_list = ['P1','P2','P3']

def dict_extract_all(datatype_list, dic, item):  ### count the number of true/false and return a dictionary for all data types 
    list_return_all = []
    for i in datatype_list:
        i = join(i + '_' + item)
        list_return_all += dic[i]
    dict_return_all = dict((x,list_return_all.count(x)) for x in [True,False])
    
    return dict_return_all

def dict_extract(datatype_name, dic, item):  ### given data type, dictionary, to count the number of true/false and return a dictionary containg the number for each data type 
    list_return = dic[datatype_name + '_' + item]
    dict_return = dict((x,list_return.count(x)) for x in [True,False])
    
    return dict_return

def angle(data):
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    return 

chart_colors = ['#007bff','#e29e44','#44e5e2','#eeeeee','#d8e244','#e244db']


def make_plot_all():
    data = dict_extract_all(data_types, dictA, ticker1.value)
    data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'number'})
    angle(data2)
    data2['color'] = chart_colors[:len(data)]
    source = ColumnDataSource(data2)
    
    hover = HoverTool(tooltips="@number: @value")
    start_angle=cumsum('angle', include_zero=True)
    end_angle=cumsum('angle')
    color = 'color'
    legend='number'
    
    fig = figure(plot_height=350, plot_width=350, title= 'OVERALL '+ticker1.value+' RATE', toolbar_location=None,
        x_range=(-0.5, 1.0))
    fig.add_tools(hover)
    fig.wedge(x=0, y=1, radius=0.4,
        start_angle=start_angle, end_angle=end_angle,
        line_color="white", fill_color=color, legend=legend, source=source)
    fig.axis.axis_label=None
    fig.axis.visible=False
    fig.grid.grid_line_color = None
   
    plots = []
    n = 0
    for i in data_types:
        data = dict_extract(i, dictA, ticker1.value)
        data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'number'})
        data2['color'] = chart_colors[:len(data)]
        angle(data2)
        source = ColumnDataSource(data2)
        
        hover = HoverTool(tooltips="@number: @value")
        start_angle=cumsum('angle', include_zero=True)
        end_angle=cumsum('angle')
        color = 'color'
        legend='number'
        
        p = join('fig' + str(n))
        p = figure(plot_height=350, plot_width=350, title= 'OVERALL ' +ticker1.value + ' RATE BY DATA TYPE', toolbar_location=None,
            x_range=(-0.5, 1.0))
        p.wedge(x=0, y=1, radius=0.4,
            start_angle=start_angle, end_angle=end_angle,
            line_color="white", fill_color=color, legend=legend, source=source)
        p.xaxis.axis_label=i
        p.yaxis.visible=False
        p.grid.grid_line_color = None
        plots.append(p)

    return row(fig,*plots)


def make_plot_project(): ### show the figure with the project name such as 'P1', 'P2'
    dictP = group.get_group(ticker2.value).set_index('ProjectName').to_dict('list')
    data = dict_extract_all(data_types, dictP, ticker1.value)
    data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'number'})
    angle(data2)
    data2['color'] = chart_colors[:len(data)]
    source = ColumnDataSource(data2)
    
    hover = HoverTool(tooltips="@number: @value")
    start_angle=cumsum('angle', include_zero=True)
    end_angle=cumsum('angle')
    color = 'color'
    legend='number'
    
    fig = figure(plot_height=350, plot_width=350, title= ticker2.value + ' OVERALL ' + ticker1.value +' RATE', toolbar_location=None,
           x_range=(-0.5, 1.0))
    fig.wedge(x=0, y=1, radius=0.4,
            start_angle=start_angle, end_angle=end_angle,
            line_color="white", fill_color=color, legend=legend, source=source)
    fig.axis.axis_label=None
    fig.axis.visible=False
    fig.grid.grid_line_color = None

    plots = []
    n = 0    
    for i in data_types:
        dictP = group.get_group(ticker2.value).set_index('ProjectName').to_dict('list')
        data = dict_extract(i, dictP, ticker1.value)
        data2 = pd.Series(data).reset_index(name='value').rename(columns={'index':'number'})
        data2['color'] = chart_colors[:len(data)]
        angle(data2)
        
        hover = HoverTool(tooltips="@number: @value")
        start_angle=cumsum('angle', include_zero=True)
        end_angle=cumsum('angle')
        color = 'color'
        legend='number'
    
        p = figure(plot_height=350, plot_width=350, title= ticker2.value+ ' '+ ticker1.value +' RATE BY DATA TYPE', toolbar_location=None,
            x_range=(-0.5, 1.0))
        p.wedge(x=0, y=1, radius=0.4,
            start_angle=start_angle, end_angle=end_angle,
            line_color="white", fill_color=color, legend=legend, source=source)
        p.xaxis.axis_label = i
        p.yaxis.visible=False
        p.grid.grid_line_color = None
        plots.append(p)

    return row(fig,*plots)


data = pd.read_csv("/Users/xli677/Dropbox (Uni of Auckland)/xli677/Projects/MyTardis/Visualisation_with_Bokeh/SampleSheet_Bokeh_test.csv")
data2 = data.set_index('ProjectName')
group = data.groupby('ProjectName')    
dictA = data2.to_dict('list')

item_list = ['Returned', 'PassQC', 'Processed']
data_types = ['RNA_seq','DNA_seq','Methyl_seq']
project_list = ['P1','P2','P3']


def update(attr, old, new):
    my_layout.children[1] = make_plot_all() 
    my_layout.children[2] = make_plot_project() 
    
# set up widgets
ticker1 = Select(title="Pages:", value='Returned', options=item_list)
ticker1.on_change('value', update)

ticker2 = Select(title="Projects:", value='P1', options=project_list)
ticker2.on_change('value', update)

widgets = widgetbox([ticker1, ticker2])
layout = row(widgets, make_plot_all(),make_plot_project())

my_layout = column(children=[widgets, 
                              make_plot_all(),
                              make_plot_project()],
                              sizing_mode='stretch_both')

curdoc().add_root(my_layout)
curdoc().title = "Genomics Data Stats"