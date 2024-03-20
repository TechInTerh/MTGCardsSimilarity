
import os

import networkx as nx
import networkx.algorithms.community

import matplotlib.pyplot as plt
import gravis as gv
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx
from pyedhrec import EDHRec

class MyEDHREc(EDHRec):
    def __init__(self):
        super().__init__()
        self._json_page_cards_url = "https://json.edhrec.com/pages/cards/"

    def get_similar_cards(self, cards_name: str):
        formatted_card_name = self.format_card_name(cards_name)
        url = f"{self._json_page_cards_url}{formatted_card_name}.json"
        data = self._get(url)
        return data["similar"]
    

class SimilarityGraphSnap(nx.DiGraph):
    def __init__(self):
        super().__init__()
        self.ploter = Plotly_Graph_Ploter()
        self.edhrec_asker = MyEDHREc()
    
    def add_card(self, card_name: str, depth_similar_cards: int = 1):
        similar_cards = self.edhrec_asker.get_similar_cards(card_name)
        for card in similar_cards:
            self.add_edge(card_name, card["name"], weight=1)
            if depth_similar_cards > 1:
                self.add_card(card["name"], depth_similar_cards - 1)
    def plot_graph(self):
        ploter = Plotly_Graph_Ploter()
        ploter.plot_graph(self)


class Plotly_Graph_Ploter():
    def __init__(self):
        pass
    def get_edge_trace(self,G:nx.Graph, pos:dict):
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend((x0,x1,None))
            edge_y.extend((y0,y1,None))

        return go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines+markers',
            marker = dict(color='red', size=10,symbol='arrow',angleref="previous")
        )

    def get_node_trace(self,G:nx.Graph, pos:dict):

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        return go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
    def plot_graph(self, G: nx.Graph):
        pos = nx.spring_layout(G)
        edge_trace = self.get_edge_trace(G, pos)
        node_trace = self.get_node_trace(G, pos)
        node_adjacencies = [len(adjacencies[1]) for adjacencies in G.adjacency()]
        node_trace.marker.color = node_adjacencies
        node_trace.text =list(pos.keys())
        fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.show()

mis_graph = nx.les_miserables_graph()

# It comes with an edge property named "weight" which can be used as edge size
gv.d3(mis_graph, edge_size_data_source='weight', use_edge_size_normalization=True)
graph = SimilarityGraphSnap()
graph.add_card("Pongify", 1)
gv.d3(graph, edge_size_data_source='weight', use_edge_size_normalization=True)
# Create a graph from a stored example


