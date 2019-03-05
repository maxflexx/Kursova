import owlready2 as owlready
from career import *
from skill import *
from user import *
from sorter import *


def group_individuals(individuals):
	for i in range(len(individuals)):
		individual = individuals[i]
		if individual.is_a[0].name == Career.nameInOntology:
			Career.careers.append(Career(individual.career_id[0], individual.career_name[0], individual.requireSkill))
			continue
		if individual.is_a[0].name == User.ontologyName:
			User.users.append(User(individual.user_id[0], individual.first_name[0], individual.last_name[0], individual.wanted_career_id[0], individual.hasSkill))
			continue
		else:
			language = []
			if hasattr(individual, 'usesLanguageFrontend'):
				language = individual.usesLanguageFrontend
			if len(language) == 0:
				language = individual.usesLanguageBackend
			Skill.skills.append(Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], language))


def get_data(onto):
	ind = onto.individuals()
	individuals = []
	for i in ind:
		individuals.append(i)
	group_individuals(individuals)


def load_data():
	o = owlready.get_ontology("file://RiepkinKursova1.owl").load()
	get_data(o)

#u = Sorter.sort_users_for_career(Career.careers[0], User.users)
#print(u[0].userId)
#print(u[0].firstName)
#print(u[0].lastName)
