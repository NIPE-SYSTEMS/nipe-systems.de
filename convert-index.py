#!/usr/bin/env python3

import os
import datetime
import sys
import hashlib
import itertools
import collections

def retrieve_project(project_dir, project):
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
	with open("{}/{}/id".format(project_dir, project)) as f:
		uuid = f.read().strip()
	return {
		"name": project,
		"id": uuid,
		"text": os.path.exists("{}/{}/text.md".format(project_dir, project)),
		"tags": list(sorted(tags, key=lambda t: t["type"]))
	}

def retrieve_trigger(project_dir, trigger_dir, timestamp):
	project = os.path.relpath(os.path.realpath("{}/{}".format(trigger_dir, timestamp)), start=os.path.join(os.getcwd(), project_dir))
	now = datetime.datetime.now()
	timestamp_obj = datetime.datetime.fromtimestamp(float(timestamp))
	later = timestamp_obj.year != now.year
	label = [ "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC" ][timestamp_obj.month - 1] + "//" + str(timestamp_obj.year)[2:4] if timestamp_obj.year == now.year else str(timestamp_obj.year)
	with open("{}/{}/id".format(trigger_dir, timestamp)) as f:
		uuid = f.read().strip()
	return {
		"project": project,
		"timestamp": timestamp,
		"timestamp_obj": timestamp_obj,
		"later": later,
		"label": label,
		"id": uuid,
		"text": os.path.exists("{}/{}/text.md".format(trigger_dir, timestamp))
	}

def retrieve_structure(project_dir, trigger_dir):
	projects = [ retrieve_project(project_dir, p) for p in sorted(os.listdir(project_dir)) ]
	projects_grouped = { first_letter: list(projects) for first_letter, projects in itertools.groupby(projects, key=lambda p: p["name"][0].upper()) }
	
	atoz_left = { k: v for k, v in projects_grouped.items() if k < "N" }
	atoz_right = { k: v for k, v in projects_grouped.items() if k >= "N" }
	
	triggers = [ retrieve_trigger(project_dir, trigger_dir, t) for t in sorted(os.listdir(trigger_dir), reverse=True) ]
	triggers_recent = [ t for t in triggers if not t["later"] ]
	triggers_later = [ t for t in triggers if t["later"] ]
	
	def filter_duplicate_triggers(triggers):
		triggers = list(triggers)
		d = { t["project"]: t for t in triggers }
		return list(d.values())
	
	bytime_recent = { label: filter_duplicate_triggers(triggers) for label, triggers in itertools.groupby(triggers_recent, key=lambda t: t["label"]) }
	
	bytime_later = {}
	for label, triggers in itertools.groupby(triggers_later, key=lambda t: t["label"]):
		triggers = list(triggers)
		d = { t["project"]: t for t in triggers }
		counter = collections.Counter()
		for t in list(triggers):
			counter[t["project"]] += 1
		bytime_later[label] = [ d[project] for project in list(zip(*counter.most_common(7)))[0] ] + [ { "project": "...", "text": False } ]
	
	return {
		"atoz_left": atoz_left,
		"atoz_right": atoz_right,
		"bytime_recent": bytime_recent,
		"bytime_later": bytime_later
	}

def render_from_template(project_dir, trigger_dir, template_file, output_file):
	structure = retrieve_structure(project_dir, trigger_dir)
	
	for label, projects in structure["bytime_recent"].items():
		for project in projects:
			project.update({ "last": False, "beforeyear": False })
		projects[-1].update({ "last": True })
	
	for label, projects in structure["bytime_later"].items():
		for project in projects:
			project.update({ "last": False, "beforeyear": False })
		projects[-1].update({ "last": True })
	
	if len(structure["bytime_later"]) > 0:
		structure["bytime_recent"][list(structure["bytime_recent"].keys())[-1]].append({
			"project": "",
			"text": False,
			"last": True,
			"beforeyear": True
		})
	
	def render_timeline_project(project):
		last = " last" if project["last"] and not project["beforeyear"] else ""
		beforeyear = " beforeyear" if project["beforeyear"] else ""
		link_pre = "<a href=\"/{}.html\">".format(project["id"]) if project["text"] else ""
		link_post = "</a>" if project["text"] else ""
		return "\t\t\t<p class=\"timeline{}{}\">{}{}{}</p>\n".format(last, beforeyear, link_pre, project["project"], link_post)
	
	def render_timeline_time(label):
		return "\t\t\t<time>{}</time>\n".format(label)
	
	structure["bytime_recent"] = { render_timeline_time(label): "".join([ render_timeline_project(project) for project in projects ]) for label, projects in structure["bytime_recent"].items() }
	structure["bytime_recent"] = "".join([ label + projects for label, projects in structure["bytime_recent"].items() ])
	
	structure["bytime_later"] = { render_timeline_time(label): "".join([ render_timeline_project(project) for project in projects ]) for label, projects in structure["bytime_later"].items() }
	structure["bytime_later"] = "".join([ label + projects for label, projects in structure["bytime_later"].items() ])
	
	for label, projects in structure["atoz_left"].items():
		for project in projects:
			project.update({ "last": False })
		projects[-1].update({ "last": True })
	
	for label, projects in structure["atoz_right"].items():
		for project in projects:
			project.update({ "last": False })
		projects[-1].update({ "last": True })
	
	def render_project_tags(tags):
		return "".join([ "<span title=\"{}\">{}</span>".format(tag["description"], tag["label"]) for tag in tags ])
	
	def render_project_project(project):
		last = " last" if project["last"] else ""
		link_pre = "<a href=\"/{}.html\">".format(project["id"]) if project["text"] else ""
		link_post = "</a>" if project["text"] else ""
		return "\t\t\t<p class=\"project{}\">{}{}{}\n\t\t\t\t{}\n\t\t\t</p>\n".format(last, link_pre, project["name"], link_post, render_project_tags(project["tags"]))
	
	def render_project_label(label):
		return "\t\t\t<aside>{}</aside>\n".format(label)
	
	structure["atoz_left"] = { render_project_label(label): "".join([ render_project_project(project) for project in projects ]) for label, projects in structure["atoz_left"].items() }
	structure["atoz_left"] = "".join([ label + projects for label, projects in structure["atoz_left"].items() ])
	
	structure["atoz_right"] = { render_project_label(label): "".join([ render_project_project(project) for project in projects ]) for label, projects in structure["atoz_right"].items() }
	structure["atoz_right"] = "".join([ label + projects for label, projects in structure["atoz_right"].items() ])
	
	with open(template_file) as fin:
		contents = fin.read()
		with open(output_file, "w") as fout:
			fout.write(contents.replace("{{atozleft}}", structure["atoz_left"][:-1])
				.replace("{{atozright}}", structure["atoz_right"][:-1])
				.replace("{{bytimerecent}}", structure["bytime_recent"][:-1])
				.replace("{{bytimelater}}", structure["bytime_later"][:-1]))

if __name__ == "__main__":
	if len(sys.argv) != 4 + 1:
		print("Usage: {} PROJECT_DIRECTORY TRIGGER_DIRECTORY TEMPLATE_FILE OUTPUT_FILE".format(sys.argv[0]), file=sys.stderr)
		sys.exit(1)
	render_from_template(*tuple(sys.argv[1:]))
