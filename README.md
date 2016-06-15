# tinyurl
Tiny URL implementation in flask

The implementation for tinyurl is using Flask (Python).

The short URL encoding contains following 51 characters (removed the ambiguous characters and vowels, ie, 0, 1, a, i, o, u, l, A ...):
<code>23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ-_</code>

It is a bidirect function to encode/decode row id in database table to a 6 characters string.
* 1      -> 000003
* 125    -> 00004v
* 28976  -> 000f9b

# Try it out

Execute the setup.sh on a *NIX machine and try the following url in a browser.
http://127.0.0.1:8080
