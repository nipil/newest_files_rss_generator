#! /usr/bin/env python

import argparse, logging, os, datetime

from feedgen.feed import FeedGenerator

def build_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--title', required=True, metavar='TITLE')
	parser.add_argument('-u', '--base-url', required=True, metavar='URL')
	parser.add_argument('-d', '--description', required=True, metavar='DESC')
	parser.add_argument('-r', '--recursive', action='store_true')
	parser.add_argument('-n', '--number', metavar='N', type=int)
	parser.add_argument('-o', '--output', metavar='OUTPUT')
	parser.add_argument('-l', '--log', choices=['debug', 'info', 'warning', 'error', 'critical'], default='warning')
	parser.add_argument('file', nargs='+')
	return parser.parse_args()

def build_entries(candidates):
	for candidate in candidates:
		logging.debug('Processing %s', candidate)
		if os.path.isdir(candidate):
			logging.debug('Candidate %s is a directory', candidate)
			if not args.recursive:
				logging.warn('Ignoring directory ''%s'' (recursion disabled)', candidate)
				continue
			logging.info('Walking ''%s'' recursively', candidate)
			for root, dirs, files in os.walk(candidate):
				logging.debug('Directory %s has files : %s', root, files)
				for file in files:
					yield os.path.join(root, file)
		elif os.path.isfile(candidate):
			yield candidate
		else:
			logging.warn('%s is not a directory nor a regular file, ignoring it', candidate)

def entry_cmp(a, b):
	logging.error("a=%s b=%s", a, b)
	return a["t"] - b["t"]

if __name__ == '__main__':

	# setup
	args = build_arguments()
	logging.basicConfig(level=getattr(logging, args.log.upper()))
	args.base_url = args.base_url.rstrip("/")
	logging.debug(args)
	files = build_entries(args.file)

	# process and sort
	kept = []
	for file in files:
		try:
			e = {
				"t": os.path.getmtime(file),
				"p": file
			}
		except OSError as e:
			logging.warn('Skipped entry ''%s'' due to %s', file, e)
			continue
		# manage maximum number of entries
		if args.number:
			if len(kept) < args.number:
				logging.debug("Adding entry %s", e)
				kept.append(e)
			else:
				kept.sort(key=lambda v: v["t"])
				if e["t"] > kept[0]["t"]:
					logging.debug("Replacing %s with newer %s", kept[0], e)
					kept[0] = e
		else:
			logging.debug("Adding entry %s", e)
			kept.append(e)
	kept.sort(reverse=True, key=lambda v: v["t"])

	# generate feed
	fg = FeedGenerator()
	fg.link(href=args.base_url, rel='alternate')
	fg.description(args.description)
	fg.title(args.title)
	for entry in kept:
		logging.debug('Create entry for ''%s''', entry["p"])
		dt = datetime.datetime.utcfromtimestamp(int(entry["t"]))
		dts = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
		url = "%s/%s" % (args.base_url, entry["p"])
		fe = fg.add_entry()
		fe.id(url)
		fe.link(href=url)
		fe.title(os.path.basename(entry["p"]))
		fe.published(dts)

	# output feed
	if args.output:
		fg.rss_file(args.output, pretty=True)
	else:
		print fg.rss_str(pretty=True)
