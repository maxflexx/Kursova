import textract
import nltk
from nltk.corpus import stopwords
import re
import time
from ontology import ontologyInteraction

ontologyInteraction.OntologyInteraction.load_data()

lemmatizer = nltk.WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
noun_tags = ["NN", "NNS", "NNP", "NNPS", "FW"]
adjective_tags = ["JJ", "JJR", "JJS"]
adverb_tags = ["RB", "RBR", "RBS"]


def tokenize_words(text):
	return nltk.word_tokenize(text)


def pos_tag(tokenized_words):
	return nltk.pos_tag(tokenized_words)


def find_all_emails(text:str):
	res = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
	for email in res:
		text = text.replace(email, '')
	return [res, text]


def find_all_phones(text):
	res = re.findall(r"^(?:\+38)?(?:\(044\)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|044[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|044[0-9]{7})$", text)
	for phone in res:
		text = text.replace(phone, '')
	return [res, text]


def find_all_links(text):
	res = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
	for link in res:
		text = text.replace(link, '')
	return [res, text]


def erase_redundant_data(text):
	text = text.replace('(', ' ').replace(')', ' ').replace('/', ', ').replace('\\', ', ')
	tokens = text.split(' ')
	t = [w for w in tokens if w not in stop_words]
	return " ".join(t)


def lemmatize_word(word):
	return lemmatizer.lemmatize(word)


def lemmatize_words(text:str):
	text = text.lower().split(' ')
	res = ""
	for word in text:
		lemm_word = lemmatize_word(word)
		lemm_word = lemm_word.lower().strip().replace('.', '').replace(',', '')
		res += lemm_word + " "
	return res.strip()


def noun_only(p):
	return p in noun_tags or p == "FW"


def noun_adverbs(p):
	return p in noun_tags or p == "FW" or p in adverb_tags


def get_instances(part_of_speech_tags, hasToBeWritten):
	res = []
	indexes = []
	temp_res = dict()
	for i in range(len(part_of_speech_tags)):
		p = part_of_speech_tags[i]
		if hasToBeWritten(p[1]) and len(p[0]) > 1:
			temp_res[i] = p[0]
		else:
			t = []
			for k in temp_res.keys():
				indexes.append(k)
				t.append(temp_res[k])
			if len(t) > 0:
				res.append(t)
			temp_res = dict()
	return res, indexes


def merge_indexes(index1, index2):
	res = []
	iterFor1 = 0
	iterFor2 = 0
	while iterFor1 < len(index1) and iterFor2 < len(index2):
		if iterFor1 < len(index1) and (iterFor2 >= len(index2) or index1[iterFor1] < index2[iterFor2]):
			res.append(index1[iterFor1])
			iterFor1 += 1
		elif iterFor2 < len(index2):
			res.append(index2[iterFor2])
			iterFor2 += 1
	return res


def filter_by_indexes(indexes, part_of_speech_tags):
	res = dict()
	for key in part_of_speech_tags:
		index = part_of_speech_tags.index(key)
		if index not in indexes:
			res[key[0]] = key[1]
	return res

def get_by_indexes(indexes, part_of_speech_tags):
	res = dict()
	for key in part_of_speech_tags:
		index = part_of_speech_tags.index(key)
		if index in indexes:
			res[key[0]] = key[1]
	return res



def analyze_resume(part_of_speech_tags):
	noun_classes, noun_indexes = get_instances(part_of_speech_tags, noun_only)
	mix_classes, mix_indexes = get_instances(part_of_speech_tags, noun_adverbs)
	merged_indexes = merge_indexes(noun_indexes, mix_indexes)
	unclassified = filter_by_indexes(merged_indexes, part_of_speech_tags)
	classified = get_by_indexes(merged_indexes, part_of_speech_tags)
	return unclassified, classified


def find_all_universities(text:str):
	universities = []
	university_ids = []
	uu = []
	text = text.replace('"', '').replace("'", '').replace('-', ' ').replace('”', '').replace('“', '')
	for u in ontologyInteraction.University.universities:
		name = u.university_name.replace('"', '').replace("'", '').replace('-', ' ').replace('”', '').replace('“', '').strip()
		uu.append(name)
		if name in text:
			universities.append(name)
			university_ids.append(u.university_id)

	for u in universities:
		text = text.replace(u, '')
	return university_ids, universities, text


def find_all_companies(text:str):
	companies = []
	cp = []
	text = text.replace('"', '').replace("'", '').replace('-', ' ').replace('”', '').replace('“', '')
	for c in ontologyInteraction.Company.companies:
		name = c.company_name.replace('"', '').replace("'", '').replace('-', ' ').replace('”', '').replace('“',
																											  '').strip()
		cp.append(name)
		if name in text:
			companies.append(name)

	for c in companies:
		text = text.replace(c, '')
	return companies, text


def find_all_skills(text:str):
	skills = []
	skills_ids = []
	sk = []
	text = text.replace('"', '').replace("'", '').replace('-', ' ').replace('”', '').replace('“', '')
	for s in ontologyInteraction.Skill.skills:
		name = s.skillName.replace('"', '').replace("'", '').replace('-', ' ').replace('”', '').replace('“', '').strip().lower()
		sk.append(name)
		if name in text:
			skills.append(name)
			skills_ids.append(s.skillId)

	for u in skills:
		text = text.replace(u, '')
	return skills_ids, skills, text


def analyze(file, career_id):
	start_time = time.time()
	text = textract.process(file, method='pdfminer')
	#text = textract.process(file, method='docx')
	s = text.decode('utf-8')
	s = s.replace("\\t", "").replace('\\xc2', '').replace('\\xb7', '').replace('\t', ' ')
	emails, text = find_all_emails(s)
	phones, text = find_all_phones(text)
	links, text = find_all_links(text)
	university_ids, universities, text = find_all_universities(text.lower())
	#companies, text = find_all_companies(text.lower())
	skill_ids, skills, text = find_all_skills(text.lower())
	text = erase_redundant_data(text)
	text = lemmatize_words(text)

	tokens = tokenize_words(text)
	poss = pos_tag(tokens)
	unclassified, classified = analyze_resume(poss)
	candidate_terms = [i for i in classified.keys()]
	ontologyInteraction.OntologyInteraction.create_resume(emails, phones, links, university_ids, skill_ids, candidate_terms, career_id, file)
	# print("emails")
	# for e in emails:
	# 	print(e)
	# print("PHONES")
	# for p in phones:
	# 	print(p)
	# print("LINKS")
	# for l in links:
	# 	print(l)
	# print("UNIVERSITIES")
	# for u in universities:
	# 	print(u)
	# # print("companies")
	# # for c in companies:
	# # 	print(c)
	# print("SKILLS")
	# for s in skills:
	# 	print(s)
	# print("CANDIDATES for terms")
	# for c in classified:
	# 	print(c)
	# print("REDUNDANT data")
	# for r in unclassified:
	# 	print(r)
	# # for p in poss:
	# # 	print (str(p[0]) + " : " + str(p[1]))
	print(time.time() - start_time)


