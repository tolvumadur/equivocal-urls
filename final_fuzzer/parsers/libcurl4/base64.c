#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
 
static char encoding_table[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                '4', '5', '6', '7', '8', '9', '+', '/'};
static char *decoding_table = NULL;
static int mod_table[] = {0, 2, 1};
 
void build_decoding_table() {
 
    decoding_table = malloc(256);
 
    for (int i = 0; i < 64; i++)
        decoding_table[(unsigned char) encoding_table[i]] = i;
}
 
 
void base64_cleanup() {
    free(decoding_table);
} 
 
char *base64_encode(const unsigned char *data,
                    size_t input_length,
                    size_t *output_length) {

    *output_length = 4 * ((input_length + 2) / 3);

    char *encoded_data = malloc(*output_length+1);
    if (encoded_data == NULL) return NULL;

    
 
    for (int i = 0, j = 0; i < input_length;) {
 
        uint32_t octet_a = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_b = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_c = i < input_length ? (unsigned char)data[i++] : 0;
 
        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;
 
        encoded_data[j++] = encoding_table[(triple >> 3 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 2 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 1 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 0 * 6) & 0x3F];
    }
 
    for (int i = 0; i < mod_table[input_length % 3]; i++)
        encoded_data[*output_length -1 - i] = '=';
 

    encoded_data[*output_length] = '\0';

    

    return encoded_data;
}
 
void snip(char * data, long unsigned int * input_length) {
	data[(*input_length)---1] = 0;
}

unsigned char *base64_decode(char *data,
                             size_t input_length,
                             size_t *output_length) {
 
    if (decoding_table == NULL) build_decoding_table();

    if (data==NULL) {
	fprintf(stderr,"Input to b64 decoder was null.");
	return NULL;
    }

    while (data[input_length-1] == 0) {
	    snip(data, &input_length);
    }

    //while (data[input_length-1] == '\\' || data[input_length-1] == 'n' || data[input_length-1] == '\n' || data[input_length-1] == 0 || data[input_length-1] > 0x7F)  {
    while (data[input_length-1] == '\n' || data[input_length-1] == 0 || data[input_length-1] > 0x7F)  {
	//fprintf(stderr, "snipping ...%s (%ld chars); last=%d", data+input_length-5, input_length, data[input_length-1]);
	snip(data, &input_length);
	//fprintf(stderr, "snippid ...%s (%ld chars) last=%d,%d; ", data+input_length-5, input_length, data[input_length-1], data[input_length]);
    }



    while (input_length % 4 != 0) 
    {
	    //if (1){//data[input_length - 1]) {
		//input_length--;
		
		//char* end = data + input_length - 1;
		//fprintf(stderr, "Trying to fix string %s << yeah %ld; ", end-10, input_length);
		
		//*end = 0;
		snip(data,&input_length);
		//fprintf(stderr, "Now it ends: %s; ", data + input_length - 10);
		
	    //} 
	    //else {
	   // 	fprintf(stderr, "b64 input length was %ld", input_length);
	    	//fprintf(stderr, "\n %s \n", data[input_length-1]);
	   // 	return NULL;
	   // }

    }

 
    *output_length = input_length / 4 * 3;
    if (data[input_length - 1] == '=') (*output_length)--;
    if (data[input_length - 2] == '=') (*output_length)--;
 
    unsigned char *decoded_data = malloc(*output_length+1);
    if (decoded_data == NULL) return NULL;
 
    for (int i = 0, j = 0; i < input_length;) {
 
        uint32_t sextet_a = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_b = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_c = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
        uint32_t sextet_d = data[i] == '=' ? 0 & i++ : decoding_table[data[i++]];
 
        uint32_t triple = (sextet_a << 3 * 6)
        + (sextet_b << 2 * 6)
        + (sextet_c << 1 * 6)
        + (sextet_d << 0 * 6);
 
        if (j < *output_length) decoded_data[j++] = (triple >> 2 * 8) & 0xFF;
        if (j < *output_length) decoded_data[j++] = (triple >> 1 * 8) & 0xFF;
        if (j < *output_length) decoded_data[j++] = (triple >> 0 * 8) & 0xFF;
    }
 
    decoded_data[*output_length] = '\0';
    return decoded_data;
}
