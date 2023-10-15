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
    name="uknown" 
    surname=="user"

print(f"Set-cookie: name={name}")
print(f"Set-cookie: surname={surname}")
print(f"Set-cookie: terms={terms};")
print(f"Set-cookie: English={languages_checkbox["English"]};")
print(f"Set-cookie: Ukrainian={languages_checkbox["Ukrainian"]};")
print(f"Set-cookie: German={languages_checkbox["German"]};")
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
counter = 0

def deleteCookies():
    expired_date = "Wed, 28 Aug 2013 18:30:00 GMT"
    print(f"Set-cookie: name={name}; expires={expired_date};")
    print(f"Set-cookie: surname={name}; expires={expired_date};")
    print(f"Set-cookie: terms={name}; expires={expired_date};")
    print(f"Set-cookie: English={name}; expires={expired_date};")
    print(f"Set-cookie: Ukrainian={name}; expires={expired_date};")
    print(f"Set-cookie: German={name}; expires={expired_date};")
    print(f"Set-cookie: counter={name}; expires={expired_date};")
  
name_cookie = cookie.get("name").value
surname_cookie = cookie.get("surname").value
terms_cookie = cookie.get("terms").value
english_cookie = cookie.get("English").value
ukrainian_cookie = cookie.get("Ukrainian").value
german_cookie = cookie.get("German").value
if cookie.get('counter').value >= 0:
   counter = cookie['counter']
   print(f"Set-cookie: counter={counter};")
counter+=1
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
    <h1>Language options for you are:  </h1>
    <h2>English - {languages_checkbox["English"]} </h2>
     <h2>Ukrainian - {languages_checkbox["Ukrainian"]} </h2>
    <h2>German - {languages_checkbox["German"]} </h2>
    <h1>Did you agree to the terms? {terms} </h1>
    <br>
    <h2> From cookie: </h2>
    <h3> {name_cookie=} {surname_cookie=} {terms_cookie=} {english_cookie=} {ukrainian_cookie=} {german_cookie=}</h3>
    <h2>{counter=}</h2>
   </body>
</html>
"""
print(template_html)
