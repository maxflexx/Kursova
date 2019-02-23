from skill import *


class User:
	ontologyName = "User"

	users = []

	def __init__(self, user_id: int, first_name: str, last_name: str, skills: [Skill]):
		self.userId: int = user_id
		self.firstName: str = first_name
		self.lastName: str = last_name
		self.userSkills: [Skill] = Skill.get_skill_array(skills)
		self.skillWeight: float = 0
