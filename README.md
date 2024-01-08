# equivocal-urls
Code for comparing 15 different URL parsers, looking for URLs which equivocate on their hostname depending on the parser used to read them.

I wrote this code for the paper "[Equivocal URLs: Understanding the Fragmented Space of URL Parser Implementations](https://link.springer.com/chapter/10.1007/978-3-031-17143-7_9)" which won a Best Paper award at ESORICS 2022.

My co-authors were Adam Bates from UIUC and Michael Bailey from GA Tech.

## Setup & Dependencies

To run the tester, start by running final_fuzzer/fuzzer.py which will try to build each parser. Deal with failures by installing the required programming languages or libraries.

Depending on your git settings, you may need to go in and set the precompiled binaries to be executable.

If you are testing on a debian system, you will need at least 
- NodeJS, 
- Golang,
- URLX go module 
- PHP, 
- Java, 
- libcurl4-openssl-dev from apt, 
- furl from pip3, 
- uuid-dev from apt
- libpcre3-dev from apt
- libidn2-dev from apt.

