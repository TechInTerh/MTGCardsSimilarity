import networkx as nx
from IPython.core.display_functions import DisplayHandle

from src.plotly_graph_plotler import PlotlyGraphPloter
from IPython.display import HTML, display
from src.myedhrec import MyEDHREc

delimiter = ';'


class SimilarityGraph:
	def __init__(self, graph: nx.DiGraph = nx.DiGraph()):
		self.graph = graph
		self.delimiter = ';'
		self.ploter = PlotlyGraphPloter()
		self.edhrec_asker = MyEDHREc()
		self.count_cards = 0

	def _progress(self, card=None):
		return HTML(f"""Current card : {card}<br> Number of Cards : {self.count_cards}""")

	@staticmethod
	def load_graph(file_path: str):
		return SimilarityGraph(nx.read_adjlist(file_path, delimiter=delimiter))

	def write_graph(self, file_path: str):
		nx.write_adjlist(self.graph, file_path, delimiter=delimiter)

	def add_card(self, card_name: str, depth_similar_cards: int = 1):
		display_bar = display(self._progress(), display_id=True)
		self._rec_add_card(card_name, depth_similar_cards, display_bar)

	def _rec_add_card(self, card_name: str, depth_similar_cards: int, display_bar: DisplayHandle):
		similar_cards = self.edhrec_asker.get_similar_cards(card_name)
		self.count_cards += 1
		display_bar.update(self._progress(card_name))
		for card in similar_cards:
			self.graph.add_edge(card_name, card['name'], weight=1)
			if depth_similar_cards > 1 and self.graph.out_degree(card['name']) == 0:
				self._rec_add_card(card['name'], depth_similar_cards - 1, display_bar)

	def plot_graph(self):
		return self.ploter.plot_graph(self.graph)
