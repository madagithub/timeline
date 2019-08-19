import json
import csv

texts = {}
rows = []
with open('translate.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		rows.append(row)

languages = rows[0][1:]
for language in languages:
	print(language)
	texts[language] = {}

for row in rows[1:]:
	key = row[0]
	for i in range(1, len(row)):
		language = languages[i -1]
		texts[language][key] = row[i]

		if row[i].find('\u05b9') != -1:
			fixedText = ''
			lastChar = None
			for char in row[i]:
				if lastChar != '\u05b9':
					fixedText += char
				else:
					fixedText += char
				lastChar = char
			texts[language][key] = fixedText

dump = None
with open('config.json', 'r') as file:		
	config = json.load(file)
	config['texts'] = texts
	dump = json.dumps(config, sort_keys=True, indent=4)

with open('config.json', 'w') as file:
	file.write(dump)


