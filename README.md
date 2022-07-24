# OBSOLETE

This repository has been archived and will not be updated anymore.

# newest_files_rss_generator

Generates an rss feed listing files based on their modification time

# install

- install the `virtualenv` package of your linux distribution
- clone this repo
- go to cloned folder
- initialize local environment : `virtualenv env`
- install requirements locally : `env/bin/pip install -r requirements.txt`

# run

- go to folder where you will reference files to be aggregated
- run `path_to_newest_files_rss_generator/{env/bin/python,nfrg.py} ... `

# usage and options

nfrg.py [OPTIONS] file [file ...]

`-h` displays help

`file` : a path relative to the current working directory. This **relative** path will be added to the base url when building links for feed entry

`-t TITLE` : add a title to the rss feed

`-d DESC` : add a description to the rss feed

`-u URL` : use URL as base url for links

`-r` : enable recursion (disabled by default)

`-n N` : limit number of feed entry *to the N newest* files found

`-o OUTPUT` : write RSS XML feed to file instead of stdandard output

`-l level` : debugging level

# examples

Considering this structure from the current working directory :

    $ find -type f | xargs ls --full-time
    -rw-rw-r-- 1 nipil nipil 0 2016-10-02 12:22:03.910455320 +0200 a/10
    -rw-rw-r-- 1 nipil nipil 0 2016-10-02 12:22:14.350432165 +0200 a/11
    -rw-rw-r-- 1 nipil nipil 0 2016-10-02 12:22:16.734426879 +0200 a/12
    -rw-rw-r-- 1 nipil nipil 0 2016-10-02 12:22:19.218421374 +0200 a/13
    -rw-rw-r-- 1 nipil nipil 0 2016-10-02 12:21:33.814522300 +0200 a/b/1
    -rw-rw-r-- 1 nipil nipil 0 2016-10-02 12:21:47.638491492 +0200 a/b/2
    -rw-rw-r-- 1 nipil nipil 0 2016-10-02 12:21:40.366507694 +0200 a/b/3

## provide a directory

If recursion is not enabled, the generator will **not** go into the directory. As a consequence no files from `a` (nor `b`) is listed.

    $ path_to_newest_files_rss_generator/{env/bin/python,nfrg.py}
      -t title -u http://example.com/ -d description a

    WARNING:root:Ignoring directory a (recursion disabled)

    <?xml version='1.0' encoding='UTF-8'?>
    <rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
      <channel>
        <title>title</title>
        <link>http://example.com</link>
        <description>description</description>
        <docs>http://www.rssboard.org/rss-specification</docs>
        <generator>python-feedgen</generator>
        <lastBuildDate>Sun, 02 Oct 2016 10:26:44 +0000</lastBuildDate>
      </channel>
    </rss>

## provide the content of a directory

By providing the content of the directory, files found there are processed, but again, subdirectories are not processed if recursion is disabled. As a result, only files in `a` are listed while files in `b` are not.

    $ path_to_newest_files_rss_generator/{env/bin/python,nfrg.py}
        -t title -u http://example.com/ -d description a/*

    WARNING:root:Ignoring directory a/b (recursion disabled)
    
    <?xml version='1.0' encoding='UTF-8'?>
    <rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
      <channel>
        <title>title</title>
        <link>http://example.com</link>
        <description>description</description>
        <docs>http://www.rssboard.org/rss-specification</docs>
        <generator>python-feedgen</generator>
        <lastBuildDate>Sun, 02 Oct 2016 10:26:54 +0000</lastBuildDate>
        <item>
          <title>13</title>
          <link>http://example.com/a/13</link>
          <guid isPermaLink="false">http://example.com/a/13</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:19 +0000</pubDate>
        </item>
        <item>
          <title>12</title>
          <link>http://example.com/a/12</link>
          <guid isPermaLink="false">http://example.com/a/12</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:16 +0000</pubDate>
        </item>
        <item>
          <title>11</title>
          <link>http://example.com/a/11</link>
          <guid isPermaLink="false">http://example.com/a/11</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:14 +0000</pubDate>
        </item>
        <item>
          <title>10</title>
          <link>http://example.com/a/10</link>
          <guid isPermaLink="false">http://example.com/a/10</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:03 +0000</pubDate>
        </item>
      </channel>
    </rss>

