#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <curl/curl.h>
//#include <libb64.h>
#include "base64.c"

int GLOB;

//https://stackoverflow.com/questions/779875/what-function-is-to-replace-a-substring-from-a-string-in-c
// You must free the result if result is non-NULL.
char *str_replace(char *orig, char *rep, char *with) {
    char *result; // the return string
    char *ins;    // the next insert point
    char *tmp;    // varies
    int len_rep;  // length of rep (the string to remove)
    int len_with; // length of with (the string to replace rep with)
    int len_front; // distance between rep and end of last rep
    int count;    // number of replacements

    // sanity checks and initialization
    if (!orig || !rep)
        return NULL;
    len_rep = strlen(rep);
    if (len_rep == 0)
        return NULL; // empty rep causes infinite loop during count
    if (!with)
        with = "";
    len_with = strlen(with);

    // count the number of replacements needed
    ins = orig;
    for (count = 0; tmp = strstr(ins, rep); ++count) {
        ins = tmp + len_rep;
    }

    tmp = result = malloc(strlen(orig) + (len_with - len_rep) * count + 1);

    if (!result)
        return NULL;

    // first time through the loop, all the variable are set correctly
    // from here on,
    //    tmp points to the end of the result string
    //    ins points to the next occurrence of rep in orig
    //    orig points to the remainder of orig after "end of rep"
    while (count--) {
        ins = strstr(orig, rep);
        len_front = ins - orig;
        tmp = strncpy(tmp, orig, len_front) + len_front;
        tmp = strcpy(tmp, with) + len_with;
        orig += len_front + len_rep; // move to next "end of rep"
    }
    strcpy(tmp, orig);
    return result;
}

char * esc(char * s) {

	//printf("Gonna esc now:\n%s\n", s);fflush(stdout);

	int * len = &GLOB;	
	char* encoded = base64_encode(s, strlen(s), len);

	//printf("Pixed:\n%s\n", s);fflush(stdout);

	return encoded;
}


int do_error(char * s, int ret) {
	fprintf(stderr, "{'errors' : '%s'}", s);
	return ret;
}

