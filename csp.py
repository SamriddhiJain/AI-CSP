'''Implementation of the Generalized Lookahead Search algorithms'''
import json
import copy

class csp():
	def __init__(self, filename):
		with open(filename) as data_file:    
		    data = json.load(data_file)

		    self.domain = {}
		    for var in data["variables"]:
		    	self.domain[var["name"]] = var["domain"]

		    self.constraints = {}
		    for c in data["constraints"]:
		    	a = c["scope"][0]
		    	b = c["scope"][1]
		    	self.constraints[(a,b)] = c["relation"]

		    self.order = data["ordering"]

	def consistent(self, x1, v1, x2, v2):
		if((x1,x2) in self.constraints.keys()):
			rel = self.constraints[(x1,x2)]
			return ([v1,v2] in rel)
		elif((x2,x1) in self.constraints.keys()):
			rel = self.constraints[(x2,x1)]
			return ([v2,v1] in rel)
		else:
			return True

	def selectValueFC(self, index, var, dom, assignment):
		while len(dom[var[index]]):
			flag = 0
			temp = copy.deepcopy(dom)
			val = dom[var[index]][0]
			dom[var[index]].remove(val)

			for k in range(index+1, len(var)):
				for b in dom[var[k]]:
					if(not self.consistent(var[index], val, var[k], b)):
						dom[var[k]].remove(b)

				if(not len(dom[var[k]])): # inconsistent
					temp[var[index]] = copy.deepcopy(dom[var[index]])
					dom = copy.deepcopy(temp)
					flag = 1
					break
			
			if(not flag):
				return val, dom

		return None, dom

	def genaralisedLookAhead(self):
		dom = copy.deepcopy(self.domain)
		var = self.order
		domains = []

		assign = {}
		i = 0
		while(i>=0 and i<len(var)):
			domains.append(copy.deepcopy(dom))
			# print var[i]
			# print dom
			a, dom1 = self.selectValueFC(i, var, dom, assign)
			# print a
			# print dom1
			# print
			if(not a):
				# print "Backtrack at "+var[i]
				i = i-1
				dom = domains.pop()
				dom = domains.pop()
				dom[var[i]] = dom1[var[i]]
			else:
				assign[var[i]] = a
				dom = copy.deepcopy(dom1)
				i = i+1

		if i<0:
			return None
		else:
			return assign


pb = csp('t1.json')
print pb.genaralisedLookAhead()
