from ontology.skill import *


class Company:
	ontologyName = "Company"

	companies = []
	owl_companies = []

	def __init__(self, company_id, name):
		self.company_id: int = company_id
		self.company_name: str = name

	@staticmethod
	def generate_id():
		maxi = 0
		for s in Company.companies:
			if maxi < s.id[0]:
				maxi = s.id[0]
		return maxi + 1

