__author__ = 'james.morris'

import networkx as nx
from networkx_viewer import Viewer

G = nx.MultiGraph()
G.add_edge('a','b')
G.add_edge('b','c')
G.add_edge('c','a',0,{'fill':'green'})
G.add_edge('c','d')
G.add_edge('c','d',1,{'dash':(2,2)})
G.node['a']['outline'] = 'blue'
G.node['d']['label_fill'] = 'red'

app = Viewer(G)
app.mainloop()

