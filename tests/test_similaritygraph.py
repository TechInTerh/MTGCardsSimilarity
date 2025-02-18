from pathlib import Path
from unittest import TestCase

import networkx.algorithms.isomorphism

from src.similaritygraph import SimilarityGraph
from tests import path_resources_tests


class TestSimilarityGraph(TestCase):
	def assert_files_equal(self, file1: Path, file2: Path):
		with open(file1, 'r') as f1, open(file2, 'r') as f2:
			for line1, line2 in zip(f1, f2):
				self.assertEqual(line1, line2)

	def assert_similar_graphs(self, graph1: SimilarityGraph, graph2: SimilarityGraph):
		self.assertEquals(type(graph1.graph), type(graph2.graph))
		self.assertEquals(graph1.graph.nodes, graph2.graph.nodes)
		self.assertEquals(graph1.graph.edges, graph2.graph.edges)
		self.assertTrue(networkx.algorithms.isomorphism.is_isomorphic(graph1.graph, graph2.graph))

	def test_write_load_graph(self):
		simi_graph = SimilarityGraph(show_display=False)
		simi_graph.add_card('Dusk // Dawn', 3)
		self.assertLessEqual(len(simi_graph), 36)
		self.assertGreaterEqual(len(simi_graph), 7)
		simi_graph.write_graph(path_resources_tests / 'test_write_graph.gml')
		other_graph = SimilarityGraph.load_graph(path_resources_tests / 'test_write_graph.gml',
			show_display=False)

		self.assert_similar_graphs(simi_graph, other_graph)
