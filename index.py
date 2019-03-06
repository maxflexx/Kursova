from owlready2 import *
from career import *
from skill import *
from user import *
from sorter import *
import owlClasses as cl

ontology = get_ontology("file://Kursova11.owl").load()


def group_individuals(individuals):
	for i in range(len(individuals)):
		individual = individuals[i]
		if individual.is_a[0].name == Career.nameInOntology:
			Career.careers.append(Career(individual.career_id[0], individual.career_name[0], individual.requireSkill))
			c = ontology.Career(individual.name, individual.namespace)
			Career.owl_careers.append(c)
			continue
		if individual.is_a[0].name == User.ontologyName:
			User.users.append(User(individual.user_id[0], individual.first_name[0], individual.last_name[0], individual.wanted_career_id[0], individual.hasSkill))
			u = ontology.User(individual.name, individual.namespace)
			User.owl_users.append(u)
			continue
		else:
			language = []
			if hasattr(individual, 'usesLanguageFrontend'):
				language = individual.usesLanguageFrontend
			if len(language) == 0:
				language = individual.usesLanguageBackend
			Skill.skills.append(Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], language))
			if individual.is_a[0].name == "BackendFramework":
				print(ontology.BackendFramework)
				s = ontology.BackendFramework(individual.name, individual.namespace)
				Skill.owl_skills.append(s)
			elif individual.is_a[0].name == "BackendLanguage":
				s = ontology.BackendLanguage(individual.name, individual.namespace)
				Skill.owl_skills.append(s)
			elif individual.is_a[0].name == "BackendTechnology":
				s = ontology.BackendTechnology(individual.name, individual.namespace)
				Skill.owl_skills.append(s)
			elif individual.is_a[0].name == "NonRelational":
				s = ontology.NonRelational(individual.name, individual.namespace)
				Skill.owl_skills.append(s)
			elif individual.is_a[0].name == "Relational":
				s = ontology.Relational(individual.name, individual.namespace)
				Skill.owl_skills.append(s)
			elif individual.is_a[0].name == "FrontFramework":
				s = ontology.FrontFramework(individual.name, individual.namespace)
				Skill.owl_skills.append(s)
			elif individual.is_a[0].name == "FrontLanguage":
				s = ontology.FrontLanguage(individual.name, individual.namespace)
				Skill.owl_skills.append(s)
			elif individual.is_a[0].name == "FrontTechnology":
				s = ontology.FrontTechnology(individual.name, individual.namespace)
				Skill.owl_skills.append(s)


def get_data(onto):
	ind = onto.individuals()
	individuals = []
	for i in ind:
		individuals.append(i)
	group_individuals(individuals)


#get_data(ontology)

def load_data():
#	ontology = get_ontology("file://RiepkinKursova1.owl").load()
	get_data(ontology)



