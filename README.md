# wlog v0.5
public domain python weblog -- software of http://4x13.net/wlog/

Sample theme and entry in this repo's ./pages/

Features implemented: markdown -> html, file -> post, templates,
date and title from metadata, post indexing, pagination,
themeing, subdirectory support, pagination and indexing of
subdirectories, readmore

| Version | Date | Change:
|:------- |:----:|:-------
| v0.1.0  | 06-21 14:00 | project initiated
| v0.1.1  | 06-21 22:00 | file loading in "./wlog-pages" dir
| v0.1.2  | 06-22 12:00 | markdown added
| v0.1.3  | 06-22 22:00 | random indexing added
| v0.1.4  | 06-23 14:00 | realistic indexing added
| v0.1.5  | 06-23 21:00 | pagination added to indexing
| v0.1.6  | 06-27 00:00 | theming began... notes made
| v0.1.7  | 07-11 19:00 | tagging begun
| v0.1.8  | 07-12 15:00 | tagging finished
| v0.5    | 07-16 20:00 | readmore added, script basically done.


To install: 

0. Confirm that you have a web server, python3, and get Mistune - Python Markdown Converter. 
1. place wlog.py3 in a directory, and make it accessible via the web server. 
2. create a directory called "pages" in wlog's directory, and add head.wlog and post.wlog 
3. confirm that the variables at the top of wlog.py3 are correct, and modify head.wlog and post.wlog as desired
4. By default, wlog takes arguments as wlog.py3?title=ARGUMENT . 
5. For cooler URIs, try calling it "index.py3" and do a rewrite similar with this: 
6. (lighttpd) "/wlog/(.*)?" => "/wlog/index.py3?title=$1"

To add blog entries:

1. Upload a text file with the extension you select to the pages directory (./pages/*.md is the default blog entry)
2. Format it with "date: y-m-d" on the first line, and the title you want for the entry on the second line.
3. Write the rest of your blog post in Markdown.
4. Begin a line with <...>, followed by a space, to cut the blog entry short at that line in the index.
5. Place the file in a subdirectory of ./pages/ to give it a category.

To theme/configure further:

1. Copy head.wlog and post.wlog and change the extension (example: head.mytheme post.mytheme)
2. Modify as desired, change the theme setting in the script, and modify the script further as needed.
3. Submit your custom themeing / features to the project to help the project and participate in the public domain
