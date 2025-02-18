import networkx as nx
import gravis as gv


class GravisGraphPloter:
	def __init__(self):
		pass

	def assign_properties(self, g: nx.Graph):
		# Centrality calculation
		node_centralities = nx.in_degree_centrality(g)
		edge_centralities = nx.edge_betweenness_centrality(g)

		# Community detection
		communities = nx.algorithms.community.greedy_modularity_communities(g)

		# Graph properties
		g.graph['node_border_size'] = 1.5
		g.graph['node_border_color'] = 'white'
		g.graph['edge_opacity'] = 0.9

		# Node properties: Size by centrality, shape by size, color by community
		colors = [
			'red',
			'blue',
			'green',
			'orange',
			'pink',
			'brown',
			'yellow',
			'cyan',
			'magenta',
			'violet',
		]
		for node_id in g.nodes:
			node = g.nodes[node_id]
			node['size'] = 10 + node_centralities[node_id] * 100
			node['shape'] = 'circle'
			for community_counter, community_members in enumerate(communities):
				if node_id in community_members:
					break
			node['color'] = colors[community_counter % len(colors)]

		# Edge properties: Size by centrality, color by community (within=community color, between=black)
		for edge_id in g.edges:
			edge = g.edges[edge_id]
			source_node = g.nodes[edge_id[0]]
			target_node = g.nodes[edge_id[1]]
			edge['size'] = edge_centralities[edge_id] * 100
			edge['color'] = (
				source_node['color'] if source_node['color'] == target_node['color'] else 'black'
			)

	# Assign node and edge properties
	def plot_graph(self, G: nx.Graph):
		self.assign_properties(G)
		return gv.d3(
			G,
			edge_size_data_source='weight',
			use_edge_size_normalization=True,
			show_menu=True,
			graph_height=1000,
		)
