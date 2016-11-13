#!/usr/bin/env python3
import cgi, os, sys, math, mistune, re

site_name = "site"            # Link to the homepage with this name
blog_title = "blog"              # Rename wlog to anything you want :)
full_url = "http://4x13.net" # used for RSS
t_z = ":00-08:00"	# used for RSS
#blog_url = "/wlog/"              # Absolute location for wlog on the server
blog_url = "/wlog/wlog.py3"              # Absolute location for wlog on the server
pages_dir = "./pages/"           # Location of blog posts relative to script on disk
theme_dir = "./themes/"
blog_theme = "bluer"              # Use head.wlog and post.wlog for wlog theme
pagin = 5                       # Change this to change how many posts are shown per page
markdown = mistune.Markdown()
pages_extension = ".md"          # Default file extension. Markdown recommended
len_ext = len(pages_extension)
readmore = "<...> "              # Line beginning with this creates a preview for indexing
post_prefix = blog_url+"?title=" # Optionally change to blog_url
date_prefix = "date: "
ldp = len(date_prefix)
#post_prefix = blog_url # Optionally change to "blog_url+"?title="

def escape_html(text):
    """escape strings for display in HTML"""
    return cgi.escape(text, quote=True).\
        replace(u'\n', u'<br />').\
        replace(u'\t', u'&emsp;').\
        replace(u'  ', u' &nbsp;')

def main():
    form = cgi.FieldStorage()
    page_name = form.getvalue('title')
    if not page_name:
        wlog_head("1")
        post_list(pages_dir,1)
        return
    if page_name == 'posts.atom':
        do_rss()
        return
    page_name = escape_html(page_name)            
    wlog_head(page_name)
    if page_name == '0':
        post_list(pages_dir, '0')
        return
    elif os.path.isfile(pages_dir+page_name+pages_extension):
        post_printer(page_name)
        wlog_foot()        
        return
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

            
def wlog_head(page_name=' '):
    print("Content-type: text/html\r\n")
    with open(theme_dir+"head."+blog_theme) as f:
        if page_name:
            if page_name.split('/')[-1] == "":
                page_name = " "+str(page_name.split('/')[0])
            else:
                page_name = " "+str(page_name.split('/')[-1])
            content = [site_name, blog_title, " // " + page_name, post_prefix]
            print(str(f.read()).format(*content))
        else:
            print(str(f.read()).format(content[:1], blog_title,''))

def post_heading(post_title, page_date="0",
                 post_filename="", post_tag="/", tag_alias="/"):
    content = [page_date, post_filename,
               post_title.strip(), post_tag, tag_alias, post_prefix]
    with open(theme_dir+"post."+blog_theme) as f:
        print(str(f.read()).format(*content))

def post_printer(page_name,preview=0,tag="",date="0"):
    post_date = "Stickied post" # sticky, draft, etc?
    tag_alias = "/"
    post_tag = "."
    
    if not os.path.isfile(pages_dir+page_name+pages_extension):
        print("<p>Sorry, but [<em>"+page_name+"</em>] does not exist :(<hr>")
        return
    with open(pages_dir+page_name+pages_extension) as f:
        contents = list(f)
    if contents[0][:ldp] == date_prefix:
        post_date = contents.pop(0)[ldp:]
    if post_tag != page_name:
        post_tag = str(page_name.split('/')[0])
        tag_alias = "/"+post_tag+"/"
        page_name = page_name.split("/")[-1]

    page_path = str(post_prefix+tag_alias[1:]+page_name)
    previewed = []
    for line in contents[1:]:
        if line[:len(readmore)] == readmore and preview == 1:
            previewed.append("\n<a href='"+page_path+"'>Read more...</a>")
            break
        elif line[:len(readmore)] == readmore and not preview:
            previewed.append(line[len(readmore):])
        else:
            previewed.append(line)
            
    post_heading(contents[0], post_date, page_path, post_tag, tag_alias)
    print(markdown(''.join(previewed)))
    print('\n<!-- hr align="left" size="0.25" noshade="" -->')

