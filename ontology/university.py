from ontology.skill import *


class University:
	ontologyName = "University"

	universities = []
	owl_universities = []

	def __init__(self, university_id, name):
		self.university_id: int = university_id
		self.university_name: str = name

	@staticmethod
	def get_owl_university_by_name(university_name):
		for s in University.owl_universities:
			if s.university_name[0] == university_name:
				return s

	@staticmethod
	def get_owl_university_by_id(id):
		for s in University.owl_universities:
			if s.university_id[0] == id:
				return s

	@staticmethod
	def generate_id():
		maxi = 0
		for s in University.universities:
			if maxi < s.id[0]:
				maxi = s.id[0]
		return maxi + 1

