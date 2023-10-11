import cgi
import html
import http.cookies
import os

form = cgi.FieldStorage()

name = form.getfirst("name", "")
surname = form.getfirst("surname", "")
name = html.escape(name)
surname = html.escape(surname)
   
terms = form.getvalue("terms", "не обрано")
languages = ["English", "Ukrainian", "German"]
languages_checkbox = {}
for l in languages:
        value_choice = form.getvalue(l, "off")
        languages_checkbox[l] = value_choice
if name=="" and surname=="":
    name="uknown user" 

print("Content-type:text/html\r\n\r\n")

template_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result</title>
</head>
<body>
    <h1> Hi, {name} {surname}</h1>
    <h1>  </h1>
    <h2> {languages_checkbox=} </h2>
    <h2> {terms=} </h2>
   </body>
</html>
"""
print(template_html)
