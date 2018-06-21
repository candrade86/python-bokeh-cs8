import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Triangle, ColumnDataSource, Range1d, LabelSet, Label 
from bokeh.palettes import Spectral8

from graph import *

WIDTH = 500
HEIGHT = 500 

graph_data = Graph()
graph_data.debug_create_test_data()
graph_data.bfs(graph_data.vertexes[0])

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)


plot = figure(title='Carlos\' Super Cool Graph', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Triangle(size=60, angle=60, fill_color='color')

# this is drawing the edges from start to end
start_indexes = []
end_indexes = []

for start_index, vertex in enumerate(graph_data.vertexes):
    for e in vertex.edges:
        start_indexes.append(start_index)
        end_indexes.append(graph_data.vertexes.index(e.destination))


graph.edge_renderer.data_source.data = dict(
    start=start_indexes, # a list of indexes to start edges from
    end=end_indexes) # a list of vertex indexes to end edges at

### start of layout code

x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)




plot.renderers.append(graph)


source = ColumnDataSource(data=dict(height=[66, 71, 72, 68, 58, 62],
                                    weight=[165, 189, 220, 141, 260, 174],
                                    names=['Mark', 'Amir', 'Matt', 'Greg',
                                           'Owen', 'Juan']))

# Create a new dictionary to use as a data source, with three lists in it, ordered in the same way as verteses
# List of x valuses
#list of y valuses
#list of labels
 
value = [v.value for v in graph_data.vertexes] #TODO: Possible optimization: We run through this loop three times

label_source = ColumnDataSource(data=dict(x=x, y=y,  v=value))

p = figure(title='Dist. of 10th Grade Students at Lee High',
           x_range=Range1d(140, 275))
p.scatter(x='weight', y='height', size=8, source=source)
p.xaxis[0].axis_label = 'Weight (lbs)'
p.yaxis[0].axis_label = 'Height (in)'

labels = LabelSet(x='x', y='y', text='v', level='overlay',
              source=label_source, render_mode='canvas', text_align='center', text_baseline='middle')

plot.add_layout(labels)

output_file('graph.html')
show(plot)