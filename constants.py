from telebot import types
import career

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

careerAdminKeyBoard = types.ReplyKeyboardMarkup(True, False)
careerAdminKeyBoard.row('/GetTheBestCandidates')
careerAdminKeyBoard.row('/GetAllData')
careerAdminKeyBoard.row('/Delete')
careerAdminKeyBoard.row('/Back')

careerUserKeyBoard = types.ReplyKeyboardMarkup(True, False)
careerUserKeyBoard.row('/GetAllData')
careerUserKeyBoard.row('/Apply')
careerUserKeyBoard.row('/Back')


def get_careers():
	careersKeyBoard = types.ReplyKeyboardMarkup(True, False)
	for c in career.Career.careers:
		careersKeyBoard.row(str(c.id) + " " + c.name)
	return careersKeyBoard
