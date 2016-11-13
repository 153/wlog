date: 2016.11.13 [Sun] 14:00
Rewrite Rules for a nicer wlog
For wlog proper, first, rename the script to `index.py3`. 

Then, we set the variable `blog_url` to be `/wlog/` (or its other web location) and `post_prefix` to be `blog_url` . After that, add a rewrite rule like this:
`"/wlog/(.*)?" => "/wlog/index.py3?title=$1"`

and you can access categories/pages/blog entries like `/wlog/string`, `/wlog/page/2`, `/wlog/tag/entry` etc etc.   
<...> 

----
There's 2 ways to access wlog panel:

1. With the default settings, you can visit a page index.py3 or admin.py3, which takes arguments in the form of ?m=xyz
2. You can also use URL rewrite conditions for prettier URLs

I recommend rewriting URLs like this:

    1. "/wlog/admin/(.*)?" => "/wlog/admin/index.py3?m=$1",

    2. "/wlog/admin/sett.txt*" => "/wlog/admin/",

... so then, you can set the setting for "URL" to "." and access the different tools like  
"`/admin/p_add`", "`/admin/p_edit`" (for post add and post edit) 

rather than through "`/admin/index.py3?m=p_add`"