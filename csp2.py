'''Implementation of the Generalized Lookahead Search algorithms'''
import json
import copy
import gui

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
		    self.assign = {}
		    self.gui = gui.gui(self.domain, self.constraints, self.order)

	# two variables with given values are consistent
	def consistent(self, x1, v1, x2, v2):
		if((x1,x2) in self.constraints.keys()):
			rel = self.constraints[(x1,x2)]
			return ([v1,v2] in rel)
		elif((x2,x1) in self.constraints.keys()):
			rel = self.constraints[(x2,x1)]
			return ([v2,v1] in rel)
		else:
			return True

	# a variable value pair is consistent with an assignment
	def consistentAssign(self, x1, v1, assignment):
		for var in assignment.keys():
			if(not self.consistent(x1, v1, var, assignment[var])):
				return False

		return True

	def consistentFull(self, x1, v1, x2, v2, x3, v3, assignment):
		return (
			self.consistent(x1, v1, x2, v2) and self.consistent(x1, v1, x3, v3) and self.consistent(x3, v3, x2, v2) and
			self.consistentAssign(x1, v1, assignment) and self.consistentAssign(x2, v2, assignment) and 
			self.consistentAssign(x3, v3, assignment))

	def revise(self, x, y, z, val, variables, domains, assignment):
		Fl=False
		for b in domains[variables[x]]:
			flag=0
			for c in domains[variables[y]]:
				if(self.consistentFull(variables[x], b, variables[y], c, variables[z], val, assignment)):
					flag = 1
					break

			if(not flag):
				domains[variables[x]].remove(b)
				Fl=True

		return Fl, domains

	def selectValueAC(self, index, var, dom, assignment):
		while len(dom[var[index]]):
			flag = 0
			temp = copy.deepcopy(dom)
			val = dom[var[index]][0]
			dom[var[index]].remove(val)

			removedValue = True
			while(removedValue):
				removedValue = False
				for j in range(index+1, len(var)):
					for k in range(index+1,len(var)):
						if(not (j==k)):
							valR, dom = self.revise(j,k,index,val,var,dom,assignment)
							removedValue = valR
			self.gui.update(dom,self.assign,var[index], val)
			
			for j in range(index+1, len(var)):
				if(not len(dom[var[j]])): # inconsistent
					flag = 1
					break

			if(flag):
				temp[var[index]] = copy.deepcopy(dom[var[index]])
				dom = copy.deepcopy(temp)
				self.gui.update(dom,self.assign,var[index], val)
			else:
				return val, dom

		return None, dom

	def selectValueFullAC(self, index, var, dom, assignment):
		while len(dom[var[index]]):
			flag = 0
			temp = copy.deepcopy(dom)
			val = dom[var[index]][0]
			dom[var[index]].remove(val)

			for j in range(index+1, len(var)):
				for k in range(index+1,len(var)):
					if(not (j==k)):
						valR, dom = self.revise(j,k,index,val,var,dom,assignment)
			self.gui.update(dom,self.assign,var[index], val)
			
			for j in range(index+1, len(var)):
				if(not len(dom[var[j]])): # inconsistent
					flag = 1
					break

			if(flag):
				temp[var[index]] = copy.deepcopy(dom[var[index]])
				dom = copy.deepcopy(temp)
				self.gui.update(dom,self.assign,var[index], val)
			else:
				return val, dom

		return None, dom

	def selectValuePartialAC(self, index, var, dom, assignment):
		while len(dom[var[index]]):
			flag = 0
			temp = copy.deepcopy(dom)
			val = dom[var[index]][0]
			dom[var[index]].remove(val)

			for j in range(index+1, len(var)):
				for k in range(j+1,len(var)):
					valR, dom = self.revise(j,k,index,val,var,dom,assignment)

			self.gui.update(dom,self.assign,var[index], val)
			
			for j in range(index+1, len(var)):
				if(not len(dom[var[j]])): # inconsistent
					flag = 1
					break

			if(flag):
				temp[var[index]] = copy.deepcopy(dom[var[index]])
				dom = copy.deepcopy(temp)
				self.gui.update(dom,self.assign,var[index], val)
			else:
				return val, dom

		return None, dom

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
				self.gui.update(dom,self.assign,var[index], val)

				if(not len(dom[var[k]])): # inconsistent
					temp[var[index]] = copy.deepcopy(dom[var[index]])
					dom = copy.deepcopy(temp)
					flag = 1
					break

			self.gui.update(dom,self.assign, var[index], val)
			
			if(not flag):
				return val, dom

		return None, dom

	def genaralisedLookAhead(self, func):
		dom = copy.deepcopy(self.domain)
		var = self.order
		domains = []

		i = 0
		while(i>=0 and i<len(var)):
			domains.append(copy.deepcopy(dom))
			a, dom1 = func(i, var, dom, self.assign)
			if(not a):
				# print "Backtrack at "+var[i]
				i = i-1
				dom = domains.pop()
				dom = domains.pop()
				dom[var[i]] = dom1[var[i]]
				self.assign.pop(var[i])
			else:
				self.assign[var[i]] = a
				dom = copy.deepcopy(dom1)
				i = i+1

			self.gui.update(dom,self.assign)

		if i<0:
			return None
		else:
			return self.assign
