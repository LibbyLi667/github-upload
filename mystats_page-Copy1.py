''' Create a simple genomics data stats dashboard.
Choose pages to show in the drop down widgets, and make selections

on the plots to update the summary and histograms accordingly.
.. note::
    Running this example requires downloading sample data. See
    the included `README`_ for more information.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve stocks
at your command prompt. Then navigate to the URL
    http://localhost:5006/stocks
.. _README: https://github.com/bokeh/bokeh/blob/master/examples/app/stocks/README.md
'''
from functools import lru_cache
from os.path import dirname, join

#import matplotlib.pyplot as plt
#from matplotlib.gridspec import GridSpec

import pandas as pd

from bokeh import mpl
from bokeh.io import curdoc, output_file, show
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, PreText, Select, Dropdown
from bokeh.plotting import figure

item_list = ['Returned', 'PassQC', 'Processed']
data_types = ['RNA_seq','DNA_seq','Methyl_seq']
project_list = ['P1','P2','P3']

#the datasets
data = pd.read_csv("/Users/xli677/Dropbox (Uni of Auckland)/xli677/Projects/MyTardis/Visualisation_with_Bokeh/SampleSheet_Bokeh_test.csv")
data2 = data.set_index('ProjectName')
group = data.groupby('ProjectName')
    
dictA = data2.to_dict('list');
dictP = group.get_group('P1').set_index('ProjectName').to_dict('list')

def dict_extract_all(datatype_list, dic, item):  ### count the number of true/false and return a dictionary for all data types 
    list_return_all = []
    for i in datatype_list:
        i = join(i + '_' + item)
        list_return_all += dic[i]
    dict_return_all = dict((x,list_return_all.count(x)) for x in [True,False])
    
    return dict_return_all.values()

def dict_extract(datatype_name, dic, item):  ### given data type, dictionary, to count the number of true/false and return a dictionary containg the number for each data type 
    list_return = dic[datatype_name + '_' + item]
    dict_return = dict((x,list_return.count(x)) for x in [True,False])
    
    return dict_return.values()

def make_plot_all(item):
    langs = ['Success','Failure']
    fig = plt.figure(figsize=(20,10), constrained_layout=True)
    gs = GridSpec(1, 2, figure=fig)

    ax = fig.add_subplot(gs[:, 0])
    ax.pie(dict_extract_all(data_types, dictA, item), labels= langs, autopct='%.1f%%',radius = 1.2)
    ax.set_title('OVERALL ' + item + ' RATE')

    gs01 = gs[1].subgridspec(1, len(data_types))
    n = 0
    for i in data_types:
        #name = join(i + "_" + item)
        ax = join('ax' + str(n))
        ax = fig.add_subplot(gs01[0, n])
        ax.pie(dict_extract(i,dictA, item), labels=langs, autopct='%.1f%%')
        ax.set_xlabel(i)
        n += 1
    ax.set_title('OVERALL '+ item +' RATE BY DATA TYPE')    

    return plt


def make_plot_project(project, item): ### show the figure with the project name such as 'P1', 'P2'
    langs = ['Success','Failure']
    dictP = group.get_group(project).set_index('ProjectName').to_dict('list')
    
    fig = plt.figure(figsize=(20,10), constrained_layout=True)
    gs = GridSpec(1, 2, figure=fig)
    
    # plot overall for project
    ax1 = fig.add_subplot(gs[:, 0])
    ax1.pie(dict_extract_all(data_types, dictP, item), labels= langs, autopct='%.1f%%',radius = 0.8)
    ax1.set_title(join(project + '_' + item + '_RATE'))
    
    # plot overall for project by data type
    gs11 = gs[1].subgridspec(1, len(data_types))
    n = 0
    for i in data_types:
        #name = join(i + '_' + item)
        #ax = join('ax' + str(n))
        ax2 = fig.add_subplot(gs11[0, n])
        ax2.pie(dict_extract(i, dictP, item), labels=langs, autopct='%.1f%%')
        ax2.set_xlabel(i)
        n += 1
    ax2.set_title(join(project + '_' +  item +' RATE BY DATA TYPE')) 
    
    return plt


def update_plot(attrname, old, new):
    item = ticker1.value

    plot_overall = make_plot_all(ticker1.value)
    plot_project = make_plot_project(item, ticker2.value)

    return plot_overall, plot_project

#DEFAULT_TICKERS = ['Returned Rate from Suppliers Rate', 'PassQC Rate', 'Processing Rate from Bio-pipeline']
#SECOND_TICKERS = ['Project1','Project2','Project3'] ### Need to be updateable according to the number of projects

# Set up widgets
#output_file("select.html")

item = 'Returned'
project = 'P1'

#items = {
#    'Returned': {
#        'projects': ['P1','P2','P3'],
#    },
#    'PassQC': {
#        'projects': ['P1','P2','P3'],
#    },
#    'Processed': {
#        'projects': ['P1','P2','P3'],
#    }
#}

#stats = PreText(text='', width=500)
ticker1 = Select(title="Pages:", value="Returned", options=item_list)
ticker1.on_change('value', update_plot)

ticker2 = Select(title="Projects:", value="P1", options=project_list)
ticker2.on_change('value', update_plot)

plot_all = make_plot_all('Returned')
plot_project = make_plot_project('P1','Returned')

#layouts
widgets = column(ticker1, ticker2)
##plots = column(plot_all, plot_proje)c
plots = column(make_plot_all,make_plot_project)
layout = column(widgets, plots)

curdoc().add_root(layout)
curdoc().title = "Genomics Stats"