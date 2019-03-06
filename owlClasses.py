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



