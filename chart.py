# -*- coding:utf-8 -*-
import os
import sys
import math
import copy

from db import db
from datetime import datetime


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import StackedHorizontalBarChart
from pygooglechart import Axis
      
WIDTH=500

def __max_x(data):
    result=0
    for i in data:
        if i>result:
            result=i
    return result

def __fullfile_chart(title,data,labels,color):
    chart=StackedHorizontalBarChart(WIDTH, len(data)*40,x_range=[0,__max_x(data)])
    chart.set_colours([color])
    chart.add_data(data)
    chart.set_axis_labels(Axis.TOP,[title])
    chart.set_axis_labels(Axis.LEFT,labels)
    chart.set_axis_labels(Axis.RIGHT, __r_labels(data))
    file_name='%s_%s.png' % (title.replace(' ','_').lower(),datetime.now().strftime('%Y-%m-%d'))
    chart.download(file_name)
    return file_name

def __r_labels(chart_data):
    result=copy.copy(chart_data)
    result.reverse()
    return result

def __chart_labels(data):
    labels=['%s,Since %s' % (i['action'],i['started_at']) for i in data]
    labels.reverse()
    return labels

def __data_and_labels(total=True):
    data=db.data()
    if total:
        return [i['count'] for i in data],__chart_labels(data)
    return [i['perday'] for i in data],__chart_labels(data)


def total():
    data,labels=__data_and_labels(True)
    return __fullfile_chart('Behavior Total Statistic',data,labels,'1B1BF8')

def frequency():
    data,labels=__data_and_labels(False)
    return __fullfile_chart('Behavior Frequency Statistic',data,labels,'A1D164')





    
