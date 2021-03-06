import glob
import re
import os


dir_name = os.path.dirname(__file__)
regex = re.compile('[^.,;():?!"\'\s]+(?:\'[sd])?')
sentence_re = re.compile('[^.]+')
first_line = re.compile('^.*\r?\n')
cache = {}


def normalize_words(words):
	normalized = []
	for word in words:
		lower = word.lower()
		if lower == 'it\'s':
			normalized.append('it')
			normalized.append('is')
			continue
		if len(lower) > 2 and lower[-2] == '\'':
			if lower[-1] == 'd':
				normalized.append(lower[:-2])
				normalized.append('would')
				continue
			if lower[-1] == 's':
				lower = lower[:-2]
				if len(lower) == 0:
					continue
		normalized.append(lower)
	return normalized


def get_text_corpus(maxfiles=9223372036854775807, root_dir='texts', add_sentences=False):
	pattern = os.path.join(root_dir, '**/*.*')
	corpus = []
	files = 0
	for filename in glob.iglob(
		os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.normpath(pattern)),
		recursive=True
	):
		files += 1
		if files > maxfiles:
			break
		if filename in cache:
			corpus.append(cache[filename])
		else:
			all_text = open(filename, 'r').read()
			words = regex.findall(all_text)
			title_list = first_line.findall(all_text)
			if len(title_list) > 0:
				title = title_list[0].strip()
			else:
				title = ""

			by_sentence = []
			if add_sentences:
				sentences = sentence_re.findall(all_text)
				for sentence in sentences:
					by_sentence.append(normalize_words(regex.findall(sentence)))

			normalized_text = normalize_words(words)
			cache[filename] = {
				'title': title,
				'filename': filename,
				'text': normalized_text,
				'text_set': set(normalized_text),
				'by_sentence': by_sentence
			}
			corpus.append(cache[filename])
	return corpus
