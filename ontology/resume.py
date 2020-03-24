from ontology.skill import *
from ontology.university import *

class Resume:
	resumes = []
	owl_resumes = []

	def __init__(self, resume_id, resume_file_name, career_id, emails, links, phones, candidate_terms, universities: [University], skills: [Skill]):
		self.id = resume_id
		self.file_name = resume_file_name
		self.career_id = career_id
		self.emails = emails
		self.links = links
		self.phones = phones
		self.universities = universities
		self.skills = skills
		self.candidate_terms = candidate_terms

	@staticmethod
	def generate_id():
		maxi = 0
		for s in Resume.resumes:
			if maxi < s.id:
				maxi = s.id
		return maxi + 1


	@staticmethod
	def format_output_string(arr, arr_name, each_element_name, offset_str):
		result = ""
		if len(arr) > 0:
			result += arr_name + '\n'
			for a in arr:
				result += offset_str + each_element_name + a + '\n'
		return result

	@staticmethod
	def resumes_out(resumes):
		res = ""
		if len(resumes) == 0:
			return "No resumes"
		k = 0
		for u in resumes:
			if k >= 10:
				break
			res += "Resume file name: " +u.file_name + "\n"
			res += Resume.format_output_string(u.emails, "Emails: ", "", "    ")
			res += Resume.format_output_string(u.links, "Links: ", "", "    ")
			res += Resume.format_output_string(u.phones, "Phones: ", "", "    ")

			if len(u.universities) > 0:
				res += "Universities: \n"
				for university in u.universities:
					res += university.university_name + '\n'
			if len(u.skills) > 0:
				res += "Skills: \n"
				for skill in u.skills:
					res += "       Skill name: " + skill.skillName + "\n"
			res += Resume.format_output_string(u.candidate_terms, "Candidate terms: ", "", "    ")
			res += "\n\n\n"
			k += 1
		return res
