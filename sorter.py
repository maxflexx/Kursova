import numpy as np
from skill import *
from career import *
from user import *

# if == then (career_skills_len - index) * 2
# if !=, but use the same language, then (career_skills_len - index) * 1.7
# if !=, but the same category, then (career_skills_len - index) * 1.5
# if !=, but the same category(back/front), then (career_skills_len - index) * 1.2
class Sorter:
	@staticmethod
	def sort_users_for_career(career: Career, users: [User]):
		for user in users:
			for userSkill in user.userSkills:
				for careerSkill in career.careerSkills:
					if careerSkill.skillId == userSkill.skillId:
						user.skillWeight
