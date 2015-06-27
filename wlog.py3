#!/usr/bin/env python3
import cgi
import os.path
import sys 
import math
import mistune

site_name = "site"
blog_title = "wlog"
pages_dir = "./wlog-pages/"
pagin = 4

markdown = mistune.Markdown()

def escape_html(text):
    """escape strings for display in HTML"""
    return cgi.escape(text, quote=True).\
        replace(u'\n', u'<br />').\
        replace(u'\t', u'&emsp;').\
        replace(u'  ', u' &nbsp;')

def main():
    """Get title. Print html template, print single post if requested."""
    form = cgi.FieldStorage()
    page_name = form.getvalue('title')
    wlog_head() # static header, html bullshit 
    if page_name:
        if os.path.isfile(pages_dir+page_name+".md"):
            post_printer(page_name)
            wlog_foot()        
        else:
            try: 
                post_list(pages_dir,int(page_name))
            except:
                page_name = escape_html(page_name)            
                post_heading("404 error!!","page not found ...",".")
                post_printer(page_name)
    else:
        print("<div style='background-color:#aaa'><b>wlog</b>, a public domain weblog by Anon in Python",
              "<small style='float:right'>(0.1.6 // 120 sloc)&nbsp;</small></div><hr>")
        post_list(pages_dir,1)
            
def wlog_head():
    print("Content-type: text/html\n")
    with open(pages_dir+"head.wlog") as f:
        print(str(f.read()).format(site_name,blog_title))

def post_heading(post_title,page_date="0",post_filename=""):    
    with open(pages_dir+"post.wlog") as f:
        print(str(f.read()).format(page_date,post_filename,post_title))

def post_printer(page_name,date="0"):
    if os.path.isfile(pages_dir+page_name+".md"):
        with open(pages_dir+page_name+".md") as f:
            contents = list(f)
            if contents[0][:5] == "ymdt:":
                post_date = contents.pop(0)[5:]
            else:
                post_date = ""
            post_heading(contents[0], post_date, page_name)
            print(markdown(''.join(contents[1:])))
            print('\n<hr align="left" size="0.25" noshade="">')
            
    else:
        print("<p>Sorry, but [<em>"+page_name+".md</em>] does not exist :(<hr>")
        wlog_foot()

def wlog_foot(page_no=0,page_nos=0):
    print("""<a href="/">[{0}]</a> &diams; 
          <a href="/scripts/{1}/">[{1}]</a>""".format(site_name,blog_title))
    if page_no > 1:
        print("&diams; [<a href='"+str(page_no-1)+"'>prev</a>]")
    if page_no < page_nos:
        print("&diams; [<a href='"+str(page_no+1)+"'>next</a>]")
    if page_nos > 0:
        print("&diams; ["+str(page_no)+"/"+str(page_nos)+"]")
    print("""<em style="float:right">content is public domain.</em>
        <hr size="1" align="left" noshade>""")

def post_list(pages_dir,page_no=0):
    if os.path.isdir(pages_dir):
        filenames = os.listdir(pages_dir)
        dict = {}
        for filename in filenames:
            if filename[-3:] == ".md":                
                with open(pages_dir+filename) as f:
                    contents = list(f)
                    if contents[0][:5] == "ymdt:":
                        post_date=contents.pop(0)[5:].strip()
                        dict[post_date] = filename[:-3]
        post_list_pages(dict,page_no,pagin)

def post_list_pages(dict,page_no=1,pagin=4):
# confusing vars... page_no is the current page number,
# page_nos = # of pages, and post_no is total posts.
# these vars are re-used, so take mental note, hacker.
# this makes use of "pagin", or your pagination var.
# pagin=4 means 4 posts per page.

    post_no = (len(dict))
    page_nos=(math.ceil(post_no/pagin))
    if page_no > page_nos:
        page_no = page_nos
    if page_no <= 0:
        page_no = 1
    if page_nos > 1:
        page_range = slice(((int(page_no) - 1)* pagin),(int(page_no) * pagin))
        for key in sorted(dict,reverse=True)[page_range]:
            post_printer(dict[key])
        wlog_foot(page_no,page_nos)
    if page_nos == 1:
        for key in sorted(dict,reverse=True):
            post_printer(dict[key])
        wlog_foot()        

main()
