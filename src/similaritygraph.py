import networkx as nx
from IPython.core.display_functions import display

from src.plotly_graph_plotler import GraphPloter
from IPython.display import HTML, DisplayHandle
from src.myedhrec import MyEDHREc

delimiter = ';'


class SimilarityGraph:
	def __init__(self, graph: nx.DiGraph = None, show_display=True):
		if graph is None:
			graph = nx.DiGraph()
		self.graph = graph
		self.ploter = GraphPloter()
		self.edhrec_asker = MyEDHREc()
		self.max_add = 6 ** 5
		self.display_bar: DisplayHandle | None = display(self._progress(),
			display_id=True) if show_display else None

	def _progress(self, card=None):
		return HTML(f"Current card : {card}<br>Number of Cards : {len(self.graph.nodes)}")

	def _update_display(self, text: str | HTML):
		if self.display_bar is not None:
			# if isinstance(text, HTML):
			# 	text = text.data
			self.display_bar.update(text)

	@staticmethod
	def load_graph(file_path: str, **kwargs):
		return SimilarityGraph(graph=nx.read_gml(file_path), **kwargs)

	def write_graph(self, file_path: str):
		nx.write_gml(self.graph, file_path)

	def add_card(self, card_name: str, depth_similar_cards: int = 1):
		self._rec_add_card(card_name, depth_similar_cards)

	def __len__(self):
		return len(self.graph.nodes)

	def _rec_add_card(self, card_name: str, depth_similar_cards: int):
		similar_cards = self.edhrec_asker.get_similar_cards(card_name)
		self._update_display(self._progress(card_name))
		for card in similar_cards:
			self.graph.add_edge(card_name, card["name"], weight=1)
			if len(self) >= self.max_add:
				self._update_display(
					f"Max number of cards reached :  + {len(self)} / {self.max_add}")
			elif depth_similar_cards > 1 and self.graph.out_degree(card["name"]) == 0:
				self._rec_add_card(card["name"], depth_similar_cards - 1)

	def plot_graph(self):
		return self.ploter.plot_graph(self.graph)
