import numpy as np
import pandas as pd
from bokeh.layouts import  layout, widgetbox, row
from bokeh.palettes import Spectral8
from bokeh.models import Select
from bokeh.plotting import figure
from bokeh.io import curdoc
df = pd.read_csv('https://raw.githubusercontent.com/ffzs/dataset/master/insurance.csv')

# 获取图像的函数
def get_figure():
    grouped = df.groupby('sex')  # 以性别分组
    data = grouped.get_group(gender.value)  # 获取选取的性别为变量
    color_col = color.value   # 获取颜色分类的属性
    color_class = pd.Categorical(data[color_col])   # 将颜色分类数据明确化
    c = [Spectral8[i] for i in color_class.codes]   # 获取颜色列表
    s = [(np.sqrt(i)+2) for i in data['age']]   # 将年龄数据开方用大小表示用以区别年龄大小
    p = figure()
    p.circle(x=data["bmi"], y=data["charges"], color=c, size=s)   # 绘图
    return p

# 数据更新函数
def update(attr, old, new):
    layout.children[1] = get_figure()  # 将第二子图更新


# 设置下拉选项进行性别的选择
gender = Select(title='Gender', value='male', options=['female', 'male'])
gender.on_change('value', update)
# 设置下拉选项进行颜色区分的选择
color = Select(title='Color', value='region', options=['region', 'smoker', 'children'])
color.on_change('value', update)

controls = widgetbox([gender, color], width=200)  # 将小部件放在一起
layout = row(controls, get_figure())  # 小部件和图横向排列

curdoc().add_root(layout)  # 添加layout
curdoc().title = "Insurence"  # 标题设置

# bokeh serve --show insurance_graph.py   进行启动