def wlog_foot(page_no=0,page_nos=0,page_tag=""):
    print("""</div><p><div class="post"><hr><a href="/">[{0}]</a> &diams; 
          <a href="{2}">[{1}]</a>""".format(site_name,blog_title,blog_url))
    print("&diams; <a href='" + post_prefix+"0'>[all]</a>")
    if page_tag == "/":
        page_tag = ""
    if page_no > 1:
        print("&diams; [<a href='"+post_prefix+page_tag+str(page_no-1)+"'>prev</a>]")
    if page_no < page_nos:
        print("&diams; [<a href='"+post_prefix+page_tag+str(page_no+1)+"'>next</a>]")
    if page_nos > 0:
        print("&diams; ["+str(page_no)+"/"+str(page_nos)+"]")
    print("""<hr size="1" align="left" noshade>""")

def post_list(pages_dir,page_no=0,rss=0):
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
                    post_date='s' # work on this sometime
                tag = str(pages_dir.split('/')[-1])
                dict[post_date] = each_page[:-len_ext]
    if rss != 1 and page_no != '0':
        post_list_pages(dict,page_no,tag)
    elif page_no == '0':
        print("<div class='post'>")
        print("<h2>post archive</h2>")
        print(len(dict), "posts.<p>")
        print("<center><table>")
        print("<tr><th><th>Date<th>Title")
        bent = []
        for a in dict:
            bent.append([a, dict[a]])
        for n, i in enumerate(sorted(bent, reverse=1)):
            print("<tr><th>", (n+1))
            i[1] = "<a href='" + post_prefix + i[1] + "'>" + i[1].replace('/', ': ') + "</a>"
            print("<td>", i[0], "<td>", i[1])
        print("</table></center></div><p>")
        wlog_foot()
    else:
        dlist = []
        for dic in dict:
            dlist.append([dic, dict[dic]])
        return dlist

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

def do_rss():
    print("Content-type: application/atom+xml\r\n")
    print('<?xml version="1.0" encoding="utf-8"?>')
    print('<feed xmlns="http://www.w3.org/2005/Atom">')
    print("<title>", blog_title, "</title>")
    print("<link rel='self' href='"+ full_url + blog_url + "posts.atom'/>")
    print("<link href='"+ full_url + blog_url + "'/>")
    print("<id>{0}{1}</id>".format(full_url, blog_url))
    posts = sorted(post_list(pages_dir,1,1), reverse=True)
    upd = posts[0][0].replace(" ", "").replace(".", "-")
    upd = re.sub(r'\[(.*?)\]', 'T', upd)
    upd += t_z
    print("<updated>" + upd + "</updated>")
    for post in posts:
        print("\n<entry>")
        post[0] = post[0].replace(" ","").replace(".", "-")
        post[0] = re.sub(r'\[(.*?)\]', 'T', post[0])
        post[0] += t_z
        print("<updated>" + post[0] + "</updated>")
        purl = full_url + blog_url + post[1]
        p_id = full_url.replace("http://","tag:") + "," + post[0][:10]
        p_id += ":" + blog_url + post[1]
        print("<id>" + p_id + "</id>")
        print("<link rel='alternate' href='" + purl + "'/>")
        if "/" in posts[1]:
            print("<category>", posts[1].split("/"), "</category>")
        with open(pages_dir + post[1] + pages_extension) as p:
            p = p.read().splitlines()
            p[2] = "\n".join(p[2:])
            if readmore in p[2]:
                p[2] = p[2].split(readmore)
                p[2] = p[2][0] + "<p> [*Post shortened*]({0})".format(purl)
            p[2] = markdown(p[2])                    
            p[2] = cgi.escape(p[2])
            p[2] = p[2].replace('&amp;lt;', '&lt;').replace('&amp;gt;', '&gt;')
        print("<title>", p[1], "</title>")
        print("<content type='html'>", p[2], "</content>")
        print("</entry>\n")
    print("</feed>")

def do_list():
    print("ahaha")
main()
