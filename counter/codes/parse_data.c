#include <stdio.h>
#include <stdlib.h>
#include <string.h>



unsigned char * parse_data(char *raw_data, int size){
    unsigned char mask1 = 0b00001111;
    unsigned char mask2 = 0b11110000;
    char *buffer_parse =  malloc(2*size*sizeof(char));

    for(int i=0; i<size; i++){
        buffer_parse[2*i+1] = raw_data[i]&mask1;
        buffer_parse[2*i] = (raw_data[i]&mask2)>>4;
    }
    return buffer_parse;
}


void freeptr(void *fptr){
    free(fptr);
}




