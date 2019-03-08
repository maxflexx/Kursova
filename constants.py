from telebot import types
import career
import skill
import operator

key = '774248413:AAFO2klpR1LX8KyO1E1CFNNC7CPGOoa4ink'
clearifySkillClassKeyBoard = types.ReplyKeyboardMarkup(True, False)

clearifySkillClassKeyBoard.row('/BackendFramework')
clearifySkillClassKeyBoard.row('/BackendLanguage')
clearifySkillClassKeyBoard.row('/BackendTechnology')
clearifySkillClassKeyBoard.row('/RelationalDatabase')
clearifySkillClassKeyBoard.row('/NonRelationalDatabase')
clearifySkillClassKeyBoard.row('/FrontendFramework')
clearifySkillClassKeyBoard.row('/FrontendLanguage')
clearifySkillClassKeyBoard.row('/FrontendTechnology')


adminKeyBoard = types.ReplyKeyboardMarkup(True, False)
adminKeyBoard.row('/CreateNewVacancy')
adminKeyBoard.row('/SeeAllVacanciesAdmin')
adminKeyBoard.row('/Back')

userKeyBoard = types.ReplyKeyboardMarkup(True, False)
userKeyBoard.row('/SeeAllVacancies')


currentCareer = None
skill_ids = []
career_name = ""
uses_id = None
firstName = None
lastName = None

careerAdminKeyBoard = types.ReplyKeyboardMarkup(True, False)
careerAdminKeyBoard.row('/GetTheBestCandidates')
careerAdminKeyBoard.row('/GetAllData')
careerAdminKeyBoard.row('/Delete')
careerAdminKeyBoard.row('/Back')

careerUserKeyBoard = types.ReplyKeyboardMarkup(True, False)
careerUserKeyBoard.row('/GetAllData')
careerUserKeyBoard.row('/Apply')
careerUserKeyBoard.row('/Back')


def get_skills():
	skill.Skill.skills.sort(key=operator.attrgetter("skillId"), reverse=False)
	skillsKeyboard = types.ReplyKeyboardMarkup(True, False)
	write = True
	for s in skill.Skill.skills:
		for sk_id in skill_ids:
			if sk_id == s.skillId:
				write = False
				break
		if write:
			skillsKeyboard.row(str(s.skillId) + " " + s.skillName)
		write = True
	skillsKeyboard.row('CreateNewSkill')
	skillsKeyboard.row('Done')
	return skillsKeyboard


def get_careers():
	careersKeyBoard = types.ReplyKeyboardMarkup(True, False)
	for c in career.Career.careers:
		careersKeyBoard.row(str(c.id) + " " + c.name)
	return careersKeyBoard


# def get_skill_categories():
# 	skillCategoryKeyboard = types.ReplyKeyboardMarkup(True, False)
# 	for i in skill.Skill.ontologyNames:
# 		skillCategoryKeyboard.row(i)
# 	return skillCategoryKeyboard


def get_skill_main_categories():
	mainCategoryKeyboard = types.ReplyKeyboardMarkup(True, False)
	mainCategoryKeyboard.row('Framework')
	mainCategoryKeyboard.row('Back')
	return mainCategoryKeyboard


def get_languages():
	languagesKeyBoard = types.ReplyKeyboardMarkup(True, False)
	for s in skill.Skill.skills:
		if s.className == "BackendLanguage" or s.className == "FrontendLanguage":
			languagesKeyBoard.row(str(s.skillId) + " " + s.skillName)
	return languagesKeyBoard