int main(int argc, char** argv) {

		//printf("Parser running\n");fflush(stdout);
		

		char* url_b64 = NULL;
		long int url_b64_len = 0;

		char* url_decoded = NULL;
		long int url_len = 0;

		if (argc != 2) {
			fprintf(stderr, "Expected 2 args, but got %d\n", argc);
			return 1;
		}

		//if (strcmp("testing", argv[1]) == 0) {
			//printf("Running the test...\n");
			//url_b64 = "aHR0cHM6Ly9zdGFjazpleGNoYW5nZUBtZS1mYi5jb20vZmVlL2ZlZS5jb207eWVzLW5vLDEmeWVhaD9mb29iYXI9NSZ5ZXM7OyN0aGluZw==\n";
		//	url_b64 = "aHR0cHM6Ly9uLnByxKxhYS12ZXI0NS5jby51ay9hL2IuYz9hPTEmYj0zLDQjZnJhZw==\n";
		//	url_b64_len = strlen(url_b64);
		//} else {
			int getline_res = getline(&url_b64, &url_b64_len, stdin);
			if (getline_res <= 0) {
				fprintf(stderr,"Could not read url from stdin");
				return(2);
			}	
			//printf("I got a url: %s \nLength was %d\n", url_b64, getline_res);fflush(stdout);
		//}	
	
		int test = strlen(url_b64);

		//https://www.mycplus.com/source-code/c-source-code/base64-encode-decode/	
		url_decoded = base64_decode(url_b64, getline_res-1, &url_len);

		if (test != strlen(url_b64)) {
			printf("Base64decode has failed us!!!!!!!!!!!!!!!!!!!!!!!\n");fflush(stdout);
		}

		if (url_decoded == NULL) {
			fprintf(stderr, "URL b64-decoded to null!");
			return 5;
		}

		if (strcmp("testing", argv[1]) == 0) {
			fprintf(stdout,"From %s \nI got a url of length %d\n%s\n", url_b64, url_len, url_decoded);fflush(stdout);
		}

		char * error_str = "";
		CURLU *h = curl_url();
		if (h == NULL) {
			return do_error("Failed to make curl_url object", 1);
		}
		CURLUcode rc;

		rc = curl_url_set(h, CURLUPART_URL, url_decoded, 0);
		if (rc) {
			printf("libcurl4-openssl\t\t\t\t\t\t\t\t\tError Parsing URL: code %d\n",rc);fflush(stdout);
			return 0;
			//fprintf(stderr, "Error parsing URL %d", (int) rc);
		}

		char * scheme = NULL;
		char * host = NULL;
		char * user = NULL;
		char * password = NULL;
		char * port = NULL;
		char * path = NULL;
		char * query = NULL;
		char * fragment = NULL;

		rc = curl_url_get(h, CURLUPART_HOST, &host, 0);
		if (rc) {
			host = NULL;
			//fprintf(stderr, "Error getting host %d", (int) rc);
			//sprintf(buff, "error: %d", rc);
		}
		rc = curl_url_get(h, CURLUPART_SCHEME, &scheme, 0);
		if (rc) {
			scheme = NULL;
			//scheme = sprintf("error: %d", rc);
		}
		rc = curl_url_get(h, CURLUPART_USER, &user, 0);
		if (rc) {
			user = NULL;
			//user = sprintf("error: %d", rc);
		}
		rc = curl_url_get(h, CURLUPART_PASSWORD, &password, 0);
		if (rc) {
			password = NULL;
			//password = sprintf("error: %d", rc);
		}
		rc = curl_url_get(h, CURLUPART_PORT, &port, 0);
		if (rc) {
			port = NULL;
			//port = sprintf("error: %d", rc);
		}
		rc = curl_url_get(h, CURLUPART_PATH, &path, 0);
		if (rc) {
			path = NULL;
			//path = sprintf("error: %d", rc);
		}
		rc = curl_url_get(h, CURLUPART_QUERY, &query, 0);
		if (rc) {
			query = NULL;
			//query = sprintf("error: %d", rc);
		}
		rc = curl_url_get(h, CURLUPART_FRAGMENT, &fragment, 0);
		if (rc) {
			fragment = NULL;
			//fragment = sprintf("error: %d", (int) rc);
		}

		//switch(url_struct->scheme) {
		//	case SCHEME_HTTP:
		//		scheme = "http";
		//		break;
		//	case SCHEME_HTTPS:
		//		scheme = "https";
		//		break;
		//	case SCHEME_FTP:
		//		scheme = "ftp";
		//		break;
		//	case SCHEME_FTPS:
		//		scheme= "ftps";
		//		break;
		//	case SCHEME_INVALID:
		//		scheme= "other";
		//		break;
		//}

		char authority[1024];
		authority[0] = '\0';
		char userinfo[1024];
		userinfo[0] = '\0';

		if (user) {
			if (strcmp("testing", argv[1]) == 0) {
				fprintf(stdout,"Found a username\n");
			}
			strcat(authority, user);
			strcat(userinfo,  user);
		}
		if (password) {
			if (strcmp("testing", argv[1]) == 0) {
				fprintf(stdout,"Found a password\n");
			}
			strcat(authority, ":");
			strcat(userinfo,  ":");
			strcat(authority, password);
			strcat(userinfo,  password);
			strcat(authority, "@");
		}
		if (host) {
			if (strcmp("testing", argv[1]) == 0) {
				fprintf(stdout,"Found a host: %s\n", host);
			}
			strcat(authority, host);
		}
		if (port) {
			strcat(authority, ":");
			strcat(authority, port);
		}


		printf("l233 now\n");fflush(stdout);



		if (strcmp("testing", argv[1]) == 0) {
			fprintf(stdout,"Username was %s\n", userinfo);
		}

		printf("libcurl4-openssl\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n",
			scheme   ? esc(scheme)         : "",
			esc(authority),
			esc(userinfo),
			host     ? esc(host)           : "",
		    port     ? esc(port)           : "",
			path     ? esc(path)	       : "",
			query    ? esc(query)	       : "",
			fragment ? esc(fragment)       : ""
		);


		printf("Serialized\n");fflush(stdout);


		return 0;
}


