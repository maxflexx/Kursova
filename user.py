from skill import *


class User:
	ontologyName = "User"

	users = []

	def __init__(self, user_id: int, first_name: str, last_name: str, career_id: int, skills: [Skill]):
		self.userId: int = user_id
		self.firstName: str = first_name
		self.lastName: str = last_name
		self.userSkills: [Skill] = Skill.get_skill_array(skills)
		self.skillWeight: float = 0
		self.careerId: int = career_id

	@staticmethod
	def user_out(user_array):
		res = ""
		for u in user_array:
			res += u.firstName + " " + u.lastName + "\n"
			for skill in u.userSkills:
				res += "       Skill name: " + skill.skillName + "\n"
		return res
