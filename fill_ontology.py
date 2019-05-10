import ontologyInteraction
import random
import skill

ontologyInteraction.OntologyInteraction.load_data()

def get_random_letters():
	letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
	res = ""
	str_length = random.randint(1, 10)
	for i in range(str_length):
		res += letters[random.randint(0, len(letters) - 1)]
	return res

def get_random_skill_ids():
	skills = skill.Skill.owl_skills
	skill_length = random.randint(1, 10)
	res = []
	for i in range(skill_length):
		res.append(skills[random.randint(0, len(skills) - 1)].skill_id[0])
	return res

career_id = 1
for i in range(200):
	ontologyInteraction.OntologyInteraction.create_new_user(get_random_letters(), get_random_letters(), career_id, get_random_skill_ids())
