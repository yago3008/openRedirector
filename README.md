
# OPENREDIRECTOR
Toll for auto-openredirect discovery.

# Install and configure
```
▶ git clone https://github.com/yago3008/openRedirector
▶ cd openRedirector
▶ chmod +x openredirector.py
```

# Usage exemple

### Basic exemple STDIN URLs:
openRedirector accepts feeding via STDIN, and has a default worlist.
```
▶ cat domains.txt
http://example.com/redirect?redirect=
http://example.edu/redirect?url=
http://example.net/redirect?goto=

▶ cat domains.txt | ./openredirector.py
[-] NO REDIRECT FOUND: http://example.com/redirect?redirect==/%09/example.com
[+] REDIRECT FOUND: http://example.edu/redirect?url=/%2f%2fexample.com
[+] REDIRECT FOUND: http://example.net/redirect?goto=/%2f%2fexample.com
```

### Basic exemple URL list:
You can add a URL list by using the ```-l``` flag and specifying URL path:
```
▶ ./openredirector.py -l /path/to/url-list.txt
```

### Basic exemple single target:
You can add a single target by using the ```-u``` flag and specifying target:
```
▶ ./openredirector.py -u http://example.com/redirect?redirect=
```

### Timeout
You can change the timeout by using the ```-t``` flag and specifying a timeout in seconds:
```
▶ cat domains.txt | ./openredirector.py -t 2 
```

### Custom wordlist
You can add a custom wordlist by using the ```-w``` flag and specifying worlist path:
```
▶ cat domains.txt | ./openredirector.py -w /usr/share/wordlists/exemple.txt
```

### Custom wordlist
You can add Threads to scan faster by using the ```-T``` flag and specifying threads quantity:
```
▶ cat domains.txt | ./openredirector.py -T 10
```


