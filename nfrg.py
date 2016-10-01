#! /usr/bin/env python

import argparse, logging, os, datetime, errno

from feedgen.feed import FeedGenerator

def build_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--title', required=True, metavar='TITLE')
	parser.add_argument('-u', '--base-url', required=True, metavar='URL')
	parser.add_argument('-d', '--description', required=True, metavar='DESC')
	parser.add_argument('-r', '--recursive', action='store_true')
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
				logging.debug('Found files : %s', files)
				for file in files:
					yield os.path.join(root, file)
		elif os.path.isfile(candidate):
			yield candidate
		else:
			logging.warn('%s is not a directory nor a regular file, ignoring it', candidate)

if __name__ == '__main__':
	args = build_arguments()
	logging.basicConfig(level=getattr(logging, args.log.upper()))
	args.base_url = args.base_url.rstrip("/")
	logging.debug(args)
	files = build_entries(args.file)
	fg = FeedGenerator()
	fg.link(href=args.base_url, rel='alternate')
	fg.description(args.description)
	fg.title(args.title)
	for file in files:
		logging.debug('Create entry for ''%s''', file)
		try:
			t = os.path.getmtime(file)
			dt = datetime.datetime.utcfromtimestamp(int(t))
			dts = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
			url = "%s/%s" % (args.base_url, file)
		except OSError as e:
			logging.warn('Skipped entry ''%s'' due to %s', file, e)
			continue
		fe = fg.add_entry()
		fe.id(url)
		fe.link(href=url)
		fe.title(os.path.basename(file))
		fe.published(dts)
	print fg.rss_str(pretty=True)
