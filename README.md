# tinyurl
Tiny URL implementation in flask

This is an implementation for tinyurl in Python Flask using RESTful API.

The short URL encoding is using following 51 characters
23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ-_

The implementation is using a bidirect function to encode/decode record row id in DB to a 6 characters string.
<code>
* 1      -> 000003
* 125    -> 00004v
* 28976  -> 000f9b
</code>

# Try it out

Execute the setup.sh on a *NIX machine and try the following url in a browser.
http://127.0.0.1:8080
