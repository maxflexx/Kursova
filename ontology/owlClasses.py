from owlready2 import *

o = get_ontology("file://Ontology.owl").load()


class HumanLanguage(Thing):
	namespace = o


class Terms(Thing):
	namespace = o


class Company(Thing):
	namespace = o


class School(Thing):
	namespace = o


class University(Thing):
	namespace = o


class Resume(Thing):
	namespace = o


class Education(Resume):
	namespace = o


class Credentials(Resume):
	namespace = o


class WorkExperience(Resume):
	namespace = o


class Skill(Thing):
	namespace = o


class WebProgramming(Skill):
	pass


class Framework(WebProgramming):
	namespace = o


class Language(WebProgramming):
	namespace = o


class Technology(WebProgramming):
	namespace = o


class BackendFramework(Framework):
	namespace = o


class BackendLanguage(Language):
	namespace = o


class BackendTechnology(Technology):
	namespace = o


class Database(BackendTechnology):
	pass


class NonRelational(Database):
	namespace = o


class Relational(Database):
	namespace = o


class User(Thing):
	namespace = o


class FrontendFramework(Framework):
	namespace = o


class FrontendLanguage(Language):
	namespace = o


class FrontendTechnology(Technology):
	namespace = o


class usesLanguage(ObjectProperty):
	namespace = o
	domain = [Framework]
	range = [Language]


class usesFramework(ObjectProperty):
	namespace = o
	domain = [Language]
	range = [Framework]
	owl_inverse_property = usesLanguage
#
#
class skill_name(DataProperty):
	namespace = o
	domain = [Skill]
	range = [str]


class skill_id(DataProperty):
	namespace = o
	domain = [Skill]
	range = [int]


class Career(Thing):
	namespace = o


class career_name(DataProperty):
	namespace = o
	domain = [Career]
	range = [str]

#
class career_id(DataProperty):
	namespace = o
	domain = [Career]
	range = [int]


class requireSkill(ObjectProperty):
	namespace = o
	domain = [Career]
	range = [Skill]



