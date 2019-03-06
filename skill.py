import json
class Skill:
	ontologyNames = ['BackendFramework', 'BackendTechnology', 'BackendLanguage', 'NonRelational', 'Relational',
					 'FrontendFramework', 'FrontendLanguage']

	skills = []
	owl_skills = []

	def __init__(self, class_name: str, skill_id: int, skill_name: str, uses_language=[]):
		self.className: str = class_name
		self.skillId: int = skill_id
		self.skillName: str = skill_name
		self.usesLanguage: Skill = Skill.get_skill_array(uses_language)[0]

	@staticmethod
	def get_skill_array(skills):
		result = []
		for i in range(len(skills)):
			individual = skills[i]
			language = []
			if hasattr(individual, 'usesLanguageFrontend'):
				language = individual.usesLanguageFrontend
			if len(language) == 0:
				language = individual.usesLanguageBackend
			result.append(Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], language))
		if len(result) == 0:
			return [None]
		return result

