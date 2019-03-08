import json


class Skill:
	ontologyNames = ['BackendFramework', 'BackendTechnology', 'BackendLanguage', 'NonRelational', 'Relational',
					 'FrontendFramework', 'FrontendTechnology', 'FrontendLanguage']

	skills = []
	owl_skills = []

	def __init__(self, class_name: str, skill_id: int, skill_name: str, data=[]):
		self.className: str = class_name
		self.skillId: int = skill_id
		self.skillName: str = skill_name
		self.usesLanguage: [Skill] = Skill.get_language(data)
		self.usesFramework: [Skill] = Skill.get_framework(data)

	@staticmethod
	def get_language(skills):
		result = []
		for i in range(len(skills)):
			individual = skills[i]
			result.append(Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0]))
		if len(result) == 0:
			return None
		return result

	@staticmethod
	def get_framework(skills):
		result = []
		for i in range(len(skills)):
			individual = skills[i]
			result.append(Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0]))
		if len(result) == 0:
			return None
		return result

	@staticmethod
	def get_skill_array(skills):
		result = []
		for i in range(len(skills)):
			individual = skills[i]
			if len(individual.usesFramework) != 0:
				data = individual.usesFramework
				result.append(
					Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], data))
			elif len(individual.usesLanguage) != 0:
				data = individual.usesFramework
				result.append(
					Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], data))
			else:
				result.append(
					Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0]))
		if len(result) == 0:
			return [None]
		return result

	@staticmethod
	def get_owl_skill(skill_id):
		for s in Skill.owl_skills:
			if s.skill_id[0] == skill_id:
				return s

	@staticmethod
	def generate_id():
		maxi = 0
		for s in Skill.owl_skills:
			if maxi < s.skill_id[0]:
				maxi = s.skill_id[0]
		return maxi + 1
