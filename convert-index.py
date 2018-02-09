#!/usr/bin/env python3

import os
import datetime
import operator
import sys

def retrieve_structure(project_dir, trigger_dir):
	atozleft = {}
	atozright = {}
	projects = os.listdir(project_dir)
	first_letter = None
	for project in sorted(projects):
		if project[0].upper() < "N": # first letter belongs to left
			atoz = atozleft
		else: # first letter belongs to right
			atoz = atozright
		if first_letter != project[0].upper():
			first_letter = project[0].upper()
			atoz[first_letter] = []
		tags = []
		for tag_label in os.listdir("{}/{}/tags".format(project_dir, project)):
			tag = {
				"label": tag_label
			}
			with open("{}/{}/tags/{}/description".format(project_dir, project, tag_label)) as f:
				tag["description"] = f.read().strip()
			with open("{}/{}/tags/{}/type".format(project_dir, project, tag_label)) as f:
				tag["type"] = int(f.read().strip())
			tags.append(tag)
		atoz[first_letter].append({
			"name": project,
			"tags": tags
		})
	bytimerecent = {}
	bytimelater_ = {}
	triggers = os.listdir(trigger_dir)
	first_month = None
	for timestamp in sorted(triggers, reverse=True):
		project_name = os.path.relpath(
			os.path.realpath("{}/{}".format(trigger_dir, timestamp)),
			start=os.path.join(os.getcwd(), "projects"))
		now = datetime.datetime.now()
		timestamp_obj = datetime.datetime.fromtimestamp(float(timestamp))
		if timestamp_obj.year == now.year:
			label = [ "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
				"SEP", "OCT", "NOV", "DEC" ][timestamp_obj.month - 1] + "//" + str(timestamp_obj.year)[2:4]
			try:
				if project_name not in bytimerecent[label]:
					bytimerecent[label].append(project_name)
			except (KeyError, AttributeError):
				bytimerecent[label] = [ project_name ]
		else:
			label = str(timestamp_obj.year)
			try:
				bytimelater_[label][project_name] += 1
			except KeyError:
				try:
					bytimelater_[label][project_name] = 1
				except KeyError:
					bytimelater_[label] = {
						project_name: 1
					}
	bytimelater = {}
	for label, project_counts in bytimelater_.items():
		bytimelater[label] = [ p[0] for p in reversed(sorted(project_counts.items(), key=lambda p: p[1])) ][:7]
	return {
		"atozleft": atozleft,
		"atozright": atozright,
		"bytimerecent": bytimerecent,
		"bytimelater": bytimelater
	}

def replace_template(project_dir, trigger_dir, template_file, output_file):
	formatted = retrieve_structure(project_dir, trigger_dir)
	bytime_str = ""
	time_amount = len(formatted["bytimerecent"])
	for i, item in enumerate(formatted["bytimerecent"].items()):
		label, projects = item
		bytime_str += "			<time>" + label + "</time>\n"
		project_amount = len(projects)
		for j, project in enumerate(projects):
			bytime_str += "			<p class=\"timeline"
			if j + 1 == project_amount and i + 1 != time_amount:
				bytime_str += " last"
			bytime_str += "\">" + project + "</p>\n"
	if len(formatted["bytimelater"]) > 0:
		bytime_str += "			<p class=\"timeline beforeyear\"></p>\n"
	time_amount = len(formatted["bytimelater"])
	for i, item in enumerate(formatted["bytimelater"].items()):
		label, projects = item
		bytime_str += "			<time>" + label + "</time>\n"
		project_amount = len(projects)
		for j, project in enumerate(projects + [ "..." ]):
			bytime_str += "			<p class=\"timeline"
			if j + 1 == project_amount and i + 1 != time_amount:
				bytime_str += " last"
			bytime_str += "\">" + project + "</p>\n"
	
	atozleft_str = ""
	for first_letter, projects in sorted(formatted["atozleft"].items(), key=operator.itemgetter(0)):
		atozleft_str += "			<aside>" + first_letter + "</aside>\n"
		project_amount = len(projects)
		for i, project in enumerate(projects):
			atozleft_str += "			<p class=\"project"
			if i + 1 == project_amount:
				atozleft_str += " last"
			atozleft_str += "\">" + project["name"] + " "
			for tag in sorted(project["tags"], key=operator.itemgetter("type", "label")):
				atozleft_str += "<span class=\"" + str(tag["type"]) + "\" title=\"" + tag["description"] + "\">" + tag["label"] + "</span>"
			atozleft_str += "</p>\n"
	atozright_str = ""
	for first_letter, projects in sorted(formatted["atozright"].items(), key=operator.itemgetter(0)):
		atozright_str += "			<aside>" + first_letter + "</aside>\n"
		project_amount = len(projects)
		for i, project in enumerate(projects):
			atozright_str += "			<p class=\"project"
			if i + 1 == project_amount:
				atozright_str += " last"
			atozright_str += "\">" + project["name"] + " "
			for tag in sorted(project["tags"], key=operator.itemgetter("type", "label")):
				atozright_str += "<span class=\"" + str(tag["type"]) + "\" title=\"" + tag["description"] + "\">" + tag["label"] + "</span>"
			atozright_str += "</p>\n"
	with open(template_file) as fin:
		contents = fin.read()
		with open(output_file, "w") as fout:
			fout.write(contents.replace("{{atozleft}}", atozleft_str[:-1])
				.replace("{{atozright}}", atozright_str[:-1])
				.replace("{{bytime}}", bytime_str[:-1]))

if __name__ == "__main__":
	if len(sys.argv) != 4 + 1:
		print("Usage: {} PROJECT_DIRECTORY TRIGGER_DIRECTORY TEMPLATE_FILE OUTPUT_FILE".format(sys.argv[0]), file=sys.stderr)
		sys.exit(1)
	replace_template(*tuple(sys.argv[1:]))
