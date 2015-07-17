#!/usr/bin/env python3
import cgi, os, sys, math, mistune

site_name = "4x13"               # Link to the homepage with this name
blog_title = "wlog"              # Rename wlog to anything you want :)
blog_url = "/wlog/"              # Absolute location for wlog on the server
pages_dir = "./pages/"           # Location of blog posts relative to script on disk
blog_theme = "wlog"              # Use head.wlog and post.wlog for wlog theme
pagin = 4                        # Change this to change how many posts are shown per page
markdown = mistune.Markdown()
pages_extension = ".md"          # Default file extension. Markdown recommended
len_ext = len(pages_extension)
readmore = "<...> "              # Line beginning with this creates a preview for indexing

index_message = """<div style='background-color:#aaa'>
<b>wlog</b>, a public domain weblog
<small style='float:right'>
<a href='./hellow'>(v0.5 // 150 sloc)</a></small></div><hr>"""

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
            print(index_message)
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
                        post_printer(page_name)   # fix this
    else:
        wlog_head("")
        print(index_message)
        post_list(pages_dir,1)
            
def wlog_head(page_name=''):
    print("Content-type: text/html\r\n")
    with open(pages_dir+"head."+blog_theme) as f:
        if page_name:
            if page_name.split('/')[-1] == "":
                page_name = " "+str(page_name.split('/')[0])
            else:
                page_name = " "+str(page_name.split('/')[-1])
            print(str(f.read()).format(site_name,blog_title," // "+page_name))
        else:
            print(str(f.read()).format(site_name,blog_title,''))

def post_heading(post_title,page_date="0",post_filename="", post_tag="/", tag_alias="/"):    
    with open(pages_dir+"post."+blog_theme) as f:
        print(str(f.read()).format(page_date,post_filename,post_title,post_tag,tag_alias))

def post_printer(page_name,preview=0,tag="",date="0"):
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
            page_path = str(blog_url[:-1]+tag_alias+page_name)
            previewed = []
            for line in contents[1:]:
                if line[:len(readmore)] == readmore:
                    if preview == 1:
                        previewed.append("\n<a href='"+page_path+"'>Read more...</a>")
                        break
                    else:
                        previewed.append(line[len(readmore):])
                else:
                    previewed.append(line)
            post_heading(contents[0], post_date, page_path, post_tag, tag_alias)
            print(markdown(''.join(previewed)))
            print('\n<hr align="left" size="0.25" noshade="">')
    else:
        print("<p>Sorry, but [<em>"+page_name+"</em>] does not exist :(<hr>")

def wlog_foot(page_no=0,page_nos=0,page_tag=""):
    print("""<a href="/">[{0}]</a> &diams; 
          <a href="/{1}/">[{1}]</a>""".format(site_name,blog_title))
    if page_tag == "/":
        page_tag = ""
    if page_no > 1:
        print("&diams; [<a href='"+blog_url+page_tag+str(page_no-1)+"'>prev</a>]")
    if page_no < page_nos:
        print("&diams; [<a href='"+blog_url+page_tag+str(page_no+1)+"'>next</a>]")
    if page_nos > 0:
        print("&diams; ["+str(page_no)+"/"+str(page_nos)+"]")
    print("""<em style="float:right">content is public domain.</em>
        <hr size="1" align="left" noshade>""")

def post_list(pages_dir,page_no=0):
    page_path = []
    for root, dirs, fils in os.walk(pages_dir):
        for filename in fils:
            page_path.append(os.path.join(root,filename))
    dict = {}
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
                dict[post_date] = each_page[:-len_ext]
    post_list_pages(dict,page_no,tag)

def post_list_pages(dict,page_no=1,tag=""):
    post_no = (len(dict))
    page_nos=(math.ceil(post_no/pagin))
    if page_no > page_nos:
        page_no = page_nos
    if page_no <= 0:
        page_no = 1
    if page_nos > 1:
        page_range = slice(((int(page_no) - 1)* pagin),(int(page_no) * pagin))
        for key in sorted(dict,reverse=True)[page_range]:
            post_printer(tag+dict[key],preview=1)
        wlog_foot(page_no,page_nos,tag+"/")
    if page_nos == 1:
        for key in sorted(dict,reverse=True):
            post_printer(tag+dict[key],preview=1)
        wlog_foot(page_no,page_nos,tag)

main()
