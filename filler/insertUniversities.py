from ontology import ontologyInteraction

ontologyInteraction.OntologyInteraction.load_data()

file = open("../getData/universities.txt")
universities = file.read().split('\n')
for u in universities:
	ontologyInteraction.OntologyInteraction.create_university(u.strip().replace("'", '').replace('"', '').lower())

ontologyInteraction.OntologyInteraction.load_data()