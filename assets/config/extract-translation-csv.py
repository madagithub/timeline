import json
import csv

with open('config.json', 'r') as file:
	texts = json.load(file)['texts']
	languages = list(texts.keys())
	keyLanguage = languages[0]

	header = ['Key'] + [language for language in languages]
	rows = [header]

	for key in texts[keyLanguage].keys():
		row = []
		row.append(key)
		for language in languages:
			row.append(texts[language][key])

		rows.append(row)

	with open('translate.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(rows)


