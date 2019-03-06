from owlready2 import *

o = get_ontology("file://Kursova11.owl").load()


class Skill(Thing):
	namespace = o


class WebProgramming(Skill):
	pass


class Backend(WebProgramming):
	pass


class BackendFramework(Backend):
	namespace = o


class BackendLanguage(Backend):
	namespace = o


class BackendTechnology(Backend):
	namespace = o


class Database(Backend):
	pass


class NonRelational(Database):
	namespace = o


class Relational(Database):
	namespace = o


class User(Thing):
	namespace = o


# class usesLanguageBackend(Property):
# 	namespace = o
# 	domain = [BackendFramework]
# 	range = [BackendLanguage]
#
#
# class usesFrameworkBackend(Property):
# 	namespace = o
# 	domain = [BackendLanguage]
# 	range = [BackendFramework]
# 	owl_inverse_property = usesLanguageBackend


class Frontend(WebProgramming):
	pass


class FrontendFramework(Frontend):
	namespace = o


class FrontendLanguage(Frontend):
	namespace = o


class FrontendTechnology(Frontend):
	namespace = o


# class usesLanguageFrontend(Property):
# 	namespace = o
# 	domain = [FrontendFramework]
# 	range = [FrontendLanguage]
#
#
# class usesFrameworkFrontend(Property):
# 	namespace = o
# 	domain = [FrontendLanguage]
# 	range = [FrontendFramework]
# 	owl_inverse_property = usesLanguageFrontend
#
#
# class skill_name(Property):
# 	namespace = o
# 	domain = [Skill]
# 	range = [str]
#
#
# class skill_id(Property):
# 	namespace = o
# 	domain = [Skill]
# 	range = [int]


class Career(Thing):
	namespace = o


# class career_name(Property):
# 	namespace = o
# 	domain = [Career]
# 	range = [str]
#
#
# class careerid(Property):
# 	namespace = o
# 	domain = [Career]
# 	range = [int]
#
#
# class requireSkill(Property):
# 	namespace = o
# 	domain = [Career]
# 	range = [Skill]


def group_individuals(individuals):
	for i in range(len(individuals)):
		individual = individuals[i]
		print(Career.is_a)
		if individual.is_a[0].name == "Career":
			#Career.careers.append(Career(individual.career_id[0], individual.career_name[0], individual.requireSkill))
			ca = o.Career(individual.name, individual.namespace)
			c = o.Career()
			c.career_name = [individual.career_name[0]]
			c.career_id = [individual.career_id[0]]
			c.requireSkill = individual.requireSkill
			continue
		#if individual.is_a[0].name == User.ontologyName:
			#User.users.append(User(individual.user_id[0], individual.first_name[0], individual.last_name[0],
			#					   individual.wanted_career_id[0], individual.hasSkill))

		#	continue
		else:
			continue
			language = []
			if hasattr(individual, 'usesLanguageFrontend'):
				language = individual.usesLanguageFrontend
			if len(language) == 0:
				language = individual.usesLanguageBackend
			#Skill.skills.append(
			#	Skill(individual.is_a[0].name, individual.skill_id[0], individual.skill_name[0], language))


def get_data(onto):
	c = onto.Career()
	ind = onto.individuals()
	c = onto.classes()
	o = onto.data_properties()
	d = onto.properties()
	individuals = []
	data_prop = []
	classes = []
	prop = []
	for i in ind:
		individuals.append(i)
	for i in c:
		classes.append(i)
	for i in o:
		data_prop.append(i)
	for i in d:
		prop.append(i)
	group_individuals(individuals)


#get_data(o)


