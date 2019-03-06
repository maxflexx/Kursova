from owlready2 import *
from career import *
from skill import *
from user import *
from sorter import *
import owlClasses as cl

ontology_file_name = "Kursova11.owl"


class OntologyInteraction:

	ontology = get_ontology("file://" + ontology_file_name).load()

	@staticmethod
	def group_individuals(individuals):
		for i in range(len(individuals)):
			individual = individuals[i]
			if individual.is_a[0].name == Career.nameInOntology:
				Career.careers.append(Career(individual.career_id[0], individual.career_name[0], individual.requireSkill))
				c = OntologyInteraction.ontology.Career(individual.name, individual.namespace)
				Career.owl_careers.append(c)
				continue
			if individual.is_a[0].name == User.ontologyName:
				User.users.append(User(individual.user_id[0], individual.first_name[0], individual.last_name[0], individual.wanted_career_id[0], individual.hasSkill))
				u = OntologyInteraction.ontology.User(individual.name, individual.namespace)
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
					print(OntologyInteraction.ontology.BackendFramework)
					s = OntologyInteraction.ontology.BackendFramework(individual.name, individual.namespace)
					Skill.owl_skills.append(s)
				elif individual.is_a[0].name == "BackendLanguage":
					s = OntologyInteraction.ontology.BackendLanguage(individual.name, individual.namespace)
					Skill.owl_skills.append(s)
				elif individual.is_a[0].name == "BackendTechnology":
					s = OntologyInteraction.ontology.BackendTechnology(individual.name, individual.namespace)
					Skill.owl_skills.append(s)
				elif individual.is_a[0].name == "NonRelational":
					s = OntologyInteraction.ontology.NonRelational(individual.name, individual.namespace)
					Skill.owl_skills.append(s)
				elif individual.is_a[0].name == "Relational":
					s = OntologyInteraction.ontology.Relational(individual.name, individual.namespace)
					Skill.owl_skills.append(s)
				elif individual.is_a[0].name == "FrontFramework":
					s = OntologyInteraction.ontology.FrontFramework(individual.name, individual.namespace)
					Skill.owl_skills.append(s)
				elif individual.is_a[0].name == "FrontLanguage":
					s = OntologyInteraction.ontology.FrontLanguage(individual.name, individual.namespace)
					Skill.owl_skills.append(s)
				elif individual.is_a[0].name == "FrontTechnology":
					s = OntologyInteraction.ontology.FrontTechnology(individual.name, individual.namespace)
					Skill.owl_skills.append(s)

	@staticmethod
	def get_data(onto):
		ind = onto.individuals()
		individuals = []
		for i in ind:
			individuals.append(i)
		OntologyInteraction.group_individuals(individuals)

	@staticmethod
	def load_data():
		OntologyInteraction.ontology = get_ontology("file://" + ontology_file_name).load()
		User.users = []
		User.owl_users = []
		Career.careers = []
		Career.owl_careers = []
		Skill.skills = []
		Skill.owl_skills = []
		OntologyInteraction.get_data(OntologyInteraction.ontology)

	@staticmethod
	def delete_career(career_id):
		ind = list(OntologyInteraction.ontology.individuals())
		for i in ind:
			if len(i.career_id) != 0  and i.career_id[0] == career_id:
				destroy_entity(i)
			if len(i.wanted_career_id) != 0 and i.wanted_career_id[0] == career_id:
				destroy_entity(i)
		OntologyInteraction.ontology.save(ontology_file_name)
		OntologyInteraction.load_data()

	@staticmethod
	def create_new_vacancy(career_name, skill_ids):
		skills = []
		for i in skill_ids:
			skills.append(Skill.get_owl_skill(i))
		car = OntologyInteraction.ontology.Career()
		car.requireSkill = skills
		car.career_id = [Career.generate_career_id()]
		car.career_name = [career_name]
		Career.owl_careers.append(car)
		Career.careers.append(Career(car.career_id[0], car.career_name[0], skills))
		OntologyInteraction.ontology.save(ontology_file_name)
		OntologyInteraction.load_data()


