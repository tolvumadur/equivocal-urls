#!/usr/bin/env python3

import re

class URLParsingException(Exception):
    pass

class URLParsingTestException(Exception):
    pass

def galump(b):
    if b is None:
        return b
    return b"".join(b)

def display(b):
    if b is None:
        return "[NONE]"
    if type(b) is list:
        return "".join(str(x, "ascii", "backslashreplace")for x in b)
    return str(b, "ascii", "backslashreplace")

def tokenize(s):
        if s is None:
            return None
        loc = s.find(b"%")
        while loc != -1:
            try:
                p = s[loc:loc+3]
                assert p[1:2] in set(x.to_bytes(1,byteorder="big",signed=False) for x in b"1234567890abcdefABCDEF")
                assert p[2:3] in set(x.to_bytes(1,byteorder="big",signed=False) for x in b"1234567890abcdefABCDEF")
            except ValueError:
                raise URLParsingException("A % was not followed by two hex digits (1)")
            except AssertionError:
                raise URLParsingException(f"A % was not followed by two hex digits (2) {p}")
            loc = s.find(b"%", loc+1, len(s))
            
        f = 0
        res = []
        while f < len(s):
            if s[f:f+1] != b"%":
                res.append(s[f:f+1])
            else:
                res.append(s[f:f+3])
                f += 2
            f += 1

        assert b'%' not in res, res
        return res