## provide a directory with recursion enabled

Recursion enables going to any depth to find files. Here, files in `a` and `b` are listed.

    $ path_to_newest_files_rss_generator/{env/bin/python,nfrg.py}
        -t title -u http://example.com/ -d description -r a

    <?xml version='1.0' encoding='UTF-8'?>
    <rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
      <channel>
        <title>title</title>
        <link>http://example.com</link>
        <description>description</description>
        <docs>http://www.rssboard.org/rss-specification</docs>
        <generator>python-feedgen</generator>
        <lastBuildDate>Sun, 02 Oct 2016 10:27:12 +0000</lastBuildDate>
        <item>
          <title>13</title>
          <link>http://example.com/a/13</link>
          <guid isPermaLink="false">http://example.com/a/13</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:19 +0000</pubDate>
        </item>
        <item>
          <title>12</title>
          <link>http://example.com/a/12</link>
          <guid isPermaLink="false">http://example.com/a/12</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:16 +0000</pubDate>
        </item>
        <item>
          <title>11</title>
          <link>http://example.com/a/11</link>
          <guid isPermaLink="false">http://example.com/a/11</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:14 +0000</pubDate>
        </item>
        <item>
          <title>10</title>
          <link>http://example.com/a/10</link>
          <guid isPermaLink="false">http://example.com/a/10</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:03 +0000</pubDate>
        </item>
        <item>
          <title>2</title>
          <link>http://example.com/a/b/2</link>
          <guid isPermaLink="false">http://example.com/a/b/2</guid>
          <pubDate>Sun, 02 Oct 2016 10:21:47 +0000</pubDate>
        </item>
        <item>
          <title>3</title>
          <link>http://example.com/a/b/3</link>
          <guid isPermaLink="false">http://example.com/a/b/3</guid>
          <pubDate>Sun, 02 Oct 2016 10:21:40 +0000</pubDate>
        </item>
        <item>
          <title>1</title>
          <link>http://example.com/a/b/1</link>
          <guid isPermaLink="false">http://example.com/a/b/1</guid>
          <pubDate>Sun, 02 Oct 2016 10:21:33 +0000</pubDate>
        </item>
      </channel>
    </rss>

## providing a limit to the number of entries

If you provide a maximum number of entries, only the N newest entries will be listed. Here, with `-n 3`, the file `10` in `a` and the files in `b` will not be listed, as they are not among the 3 newest files.

    $ path_to_newest_files_rss_generator/{env/bin/python,nfrg.py}
        -t title -u http://example.com/ -d description a -r -n 3

    <?xml version='1.0' encoding='UTF-8'?>
    <rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
      <channel>
        <title>title</title>
        <link>http://example.com</link>
        <description>description</description>
        <docs>http://www.rssboard.org/rss-specification</docs>
        <generator>python-feedgen</generator>
        <lastBuildDate>Sun, 02 Oct 2016 10:27:44 +0000</lastBuildDate>
        <item>
          <title>13</title>
          <link>http://example.com/a/13</link>
          <guid isPermaLink="false">http://example.com/a/13</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:19 +0000</pubDate>
        </item>
        <item>
          <title>12</title>
          <link>http://example.com/a/12</link>
          <guid isPermaLink="false">http://example.com/a/12</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:16 +0000</pubDate>
        </item>
        <item>
          <title>11</title>
          <link>http://example.com/a/11</link>
          <guid isPermaLink="false">http://example.com/a/11</guid>
          <pubDate>Sun, 02 Oct 2016 10:22:14 +0000</pubDate>
        </item>
      </channel>
    </rss>
