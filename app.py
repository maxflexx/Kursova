import telebot
import constants
from ontology import career, user, resume, sorter, ontologyInteraction
from analyze import resumeAnalyze
import os
bot = telebot.TeleBot(constants.key)


@bot.message_handler(commands=['admin'])
def handle_admin(message):
    admin_key_board = constants.adminKeyBoard
    bot.send_message(message.from_user.id, "OK, boss ", reply_markup=admin_key_board)


@bot.message_handler(commands=['user'])
def handle_user(message):
    user_key_board = constants.userKeyBoard
    bot.send_message(message.from_user.id, "That's what we've got ", reply_markup=user_key_board)


@bot.message_handler(commands=['SeeAllVacanciesAdmin'])
def show_all_vacancies(message):
    msg = bot.send_message(message.from_user.id, "All careers we have",
                                                 reply_markup=constants.get_careers())
    bot.register_next_step_handler(msg, process_career_select)


@bot.message_handler(commands=['SeeAllVacancies'])
def handle_see_all_vacancies_user(message):
    msg = bot.send_message(message.from_user.id, "All careers we have",
                           reply_markup=constants.get_careers())
    bot.register_next_step_handler(msg, process_career_select_user)


def process_career_select_user(message):
    careerId = str(message.text).split(' ')[0]
    constants.currentCareer = career.Career.find_career_by_id(int(careerId))
    if constants.currentCareer == None:

        bot.send_message(message.from_user.id, "Invalid career selected",
                         reply_markup=constants.userKeyBoard)
    else:
        msg = bot.send_message(message.from_user.id, "What do you want to do?",
                               reply_markup=constants.careerUserKeyBoard)
    bot.register_next_step_handler(msg, career_action_user)


def process_career_select(message):
    careerId = str(message.text).split(' ')[0]
    constants.currentCareer = career.Career.find_career_by_id(int(careerId))
    if constants.currentCareer == None:
        bot.send_message(message.from_user.id, "Invalid career selected",
                                   reply_markup= constants.adminKeyBoard)
    else:
        msg = bot.send_message(message.from_user.id, "What do you want to do?",
                         reply_markup=constants.careerAdminKeyBoard)
    bot.register_next_step_handler(msg, career_action)


def career_action_user(message):
    if message.text == "/GetAllData":
        msg = bot.send_message(message.from_user.id,
							   career.Career.careers_out([constants.currentCareer]),
							   reply_markup=constants.careerUserKeyBoard)
        bot.register_next_step_handler(msg, career_action_user)
    elif message.text == "/Apply":
        msg = bot.send_message(message.from_user.id, "Send your resume",
		 					   reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, handle_resume)
    elif message.text == "/Back":
        handle_back(message)
        constants.currentCareer = None

