import owlready2 as owlready
from career import *
from skill import *
from user import *

careers = []
skills = []
users = []


def group_individuals(individuals):
	for i in range(len(individuals)):
		individual = individuals[i]
		print(individual.is_a[0].name)
		if individual.is_a[0].name == Career.nameInOntology:
			careers.append(Career(individual.career_id[0], individual.career_name[0], individual.requireSkill))
			continue
		if individual.is_a[0].name == User.ontologyName:
			users.append(User(individual.user_id[0], individual.first_name[0], individual.last_name[0], individual.hasSkill))
			continue
		else:
			language = []
			if hasattr(individual, 'usesLanguageFrontend'):
				language = individual.usesLanguageFrontend
			if len(language) == 0:
				language = individual.usesLanguageBackend
			skills.append(Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], language))


def get_data(onto):
	ind = onto.individuals()
	individuals = []
	for i in ind:
		individuals.append(i)
	group_individuals(individuals)



o = owlready.get_ontology("file://RiepkinKursova.owl")
onto = o.load()
get_data(onto)
for i in careers:
	print(str(i))
print(users)
print(skills)
