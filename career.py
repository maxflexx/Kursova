from skill import *


class Career:
	nameInOntology = "Career"
	careers = []

	def __init__(self, skill_id: int, name: str, skills: [Skill]):
		self.id: int = skill_id
		self.name: str = name
		self.careerSkills: [Skill] = Skill.get_skill_array(skills)

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
			res += "Id: " + str(c.id) + " Name: " + c.name + "\n"
			for skill in c.careerSkills:
				res += "	Skill id: " + str(skill.skillId) + " Skill name: " + skill.skillName + "\n"
			res += "\n\n"
		return res

	@staticmethod
	def find_career_by_id(career_id):
		for c in Career.careers:
			if c.id == career_id:
				return c
		return None

