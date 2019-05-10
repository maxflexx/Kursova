from owlready2 import *
from career import *
from skill import *
from user import *
from sorter import *
import owlClasses as cl

ontology_file_name = "Ontology.owl"


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
				if len(individual.usesLanguage) != 0:
					language = individual.usesLanguage
				if len(language) == 0:
					language = individual.usesFramework
				Skill.skills.append(Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], language))
				s = OntologyInteraction.ontology.Skill(individual.name, individual.namespace)
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
		sync_reasoner_hermit()
		OntologyInteraction.get_data(OntologyInteraction.ontology)

	@staticmethod
	def delete_career(career_id):
		ind = list(OntologyInteraction.ontology.individuals())
		for i in ind:
			if len(i.career_id) != 0  and i.career_id[0] == career_id:
				destroy_entity(i)
			if len(i.wanted_career_id) != 0 and i.wanted_career_id[0] == career_id:
				destroy_entity(i)
		sync_reasoner_hermit()
		OntologyInteraction.ontology.save(ontology_file_name)
		OntologyInteraction.load_data()

	@staticmethod
	def create_new_vacancy(career_name, skill_ids):
		skills = []
		sync_reasoner_hermit()
		for i in skill_ids:
			skills.append(Skill.get_owl_skill(i))
		car = OntologyInteraction.ontology.Career()
		car.requireSkill = skills
		car.career_id = [Career.generate_career_id()]
		car.career_name = [career_name]
		OntologyInteraction.ontology.save(ontology_file_name)
		new_career = OntologyInteraction.get_vacancy_by_id_after_sync(car.career_id[0])
		Career.owl_careers.append(new_career)
		Career.careers.append(Career(new_career.career_id[0], new_career.career_name[0], new_career.requireSkill))
		OntologyInteraction.load_data()

	@staticmethod
	def create_new_skill(skill_name, uses_id):
		uses = []
		for i in uses_id:
			uses.append(Skill.get_owl_skill(i))
		skill = OntologyInteraction.ontology.Skill(usesLanguage=uses)
		skill.skill_name = [skill_name]
		skill.skill_id = [Skill.generate_id()]
		OntologyInteraction.ontology.save(ontology_file_name)
		new_skill = OntologyInteraction.get_skill_by_id_after_sync(skill.skill_id[0])
		Skill.skills.append(Skill(new_skill.is_a[0].name, new_skill.skill_id[0], new_skill.skill_name[0], new_skill.usesLanguage))
		Skill.owl_skills.append(new_skill)
		OntologyInteraction.load_data()
		return skill.skill_id[0]

	@staticmethod
	def create_new_user(first_name, last_name, career_id, skill_ids):
		skills = []
		for i in skill_ids:
			skills.append(Skill.get_owl_skill(i))
		user = OntologyInteraction.ontology.User()
		user.user_id = [User.generate_id()]
		user.total_skill_weight = [0]
		user.wanted_career_id = [career_id]
		user.first_name = [first_name]
		user.last_name = [last_name]
		user.hasSkill = skills
		OntologyInteraction.ontology.save(ontology_file_name)
		new_user = OntologyInteraction.get_user_by_id_after_sync(user.user_id[0])
		User.users.append(User(new_user.user_id[0], new_user.first_name[0], new_user.last_name[0], new_user.wanted_career_id[0], new_user.hasSkill))
		User.owl_users.append(new_user)
		OntologyInteraction.load_data()

	@staticmethod
	def get_skill_by_id_after_sync(skill_id):
		sync_reasoner_hermit()
		skills = list(OntologyInteraction.ontology.individuals())
		for s in skills:
			if s.skill_id != None and len(s.skill_id) != 0 and s.skill_id[0] == skill_id:
				return s
		return None

	@staticmethod
	def get_vacancy_by_id_after_sync(career_id):
		sync_reasoner_hermit()
		career = list(OntologyInteraction.ontology.individuals())
		for c in career:
			if c.career_id != None and len(c.career_id) != 0 and c.career_id[0] != None and c.career_id[0] == career_id:
				return c
		return None

	@staticmethod
	def get_user_by_id_after_sync(user_id):
		sync_reasoner_hermit()
		users = list(OntologyInteraction.ontology.individuals())
		for u in users:
			if u.user_id != None and len(u.user_id) != 0 and u.user_id[0] != None and u.user_id[0] == user_id:
				return u
		return None

