from ontology.skill import *


class Career:
	nameInOntology = "Career"
	careers = []
	owl_careers = []

	def __init__(self, career_id: int, name: str, skills: [Skill]):
		self.id: int = career_id
		self.name: str = name
		self.careerSkills: [Skill] = Skill.get_skill_array(skills)

	@staticmethod
	def delete_career(career_id):
		for c in Career.careers:
			if c.id == career_id:
				Career.careers.remove(c)
				break
		for c in Career.owl_careers:
			if c.career_id[0] == career_id:
				Career.owl_careers.remove(c)
				break

	@staticmethod
	def get_all_careers():
		res = ""
		for c in Career.careers:
			res += "Id: " + str(c.id) + " Name: " + c.name + "\n"
			for skill in c.careerSkills:
				res += "	Skill id: " + str(skill.skillId) + " Skill name: " + skill.skillName + "\n"
			res += "\n\n"
		return res

	@staticmethod
	def careers_out(careers):
		res = ""
		for c in careers:
			res += " Name: " + c.name + "\n"
			for skill in c.careerSkills:
				res += "                 Skill name: " + skill.skillName + "\n"
			res += "\n\n"
		return res

	@staticmethod
	def find_career_by_id(career_id):
		for c in Career.careers:
			if c.id == career_id:
				return c
		return None

	@staticmethod
	def find_owl_career_by_id(career_id):
		for c in Career.owl_careers:
			if c.career_id[0] == career_id:
				return c
		return None

	@staticmethod
	def generate_career_id():
		maxi = -1
		for c in Career.careers:
			if c.id > maxi:
				maxi = c.id
		return maxi + 1

