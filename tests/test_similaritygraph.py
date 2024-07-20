from pathlib import Path
from unittest import TestCase

from src.similaritygraph import SimilarityGraph
from tests import path_resources_tests


class TestSimilarityGraph(TestCase):
	def assert_files_equal(self, file1: Path, file2: Path):
		with open(file1, 'r') as f1, open(file2, 'r') as f2:
			for line1, line2 in zip(f1, f2):
				self.assertEqual(line1, line2)

	def test_load_graph(self):
		self.fail()

	def test_write_graph(self):
		simi_graph = SimilarityGraph(show_display=False)
		simi_graph.add_card('Dusk // Dawn', 3)
		self.assertGreaterEqual(simi_graph.count_cards, 7)
		self.assertLess(simi_graph.count_cards, 36)
		simi_graph.write_graph(path_resources_tests / 'test_write_graph.txt')
		
