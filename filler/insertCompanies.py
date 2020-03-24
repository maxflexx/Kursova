from ontology import ontologyInteraction

ontologyInteraction.OntologyInteraction.load_data()

file = open("../getData/companies.txt")
companies = file.read().split('\n')
for c in companies:
	ontologyInteraction.OntologyInteraction.create_company(c.strip().replace("'", '').replace('"', '').lower())

ontologyInteraction.OntologyInteraction.load_data()