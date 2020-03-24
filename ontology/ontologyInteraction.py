from owlready2 import *
from ontology.sorter import *
from ontology.company import *
from ontology.university import *
from ontology.resume import *
ontology_file_name = "Ontology.owl"


class OntologyInteraction:

	ontology = get_ontology("file://" + ontology_file_name).load()
	universityId = 1
	companyId = 1
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
			if individual.is_a[0].name == "University":
				University.universities.append(University(individual.university_id[0], individual.universityName[0]))
				u = OntologyInteraction.ontology.University(individual.name, individual.namespace)
				University.owl_universities.append(u)
				continue
			if individual.is_a[0].name == "Company":
				Company.companies.append(Company(individual.company_id[0], individual.companyName[0]))
				c = OntologyInteraction.ontology.Company(individual.name, individual.namespace)
				Company.owl_companies.append(c)
				continue
			if individual.is_a[0].name == "Resume":
				emails = []
				links = []
				phones = []
				skills = []
				universities = []
				candidate_terms = []
				for skill in individual.resumeHasSkill:
					language = []
					if len(individual.usesLanguage) != 0:
						language = individual.usesLanguage
					if len(language) == 0:
						language = individual.usesFramework
					skills.append(Skill(skill.is_a[0].name, skill.skill_id[0], skill.skill_name[0], language))
				for university in individual.educatedAt:
					universities.append(University(university.university_id[0], university.universityName[0]))
				if hasattr(individual, "resume_email"):
					emails = individual.resume_email
				if hasattr(individual, "resume_link"):
					links = individual.resume_link
				if hasattr(individual, "resume_phone"):
					phones = individual.resume_phone
				if hasattr(individual, "resume_candidate_term"):
					candidate_terms = individual.resume_candidate_term
				Resume.resumes.append(Resume(individual.resume_id[0], individual.resume_file_name[0], individual.resume_career_id[0], emails, links, phones, candidate_terms, universities, skills))
				r = OntologyInteraction.ontology.Resume(individual.name, individual.namespace)
				Resume.owl_resumes.append(r)
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
	def create_resume(emails, phones, links, university_ids, skill_ids, candidate_terms, career_id, resume_file_name):
		skills = []
		for i in skill_ids:
			skills.append(Skill.get_owl_skill(i))
		universities = []
		for i in university_ids:
			universities.append(University.get_owl_university_by_id(i))

		resume = OntologyInteraction.ontology.Resume()
		resume.resume_id = [Resume.generate_id()]
		resume.resume_career_id = [career_id]
		resume.resume_file_name = [resume_file_name]
		resume.resumeHasSkill = skills
		resume.educatedAt = universities
		resume.resume_email = emails
		resume.resume_phone = phones
		resume.resume_link = links
		resume.resume_candidate_term = candidate_terms
		OntologyInteraction.ontology.save(ontology_file_name)
		new_resume = OntologyInteraction.get_resume_by_id_after_sync(resume.resume_id[0])
		Resume.resumes.append(
			Resume(new_resume.resume_id[0],
				   resume.resume_file_name[0],
				   resume.resume_career_id[0],
				   resume.resume_email,
				   resume.resume_link,
				   resume.resume_phone,
				   resume.resume_candidate_term,
				   resume.educatedAt,
				   resume.resumeHasSkill))
		Resume.owl_resumes.append(new_resume)
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

	@staticmethod
	def get_resume_by_id_after_sync(resume_id):
		sync_reasoner_hermit()
		resumes = list(OntologyInteraction.ontology.individuals())
		for u in resumes:
			if u.resume_id != None and len(u.resume_id) != 0 and u.resume_id[0] != None and u.resume_id[0] == resume_id:
				return u
		return None

	# Kursova 2
	@staticmethod
	def create_university(name:str):
		university = OntologyInteraction.ontology.University()
		university.universityName = [name]
		university.university_id = [OntologyInteraction.universityId]
		OntologyInteraction.universityId += 1
		OntologyInteraction.ontology.save(ontology_file_name)

	@staticmethod
	def create_company(name: str):
		company = OntologyInteraction.ontology.Company()
		company.companyName = [name]
		company.company_id = [OntologyInteraction.companyId]
		OntologyInteraction.companyId += 1
		OntologyInteraction.ontology.save(ontology_file_name)



