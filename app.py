import telebot
import constants
import career
import index
import sorter
import user

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


def process_career_select(message):
    careerId = str(message.text).split(' ')[0]
    constants.currentCareer = career.Career.find_career_by_id(int(careerId))
    if constants.currentCareer == None:
        bot.send_message(message.from_user.id, "Invalid career selected",
                               reply_markup=constants.adminKeyBoard)
    else:
        msg = bot.send_message(message.from_user.id, "What do you want to do?",
                         reply_markup=constants.careerAdminKeyBoard)
        bot.register_next_step_handler(msg, career_action)


def career_action(message):
    if message.text == "/GetTheBestCandidates":
        msg = bot.send_message(message.from_user.id, sorter.Sorter.sort_users_for_career(constants.currentCareer, user.User.users),
                               reply_markup=constants.careerAdminKeyBoard)
        bot.register_next_step_handler(msg, career_action)
    elif message.text == "/GetAllData":
        msg = bot.send_message(message.from_user.id,
                               career.Career.careers_out([constants.currentCareer]),
                               reply_markup=constants.careerAdminKeyBoard)
        bot.register_next_step_handler(msg, career_action)
    elif message.text == "/Back":
        handle_back(message)





@bot.message_handler(commands=['Back'])
def handle_back(message):
    hide = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "OK", reply_markup=hide)



if __name__ == "__main__":
    print("Starting bot..")
    index.load_data()
    bot.polling(none_stop=True, interval=0)
