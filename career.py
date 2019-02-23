from skill import *


class Career:
	nameInOntology = "Career"
	careers = []

	def __init__(self, skill_id: int, name: str, skills: [Skill]):
		self.id: int = skill_id
		self.name: str = name
		self.careerSkills: [Skill] = Skill.get_skill_array(skills)