def handle_resume(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if str(file_info.file_path).endswith(".pdf") == False:
        msg = bot.send_message(message.from_user.id, "We accept only .pdf files",
							   reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, handle_back)

    resume_path = "../resumes" + "/" + constants.currentCareer.name + "/" + message.chat.username + ".pdf"
    if not os.path.exists("../resumes" + "/" + constants.currentCareer.name):
        os.makedirs("../resumes" + "/" + constants.currentCareer.name)
    with open(resume_path, "wb") as new_file:
        new_file.write(downloaded_file)
    resumeAnalyze.analyze(resume_path, constants.currentCareer.id)
    bot.register_next_step_handler(message, handle_back)


def career_action(message):
    if message.text == "/GetTheBestCandidates":
        msg = bot.send_message(message.from_user.id, sorter.Sorter.sort_resumes_for_career(constants.currentCareer,
																						 list(filter(lambda x: x.career_id == constants.currentCareer.id, resume.Resume.resumes))),
							   reply_markup=constants.careerAdminKeyBoard)
        bot.register_next_step_handler(msg, career_action)
    elif message.text == "/GetAllData":
        msg = bot.send_message(message.from_user.id,
							   career.Career.careers_out([constants.currentCareer]),
							   reply_markup=constants.careerAdminKeyBoard)
        bot.register_next_step_handler(msg, career_action)
    elif message.text == "/Delete":
        ontologyInteraction.OntologyInteraction.delete_career(constants.currentCareer.id)
        constants.currentCareer = None
        handle_back(message)
    elif message.text == "/Back":
        handle_back(message)
        constants.currentCareer = None


@bot.message_handler(commands=['CreateNewVacancy'])
def handle_vacancy_creation(message):
    constants.skill_ids = []
    constants.career_name = ""
    msg = bot.send_message(message.from_user.id, "Enter career name", reply_markup= telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, handle_vacancy_name_enter)


def handle_vacancy_name_enter(message):
    constants.career_name = message.text
    msg = bot.send_message(message.from_user.id, "Select required skills",
                           reply_markup=constants.get_skills())
    bot.register_next_step_handler(msg, skill_selection)


def skill_selection(message):
	if message.text == "CreateNewSkill":
		msg = bot.send_message(message.from_user.id, "What is it?", reply_markup=constants.get_skill_main_categories())
		bot.register_next_step_handler(msg, skill_creation)
	elif message.text == "Done":
		ontologyInteraction.OntologyInteraction.create_new_vacancy(constants.career_name, constants.skill_ids)
		bot.send_message(message.from_user.id, "New career created")
		handle_back(message)
	else:
		skill_id = str(message.text).split(' ')[0]
		constants.skill_ids.append(int(skill_id))
		msg = bot.send_message(message.from_user.id, "Select required skills",
                               reply_markup=constants.get_skills())
		bot.register_next_step_handler(msg, skill_selection)


def skill_creation(message):
	constants.uses_id = []
	if message.text == "Framework":
		msg = bot.send_message(message.from_user.id, "Select which language it uses", reply_markup=constants.get_languages())
		bot.register_next_step_handler(msg, language_selector)
	elif message.text == "Back":
		handle_back(message)


def language_selector(message):
	language_id = int(str(message.text).split(' ')[0])
	constants.uses_id = [language_id]
	msg = bot.send_message(message.from_user.id, "Enter new skill name", reply_markup=telebot.types.ReplyKeyboardRemove())
	bot.register_next_step_handler(msg, skill_name)


def skill_name(message):
	constants.skill_ids.append(
		ontologyInteraction.OntologyInteraction.create_new_skill(message.text, constants.uses_id))
	msg = bot.send_message(message.from_user.id, "Select required skills",
						   reply_markup=constants.get_skills())
	bot.register_next_step_handler(msg, skill_selection)


def handle_name_entering(message):
	data = str(message.text).split(' ')
	constants.firstName = data[0]
	constants.lastName = data[1]
	msg = bot.send_message(message.from_user.id, "Select required skills",
						   reply_markup=constants.get_skills())
	bot.register_next_step_handler(msg, skill_selection_user)


def handle_vacancy_name_enter_user(message):
    constants.currentCareer = career.Career.find_career_by_id(int(str(message.text).split(' ')[0]))
    msg = bot.send_message(message.from_user.id, "Select required skills",
                           reply_markup=constants.get_skills())
    bot.register_next_step_handler(msg, skill_selection_user)


def skill_selection_user(message):
	if message.text == "CreateNewSkill":
		msg = bot.send_message(message.from_user.id, "What is it?", reply_markup=constants.get_skill_main_categories())
		bot.register_next_step_handler(msg, skill_creation_user)
	elif message.text == "Done":
		ontologyInteraction.OntologyInteraction.create_new_user(constants.firstName, constants.lastName, constants.currentCareer.id, constants.skill_ids)
		bot.send_message(message.from_user.id, "Application accepted")
		handle_back(message)
	else:
		skill_id = str(message.text).split(' ')[0]
		constants.skill_ids.append(int(skill_id))
		msg = bot.send_message(message.from_user.id, "Select required skills",
                               reply_markup=constants.get_skills())
		bot.register_next_step_handler(msg, skill_selection_user)


def skill_creation_user(message):
	constants.uses_id = []
	if message.text == "Framework":
		msg = bot.send_message(message.from_user.id, "Select which language it uses", reply_markup=constants.get_languages())
		bot.register_next_step_handler(msg, language_selector_user)
	elif message.text == "Back":
		handle_back(message)


def language_selector_user(message):
	language_id = int(str(message.text).split(' ')[0])
	constants.uses_id = [language_id]
	msg = bot.send_message(message.from_user.id, "Enter new skill name", reply_markup=telebot.types.ReplyKeyboardRemove())
	bot.register_next_step_handler(msg, skill_name_user)


def skill_name_user(message):
	constants.skill_ids.append(
		ontologyInteraction.OntologyInteraction.create_new_skill(message.text, constants.uses_id))
	msg = bot.send_message(message.from_user.id, "Select required skills",
						   reply_markup=constants.get_skills())
	bot.register_next_step_handler(msg, skill_selection_user)


@bot.message_handler(commands=['Back'])
def handle_back(message):
    hide = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "OK", reply_markup=hide)



if __name__ == "__main__":
    ontologyInteraction.OntologyInteraction.load_data()
    bot.polling(none_stop=True, interval=0)
