# -*- coding:utf-8 -*-

##################################################################################################

import csv
import plotly.graph_objects as go

from util.fsUtils import Join

from common import getSharedPreferences
from webConfig import SHARED_PATH

##################################################################################################

sp           = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR = sp.getString('ANALYSIS_DIR')
HTML_PATH    = Join(ANALYSIS_DIR, 'static.html')

##################################################################################################


def getStatitics(path):
    with open(path, 'r') as fr:
        cr = csv.reader(fr, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL)

        labels = list()
        values = list()
        for row in cr:
            labels.append(row[0])
            values.append(row[1])

    layout = go.Layout(title='system call count')
    data = go.Pie(labels=labels, values=values)

    f = go.Figure(data=[data], layout=layout)
    #f.show()

    f.write_html(HTML_PATH, auto_open=True)

    return HTML_PATH
