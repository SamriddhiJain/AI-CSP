import networkx as nx  
import matplotlib.pyplot as plt

# plt.gca().invert_yaxis()
# plt.gca().invert_xaxis()

class gui():
	def __init__(self, domains, relations, order, edge_check):                                                                                   
		self.graph = nx.MultiGraph()
		self.domains = domains
		self.relations = relations
		self.order = order
		self.edge_check = edge_check

		xO = 0
		yO = 0
		step = 10                                                                

		#add variables and values
		for i,var in enumerate(list(reversed(order))):                              
			self.graph.add_node(var, pos=(yO,xO))
			yO = yO + step
		pos = {city:(long, lat) for (city, (lat,long)) in nx.get_node_attributes(self.graph, 'pos').items()}  
		nx.draw_networkx(self.graph, pos, node_color='r', with_labels=True)

		#add values
		node_list = []
		yO = 0
		for i,var in enumerate(list(reversed(order))):                              
			for index,val in enumerate(domains[var]):
				self.graph.add_node(var+": "+val,pos=(yO,xO+((index+1)*step)), node_size=500)
				node_list.append(var+": "+val)

			yO = yO + step                                                                           
		
		positions = nx.spring_layout(self.graph )
		pos = {city:(long, lat) for (city, (lat,long)) in nx.get_node_attributes(self.graph, 'pos').items()}  
		nx.draw_networkx(self.graph, pos, nodelist=node_list, node_color='b', with_labels=True)
		plt.show()
		
	'''
	Color code: Values before assigned values: blue
				Values after assigned values: green
				Assigned values: red
				Deleted values: black
	'''
	def update(self, currentDomain, assignment, currVar="", currVal=""):
		xO = 0
		yO = 0
		step = 10                                                                

		#add variables
		for i,var in enumerate(list(reversed(self.order))):                              
			self.graph.add_node(var, pos=(yO,xO))
			yO = yO + step
		pos = {city:(long, lat) for (city, (lat,long)) in nx.get_node_attributes(self.graph, 'pos').items()}  
		nx.draw_networkx(self.graph, pos, node_color='r', with_labels=True)

		#add values
		assigned_list = []
		previous_list = []
		future_list = []
		yO = 0
		for i,var in enumerate(list(reversed(self.order))):  
			flag = 0            
			for index,val in enumerate(self.domains[var]):
				self.graph.add_node(var+": "+val,pos=(yO,xO+((index+1)*step)), node_size=500)

				if((not flag) and var in assignment.keys() and val==assignment[var]):
					flag=1 #assigned value found
					assigned_list.append(var+": "+val)
				elif(not flag):
					previous_list.append(var+": "+val)
				else:
					future_list.append(var+": "+val)

			yO = yO + step                                                                           
		
		positions = nx.spring_layout(self.graph )
		pos = {city:(long, lat) for (city, (lat,long)) in nx.get_node_attributes(self.graph, 'pos').items()}  
		nx.draw_networkx(self.graph, pos, nodelist=assigned_list, node_color='r', with_labels=True)
		nx.draw_networkx(self.graph, pos, nodelist=previous_list, node_color='b', with_labels=True)
		nx.draw_networkx(self.graph, pos, nodelist=future_list, node_color='g', with_labels=True)

		pruned_list = []
		# pruned values
		for i,var in enumerate(list(reversed(self.order))):
			if(var not in assignment.keys()):         
				for index,val in enumerate(self.domains[var]):
					if(val not in currentDomain[var]):
						pruned_list.append(var+": "+val)

		nx.draw_networkx(self.graph, pos, nodelist=pruned_list, node_color='y', with_labels=True)

		if(currVar and currVal):
			currNode = []
			currNode.append(currVar+": "+currVal)
			nx.draw_networkx(self.graph, pos, nodelist=currNode, node_color='w', with_labels=True)

		# add edges to the assigned list
		if(self.edge_check):
			for var1 in assignment.keys():
				for var2 in assignment.keys():
					if((var1,var2) in self.relations.keys()):
						self.graph.add_edge(var1+": "+assignment[var1],var2+": "+assignment[var2])
					elif((var2,var1) in self.relations.keys()):
						self.graph.add_edge(var2+": "+assignment[var2],var1+": "+assignment[var1])
		
		plt.show()