class URL:
    def __init__(self):
        self.error = "URL Object Uninitialized"

    def __str__(self):
        return f"""
        URL:       {self.orig_bytes}
        Scheme:    {self.scheme}
        Authority: {self.display(self.authority)}
        UserInfo:  {self.display(self.userinfo)}
        Hostname:  {self.display(self.hostname)}
        Port:      {self.display(self.port)}
        Path:      {self.display(self.path)}
        Query:     {self.display(self.query)}
        Fragment:  {self.display(self.fragment)}
        Errors:    {self.display(self.error)}
        """

    def display(self, b):
        return display(b)


    def print_comparison(self,scheme,authority,userinfo,username,password,hostname,port,path,query,fragment):
        print(self.get_comparison(self,scheme,authority,userinfo,username,password,hostname,port,path,query,fragment))

    def get_comparison(self,scheme,authority,userinfo,username,password,hostname,port,path,query,fragment):
        return f"""        ---------------------------------------------------------------------------------------
        URL:       {self.display(self.orig_bytes)} 
        ---------------------------------------------------------------------------------------
        Scheme:    {self.display(self.scheme):30} {self.display(scheme)}
        Authority: {self.display(self.authority):30} {self.display(authority)}
        UserInfo:  {self.display(self.userinfo):30} {self.display(userinfo)}
        Hostname:  {self.display(self.hostname):30} {self.display(hostname)}
        Port:      {self.display(self.port):30} {self.display(port)}
        Path:      {self.display(self.path):30} {self.display(path)}
        Query:     {self.display(self.query):30} {self.display(query)}
        Fragment:  {self.display(self.fragment):30} {self.display(fragment)}
        Errors:    {self.display(self.error):30} [NONE]
        """

    def __init__(self, url):

        if url is None:
            raise URLParsingException("URL was None")
        if type(url) is not bytes:
            raise URLParsingException(f"URL was of type {type(url)}--bytes expected")
        if len(url) == 0:
            raise URLParsingException("URL was empty")

        self.orig_bytes = url
        self.error = None
        self.scheme = None
        self.authority = None
        self.userinfo = None
        self.hostname = None
        self.port = None
        self.path = None
        self.query = None
        self.fragment = None

        self.gen_delims = set(x.to_bytes(1,byteorder="big",signed=False) for x in b":/?#[]@")
        self.sub_delims = set(x.to_bytes(1,byteorder="big",signed=False) for x in b"!$&'()*+,;=") 
        self.alpha = set(x.to_bytes(1,byteorder="big",signed=False) for x in b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.digit = set(x.to_bytes(1,byteorder="big",signed=False) for x in b"1234567890")
        self.hexdigit = set(x.to_bytes(1,byteorder="big",signed=False) for x in b"1234567890abcdefABCDEF")
        self.pct_encoded = set(b"%" + a + b for a in self.hexdigit for b in self.hexdigit)
        self.rfc_parser = rb"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?"

        self.reserved = set()
        self.reserved.update(self.gen_delims, self.sub_delims)

        self.unreserved = set()
        self.unreserved.update(self.alpha, self.digit, set(x.to_bytes(1,byteorder="big",signed=False) for x in b"._-~"))

        self.pchar = set()
        self.pchar.update(self.unreserved, self.sub_delims,  set(x.to_bytes(1,byteorder="big",signed=False) for x in b":@"), self.pct_encoded)

        self.valid_bytes = set()
        self.valid_bytes.update(self.hexdigit, self.alpha, self.reserved, self.unreserved)
        self.valid_bytes.add(b"%")
        self.valid_bytes.add(b"[")
        self.valid_bytes.add(b"]")

        # Go through and URL-Encode everything outside the permissible character sets
        self.check_all_bytes_valid()

        # Parse out the syntactic segments using provided regex
        m = re.search(self.rfc_parser, self.orig_bytes)
        if not m:
            raise URLParsingException("URL is syntactically invalid")
        else:
            self.scheme = m.group(2)
            self.validate_scheme()

            self.authority = self.tokenize(m.group(4))
            self.parse_authority()

            self.path = self.tokenize(m.group(5))
            self.validate_path()

            self.query = self.tokenize(m.group(7))
            self.validate_query()

            self.fragment = self.tokenize(m.group(9))
            self.validate_fragment()

        self.authority = b"".join(self.authority) if self.authority is not None else b""
        self.userinfo  = b"".join(self.userinfo)  if self.userinfo is not None else b""
        self.hostname  = b"".join(self.hostname)  if self.hostname is not None else b""
        self.path      = b"".join(self.path)      if self.path is not None else b""
        self.query     = b"".join(self.query)     if self.query is not None else b""
        self.fragment  = b"".join(self.fragment)  if self.fragment is not None else b""

    def tokenize(self, s):
        return tokenize(s)
        



    # Checks if the URL contains any bytes outside the permissible range in ASCII
    def check_all_bytes_valid(self):
        for b in self.orig_bytes:
            if b.to_bytes(1,byteorder="big",signed=False) not in self.valid_bytes:
                raise URLParsingException("<<Invalid byte found in URL: " + hex(b) + " {" + str(b.to_bytes(1,byteorder="big",signed=False),errors='backslashreplace') + "} >>")

    def validate_scheme(self):
        s = self.scheme
        if s is None or type(s) is not bytes or len(s) < 1:
            raise URLParsingException("Scheme is invalid:", self.scheme)
        if s[0].to_bytes(1,byteorder="big",signed=False) not in self.alpha:
            raise URLParsingException("Scheme must start with a letter:", self.scheme)
        allowed = set()
        allowed.update(set(x.to_bytes(1,byteorder="big",signed=False) for x in b"+-."), self.alpha, self.digit)
        for b in s[0:]:
            if b.to_bytes(1,byteorder="big",signed=False) not in allowed:
                raise URLParsingException("Scheme must only contain letters, digits, and +-.  ", self.scheme)

    def parse_authority(self):
        s = self.authority
        if s is None:
            self.userinfo = None
            self.hostname = None
            self.port = None
            if self.scheme in [b'http',b'https']:
                raise URLParsingException("HTTP and HTTPS do not allow an empty authority")
            return
        if len(s) == 0:
            if self.scheme in [b'http',b'https']:
                raise URLParsingException("HTTP and HTTPS do not allow an empty authority")
        at_sign_count = s.count(b"@")
        
        if at_sign_count == 1:
            self.userinfo = s[:s.index(b"@")]
            #Chars allowed in userinfo
            allowed = set()
            allowed.update(self.unreserved, self.pct_encoded, self.sub_delims)
            allowed.add(b":")
            for i in range(len(self.userinfo)):
                if self.userinfo[i] not in allowed:
                    raise URLParsingException("Illegal byte in userinfo: ", self.userinfo[i:i+1])
            s = s[s.index(b"@")+1:]

        elif at_sign_count > 1:
            raise URLParsingException("Authority can contain no more than one literal @")
        
        colon_count = s.count(b":")
        ipv6 = False
        if colon_count > 1:
            if b'[' == s[0] and s.count(b'[') == 1 and s.count(b']') == 1:
                try:
                    self.validate_IPv6(s[1:s.index(b']')])
                    self.hostname = s[1:s.index(b']')]
                    ipv6 = True
                    s = s[s.index(b']')+1:]
                    colon_count = colon_count = s.count(b":")
                except URLParsingException as m1:
                    raise URLParsingException(f"Authority after UserInfo can contain 1 ':' max except in cases of IPv6. This is not valid IPv6 syntax: {m1}")
            else:
                raise URLParsingException("Authority after UserInfo can contain 1 ':' max except in cases of IPv6")

        if colon_count == 1:
            self.port = s[s.index(b":")+1:]
            s = s[:s.index(b":")]
            allowed = set()
            allowed.update(self.digit)
            for i in range(0,len(self.port)):
                if self.port[i] not in allowed:
                    raise URLParsingException("Port contains invalid byte", self.port[i:i+1])

        if ipv6: # skip if we already decided it was an IPv6 address
            return

        self.hostname = s
        if len(s) == 0:
            self.hostname = None
            if self.scheme in [b'http',b'https']:
                raise URLParsingException("HTTP and HTTPS do not allow an empty hostname")
        self.validate_hostname()

    def validate_IPv6(self, h):
        if h[0] == b"v":
            self.validate_IPvFuture(h)
        else:
            # check only allowed bytes exist
            allowed = set()
            allowed.update(self.hexdigit)
            allowed.add(b":")
            allowed.add(b".")
            for b in h:
                if b not in h:
                    raise URLParsingException(f"Invalid syntax for IPv6 - invalid byte: {b}")
            if h.count(b":") not in [2,3,4,5,6,7]:
                raise URLParsingException(f"Impossible number of ':' to be an IPv6 Address {h.count(b':')}")
            if h.count(b".") not in [0, 3]:
                raise URLParsingException(f"Impossible number of '.' to be an IPv6 Address {h.count(b'.')}")
            # check syntax
            bits = b"".join(h).split(b":")

            have_seen_skip = False
            if bits[0] == bits[1] == b'':
                 # first bit is empty
                 have_seen_skip = True
                 bits = bits[2:]
            try:
                self.validate_IPv4((bits[-1])) # See if the last bit is an IPv4 addr
                bits = bits[:-1]
            except URLParsingException as err:
                if b"." in bits[-1]:
                    raise URLParsingException(f"Malformed final IPv4 block: {bits[-1]} {err}")
                pass            
            for bit in bits[:]:
                if len(bit) == 0:
                    if have_seen_skip == False:
                        have_seen_skip = True
                    else: 
                        raise URLParsingException("IPv6 address cannot skip with :: more than once")
                else:
                    if len(bit) > 4:
                        raise URLParsingException("IPv6 Segments cannot have longer than 4 hex chars")
                    try:
                        int(bit,16)
                    except Exception as err:
                        raise URLParsingException(f"Could not parse an IPv6 segment as a hex integer {bit} {type(err)}")
            pass

    def validate_IPvFuture(self, h):
        if h[0] != b'v' or h.count(b'.') != 1 or len(h) < 4:
            raise URLParsingException("Invalid syntax for IPvFuture")
        version = h[1:h.index('.')]
        if len(version) < 1:
            raise URLParsingException("Invalid syntax for IPvFuture - empty version")
        for b in version:
            if b not in self.hexdigit:
                raise URLParsingException("Invalid syntax for IPvFuture - version is not hexadecimal")
        addr = h[h.index(".")+1:]
        if len(addr) < 1:
            raise URLParsingException("Invalid syntax for IPvFuture - empty address")
        allowed = set()
        allowed.update(self.unreserved,self.sub_delims)
        allowed.add(b':')
        for b in addr:
            if b not in allowed:
                raise URLParsingException(f"Invalid syntax for IPvFuture - invalid byte in address portion: {b}")
        pass

    def validate_IPv4(self, h):
        db = ""
        if h is None:
            raise URLParsingException("Potential IPv4 was None")
        if type(h) is not bytes:
            raise URLParsingException("Potential IPv4 was not bytes")
        if h.count(b".") != 3:
            raise URLParsingException("Potential IPv4 did not have three periods")
        try:
            oes = h.split(b".")
            for o in oes:
                db = o
                oi = int(o, 10)
                if oi < 0 or oi > 255:
                    raise URLParsingException(f"Potential IPv4 had 4 segments, one was an integer out of bounds 0-255 {oi}")
        except Exception as err:
            raise URLParsingException(f"Potential IPv4 had 4 segments, but at least one of those did not contain a decimal number {db} {type(err)}: {err}")
        
        #self.error = b"This contains a valid IPv4 Address"
        pass



    def validate_reg_name(self, h):
        allowed = set()
        allowed.update(self.unreserved, self.pct_encoded, self.sub_delims)
        for b in h:
            if b not in allowed:
                raise URLParsingException(f"Invalid byte for a reg_name: {b} {h}")

        #self.error = b"Valid reg_name: " + bytes(self.display(h[:]), "utf-8") + bytes(str(allowed), 'ascii')
        pass

    def validate_hostname(self):
        s = self.hostname
        try:
            self.validate_IPv4(s)
            return
        except URLParsingException as m1:
            try:
                self.validate_reg_name(s)
            except URLParsingException as m2:
                raise URLParsingException(f"Host is not a valid IPv6, IPvFuture, IPv4, or RegName\nIPv4 parser said {m1}\nRegName parser said {m2}")

    def validate_path(self):
        s = self.path
        if type(s) is not list:
            raise URLParsingException("Path is invalid:", self.path)
        if s is None or len(s) < 1:
            return # Empty Path

        # If this is a relative URL, this cannot start with two //'s
        #TODO we are setting aside relative URLs for now

        allowed = set()
        allowed.update(self.unreserved, self.pct_encoded, self.sub_delims)
        allowed.add(b"@")
        allowed.add(b":")
        allowed.add(b"/")# See TODO above

        for b in s:
            if b not in allowed:
                raise URLParsingException("Path contains invalid byte", b, b"".join(self.path))


    def validate_query(self):
        s = self.query
        if s is None:
            return # Empty Query is ok
        if type(s) is not list:
            raise URLParsingException("Query is an invalid type:", type(self.query))
        if len(s) < 1:
            return # Empty Query is ok

        allowed = set()
        allowed.update(self.pchar)
        allowed.add(b"/")
        allowed.add(b"?")
        #allowed.add(b"%")
        for b in s:
            if b not in allowed:
                raise URLParsingException("Query contains invalid byte" + str(b, encoding="ascii", errors='backslashreplace') + "  " + display(self.query))

    def validate_fragment(self):   
        s = self.fragment
        if s is None:
            return
        if type(s) is not list:
            raise URLParsingException("Fragment is invalid type:" + str(type(self.fragment)))
        if len(s) < 1:
            return # Empty Query is ok

        allowed = set()
        allowed.update(self.pchar)
        allowed.add(b"/")
        allowed.add(b"?")
        for b in s:
            if b not in allowed:
                raise URLParsingException("Fragment contains invalid byte" + str(b,encoding="ascii", errors='backslashreplace') + display(self.fragment))            


def urlparse(url):
    return URL(url)

def testparse(url, scheme=b"", authority=b"", userinfo=b"", username=b"", password=b"", hostname=b"", port=b"", path=b"", query=b"", fragment=b"", shouldfail=False, error_must_contain=None):
    try:
        u = URL(url)
    except URLParsingException as err:
        if not shouldfail:
            raise URLParsingTestException(f"Valid URL was rejected: {err}\nURL: {url}")
        else:
            if error_must_contain is not None:
                if error_must_contain not in str(err):
                    raise URLParsingTestException(f"Invalid URL was rejected, but for the wrong reasons. Expected: {error_must_contain}\nGot: {err}")
            return
    except Exception as err:
        raise URLParsingTestException(f"URL Parser reached an unhandled exception: {type(err)}: {err}\nURL: {url}")

    if shouldfail:
        raise URLParsingTestException(f"\n\nInvalid URL was accepted: {url}\n{u}")
    
    try:
        assert u.scheme    == scheme,    f"\ngot:      {display(u.scheme)} \nexpected: {display(scheme)}"
        assert u.authority == tokenize(authority), f"\ngot:      {display(u.authority)} \nexpected: {display(authority)}"
        assert u.userinfo  == tokenize(userinfo),  f"\ngot:      {display(u.userinfo)} \nexpected: {display(userinfo)}"
        assert u.hostname  == tokenize(hostname),  f"\ngot:      {display(u.hostname)} \nexpected: {display(hostname)}"
        assert u.port      == tokenize(port),      f"\ngot:      {display(u.port)} \nexpected: {display(port)}"
        assert u.path      == tokenize(path),      f"\ngot:      {display(u.path)} \nexpected: {display(path)}"
        assert u.query     == tokenize(query),     f"\ngot:      {display(u.query)} \nexpected: {display(query)}"
        assert u.fragment  == tokenize(fragment),  f"\ngot:      {display(u.fragment)} \nexpected: {display(fragment)}"
    except AssertionError as err:
        print(err)
        raise URLParsingTestException(f"URL was parsed wrong: {url}\n{u.get_comparison(scheme,authority,userinfo,username,password,hostname,port,path,query,fragment)}")



if __name__ == "__main__":
    print("Testing RFC URL Parser")
    
    # Empty URL
    testparse(b"",      shouldfail=True, error_must_contain="URL was empty")
    testparse(None,     shouldfail=True, error_must_contain="URL was None")
    print("+ Passed empty URLs")

    # URL that is not raw bytes
    testparse("https://example.com",     shouldfail=True, error_must_contain="URL was of type")
    testparse(100,                       shouldfail=True, error_must_contain="URL was of type")
    testparse(["https://example.com"],   shouldfail=True, error_must_contain="URL was of type")
    print("+ Passed invalid input types")

    # Invalid Bytes in URL
    testparse(b"\x00", shouldfail=True, error_must_contain="Invalid byte found in URL")
    testparse(b"\xff", shouldfail=True, error_must_contain="Invalid byte found in URL")
    testparse(b"\x01", shouldfail=True, error_must_contain="Invalid byte found in URL")
    testparse(b"\x1a", shouldfail=True, error_must_contain="Invalid byte found in URL")
    testparse(b"{",    shouldfail=True, error_must_contain="Invalid byte found in URL")
    print("+ Passed URLs with invalid octets")

    # URLs with invalid syntax
    testparse(b"http://userbog:yep@m@e.example-.com/hi./../no.html?z&&&#yeah",       shouldfail=True, error_must_contain="literal @")
    testparse(b"http://userbog:yep@me.example-.com:80:80/hi./../no.html?z&&&#yeah",  shouldfail=True, error_must_contain="1 ':' max")
    testparse(b"http://userbog:yep@m%e.example-.com:80/hi./../no.html?z&&&#yeah",    shouldfail=True, error_must_contain="A % was not followed by two hex digits")
    testparse(b"http://userbog:yep@me.example-.com:80b/hi./../no.html?z&&&#yeah",    shouldfail=True, error_must_contain="Port contains invalid byte")
    testparse(b"http://userbog:yep@me.example-.com:80/hi./../no.%A2html?z&&&#ye#ah", shouldfail=True, error_must_contain="Fragment contains invalid byte")
    testparse(b"http://userbog:yep@me.example-.com:80/hi./../no.%A2html?z&[&&#yeah", shouldfail=True, error_must_contain="Query contains invalid byte")
    testparse(b"http://?z&&&#yeah",                                                   shouldfail=True, error_must_contain="HTTP and HTTPS do not allow an empty authority")
    testparse(b"http://:443?z&&&#yeah",                                               shouldfail=True, error_must_contain="HTTP and HTTPS do not allow an empty hostname")
    testparse(b"https://[2001:0db8:85a3::0000:8a2e:1.1.1.1.1]",                       shouldfail=True, error_must_contain="Impossible number of '.' to be an IPv6 Address")
    testparse(b"https://[2001:0db8:85a3::FFFFF:8a2e:1.1.1.1]",                        shouldfail=True, error_must_contain="IPv6 Segments cannot have longer than 4 hex chars")
    testparse(b"https://[2001:0db8:85a3::FFFX:8a2e:1.1.1.1]",                         shouldfail=True, error_must_contain="Could not parse an IPv6 segment as a hex integer")
    testparse(b"https://1.256.1.1]",                                                  shouldfail=True, error_must_contain="nvalid byte for a reg_name")
    testparse(b"https://[2001:0db8:85a3::FFFa:8a2e:1.256.1.1]",                       shouldfail=True, error_must_contain="integer out of bounds")
    testparse(b"https://[2001:0db8:85a3::FFFa:8a2e:-1.255.1.1]",                      shouldfail=True, error_must_contain="integer out of bounds")
    testparse(b"https://1.256.1.1]",                                                  shouldfail=True, error_must_contain="nvalid byte for a reg_name")

    # Valid Absolute URLs
    testparse(
        b"http://userbog:yep@me.example-.com/hi./../no.html?z&&&#yeah",
        scheme=b"http",
        port=None,
        query=b"z&&&",
        hostname=b"me.example-.com",
        authority=b"userbog:yep@me.example-.com",
        userinfo=b"userbog:yep",
        fragment=b"yeah",
        path=b"/hi./../no.html"
    )
    testparse(
        b"http://userbog:yep@-/hi./../no.html?z&&&#yeah",
        scheme=b"http",
        port=None,
        query=b"z&&&",
        hostname=b"-",
        authority=b"userbog:yep@-",
        userinfo=b"userbog:yep",
        fragment=b"yeah",
        path=b"/hi./../no.html"
    )
    testparse(
        b"http://userbog:yep@a:/hi./../no.html?z&&&#yeah",
        scheme=b"http",
        port=b"",
        query=b"z&&&",
        hostname=b'a',
        authority=b"userbog:yep@a:",
        userinfo=b"userbog:yep",
        fragment=b"yeah",
        path=b"/hi./../no.html"
    )
    testparse(
        b"http://user%99bog:yep@exam%f9ple.com:443/h%FFi./../no.html?z&&%42&#y%00eah",
        scheme=b"http",
        port=b"443",
        query=b"z&&%42&",
        hostname=b"exam%f9ple.com",
        authority=b"user%99bog:yep@exam%f9ple.com:443",
        userinfo=b"user%99bog:yep",
        fragment=b"y%00eah",
        path=b"/h%FFi./../no.html"
    )
    testparse(
        b"http://userbog:yep@example.com:000000000000000000000000000000000000000000000000000000000000000000000000000443/h%FFi./../no.html?z&&%42&#y%00eah",
        scheme=b"http",
        port=b"000000000000000000000000000000000000000000000000000000000000000000000000000443",
        query=b"z&&%42&",
        hostname=b"example.com",
        authority=b"userbog:yep@example.com:000000000000000000000000000000000000000000000000000000000000000000000000000443",
        userinfo=b"userbog:yep",
        fragment=b"y%00eah",
        path=b"/h%FFi./../no.html"
    )    
    testparse(
        b"http://userbog:yep@[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:42/h%FFi./../no.html?z&&%42&#y%00eah",
        scheme=b"http",
        port=b"42",
        query=b"z&&%42&",
        hostname=b"2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        authority=b"userbog:yep@[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:42",
        userinfo=b"userbog:yep",
        fragment=b"y%00eah",
        path=b"/h%FFi./../no.html"
    )
    testparse(
        b"http://userbog:yep@[2001:0db8:85a3::0000:8a2e:0370:7334]:42/h%FFi./../no.html?z&&%42&#y%00eah",
        scheme=b"http",
        port=b"42",
        query=b"z&&%42&",
        hostname=b"2001:0db8:85a3::0000:8a2e:0370:7334",
        authority=b"userbog:yep@[2001:0db8:85a3::0000:8a2e:0370:7334]:42",
        userinfo=b"userbog:yep",
        fragment=b"y%00eah",
        path=b"/h%FFi./../no.html"
    )
    testparse(
        b"https://[2001:0db8:85a3::0000:8a2e:1.1.1.1]",
        scheme=b"https",
        port=None,
        query=None,
        hostname=b"2001:0db8:85a3::0000:8a2e:1.1.1.1",
        authority=b"[2001:0db8:85a3::0000:8a2e:1.1.1.1]",
        userinfo=None,
        fragment=None,
        path=b""
    )


    # Valid Relative URLs
    # TODO WON'T IMPLEMENT


    print("pass")

