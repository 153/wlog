#!/usr/bin/env python3
import cgi
import os
import sys 
import math
import mistune

site_name = "4x13"
blog_title = "wlog"
blog_theme = "wlog"
pages_dir = "./pages/"
pages_extension = ".md"
len_ext = len(pages_extension)
pagin = 4

markdown = mistune.Markdown()

def escape_html(text):
    """escape strings for display in HTML"""
    return cgi.escape(text, quote=True).\
        replace(u'\n', u'<br />').\
        replace(u'\t', u'&emsp;').\
        replace(u'  ', u' &nbsp;')

def main():
    form = cgi.FieldStorage()
    page_name = form.getvalue('title')
    if page_name:
        page_name = escape_html(page_name)            
        wlog_head(page_name) 
        if os.path.isfile(pages_dir+page_name+pages_extension):
            post_printer(page_name)
            wlog_foot()        
        else:
            print("<div style='background-color:#aaa'><b>wlog</b>, a public domain weblog by Anon in Python",
              "<small style='float:right'><a href='./hellow'>",
              "(0.1.8 // 170 sloc)</a></small></div><hr>")
            try:
                page_no = int(page_name.split('/')[-1])
                page_tag = page_name.split('/')[0:]
                if int(page_tag[0]) != page_no:
                    post_list(pages_dir+page_tag[0],page_no)
                else:
                    post_list(pages_dir,page_no)
            except:
                try:
                    page_no = int(page_name.split('/')[-1])
                    page_tag = str(page_name.split('/')[:-1])[2:-2]
                    post_list(pages_dir+page_tag,page_no)
                except:
                    try:
                        page_tag = page_name.split('/')[0]
                        post_list(pages_dir+page_tag,1)                
                    except:                            
                        post_heading("404 :: "+page_name,"page not found ...",".")
                        post_printer(page_name)
    else:
        wlog_head("")
        print("<div style='background-color:#aaa'><b>wlog</b>, a public domain weblog by Anon in Python",
              "<small style='float:right'><a href='./hellow'>",
              "(0.1.7 // 140 sloc)</a></small></div><hr>")
        post_list(pages_dir,1)
            
def wlog_head(page_name=''):
    print("Content-type: text/html\r\n")
    with open(pages_dir+"head."+blog_theme) as f:
        if page_name:
#            if '/' in page_name:
            if page_name.split('/')[-1] == "":
                page_name = " "+str(page_name.split('/')[0])
            else:
                page_name = " "+str(page_name.split('/')[-1])
            print(str(f.read()).format(site_name,blog_title," // "+page_name))
        else:
            print(str(f.read()).format(site_name,blog_title,''))

def post_heading(post_title,page_date="0",post_filename="", post_tag="/", tag_alias="/"):    
   # datetime path title tag
    with open(pages_dir+"post."+blog_theme) as f:
        print(str(f.read()).format(page_date,post_filename,post_title,post_tag,tag_alias))
# 
#<span id='auth' style='float:right'>by <a href=''>auth</a>, 14:00</span></em>

def post_printer(page_name,tag="",date="0"):
#    print(pages_dir+tag+page_name+pages_extension)
    if os.path.isfile(pages_dir+page_name+pages_extension):
        with open(pages_dir+page_name+pages_extension) as f:
            contents = list(f)
            if contents[0][:5] == "date:":
                post_date = contents.pop(0)[5:]
            else:
                post_date = "Stickied post" # sticky, draft, etc?

            post_tag = str(page_name.split('/')[0])
            if post_tag != page_name:
                tag_alias = "/"+post_tag+"/"
                page_name = page_name.split("/")[-1]
            else:
                post_tag = "."
                tag_alias = "/"
            page_path = str("/wlog"+tag_alias+page_name)
            post_heading(contents[0], post_date, page_path, post_tag, tag_alias)
            print(markdown(''.join(contents[1:])))
            print('\n<hr align="left" size="0.25" noshade="">')
            
    else:
        print("<p>Sorry, but [<em>"+page_name+"</em>] does not exist :(<hr>")

def wlog_foot(page_no=0,page_nos=0,page_tag=""):
    print("""<a href="/">[{0}]</a> &diams; 
          <a href="/{1}/">[{1}]</a>""".format(site_name,blog_title))
    if page_tag == "/":
        page_tag = ""
    if page_no > 1:
        print("&diams; [<a href='"+"/wlog/"+page_tag+str(page_no-1)+"'>prev</a>]")
    if page_no < page_nos:
        print("&diams; [<a href='"+"/wlog/"+page_tag+str(page_no+1)+"'>next</a>]")
    if page_nos > 0:
        print("&diams; ["+str(page_no)+"/"+str(page_nos)+"]")
    print("""<em style="float:right">content is public domain.</em>
        <hr size="1" align="left" noshade>""")

def post_list(pages_dir,page_no=0):
    if os.path.isdir(pages_dir):
        page_path = []
        for root, dirs, fils in os.walk(pages_dir):
            for filename in fils:
                page_path.append(os.path.join(root,filename))
        dict = {}
        # associate (tag/)file.ext with date of publication to prep for pagin
        for each_page in page_path: 
            if each_page[-len_ext:] == pages_extension: 
                each_page = each_page[len(pages_dir):] 
                with open(pages_dir+each_page) as f:
                    contents = list(f)
                    if contents[0][:5] == "date:":
                        post_date=contents.pop(0)[5:].strip()
                    else:
                        post_date='s' # before, after, or null posts? sticky
                    tag = str(pages_dir.split('/')[-1])
#                    print(tag)
                    dict[post_date] = each_page[:-len_ext]
        post_list_pages(dict,page_no,tag)

def post_list_pages(dict,page_no=1,tag=""):
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
            post_printer(tag+dict[key])
#        print("page "+str(page_no)+" of "+str(page_nos)+" ")        
        wlog_foot(page_no,page_nos,tag+"/")
    if page_nos == 1:
        for key in sorted(dict,reverse=True):
            post_printer(tag+dict[key])
        wlog_foot(page_no,page_nos,tag)

def post_tagging():
    f = []
    for (root, dirs, files) in os.walk(pages_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            f.append(filepath)
    return f

main()
