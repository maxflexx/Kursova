import numpy as np
from skill import *
from career import *
from user import *
import operator

# if == then (career_skills_len - index) * 2
# if !=, but use the same language, then (career_skills_len - index) * 1.7
# if !=, but the same category, then (career_skills_len - index) * (1.2 - 0.1 * how_far_is_father)
# does not count if father is skill
class Sorter:
	@staticmethod
	def sort_users_for_career(career: Career, users: [User]) -> [User]:
		for u in users:
			for userSkill in u.userSkills:
				u.skillWeight += Sorter.how_many_points_to_give(userSkill, career.careerSkills)
		users.sort(key=operator.attrgetter("skillWeight"), reverse=True)
		return User.user_out(users)

	@staticmethod
	def how_many_points_to_give(user_skill: Skill, career_skills: [Skill]) -> float:
		res = [0]
		career_skill_len = len(career_skills)
		for careerSkillIndex in range(career_skill_len):
			career_skill = career_skills[careerSkillIndex]
			# user knows exactly what needed
			if user_skill.skillId == career_skill.skillId:
				res.append((career_skill_len - careerSkillIndex) * 2)

		for careerSkillIndex in range(career_skill_len):
			career_skill = career_skills[careerSkillIndex]
			# user knows framework on the same language as needed
			if len(user_skill.usesLanguage) != 0 and user_skill.usesLanguage.skillId == career_skill.skillId:
				res.append((career_skill_len - careerSkillIndex) * 1.5)
			# user knows language which uses needed framework
			if len(career_skill.usesLanguage) != 0 and user_skill.skillId == career_skill.usesLanguage.skillId:
				res.append((career_skill_len - careerSkillIndex) * 1.5)
			# user knows framework on same language as needed
			if len(career_skill.usesLanguage) != 0 and len(user_skill.usesLanguage) != 0 \
				and user_skill.usesLanguage.skillId == career_skill.usesLanguage.skillId:
				res.append((career_skill_len - careerSkillIndex) * 1.5)
		return max(res)
		#TODO: write finding length to common father
		#for careerSkillIndex in range(career_skill_len):
		#	career_skill = career_skills[careerSkillIndex]
