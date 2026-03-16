/* ʕ ᵔᴥᵔ ʔ */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include "learn_english.h"

void free_vector(VECTOR *v) {
    for (int i = 0; i < v->size; ++i)
    {
        free(v->data[i]);   
    }
    free(v);
}

VECTOR *init_vector() {
    VECTOR *v = (VECTOR *)malloc(sizeof(VECTOR));
    if(v == NULL) {
        printf("EROR:%d\n", __LINE__);
    }
    v->size = 0;
    v->capacity = INIT_CAPACITY;

    if(INIT_CAPACITY > 0) {
        v->data = (WORDS **)calloc(INIT_CAPACITY, sizeof(WORDS*));
        if(v->data == NULL){
            printf("EROR:%d\n", __LINE__);
            free(v);
            exit(1);
        }
    }
    else {
        printf("EROR: capacity <= 0\n");
        exit(1);
    }

    return v;
}

void realloc_vector(VECTOR *v) {
    int new_capacity = v->capacity * 2;
    
    WORDS **new_data = realloc(v->data, new_capacity * sizeof(WORDS*));
    if(new_data == NULL) {
            printf("EROR:%d\n", __LINE__);
            exit(1);        
    }
    v->data = new_data;
    v->capacity = new_capacity;
}

VECTOR *init_array_structs(FILE *file) {
    VECTOR *v = init_vector();
    int c;
    int count = 0;

    while((c = fgetc(file)) != EOF) {
        if (c == '\r' || c == '\n'){
            continue;
        }
        if (v->size >= v->capacity) {
            realloc_vector(v);
        }
        WORDS *ptr = (WORDS *)malloc(sizeof(WORDS));
        if(ptr == NULL) 
        {
            printf("EROR:%d\n", __LINE__);
            exit(1);
        }

        while ((c != '|') && (c != '\n') && (c != EOF))
        {
            ptr->eng_word[count] = (char)c;
            c = fgetc(file);
            count++;
        }
        ptr->eng_word[count] = '\0';
        count = 0;

        if(c == '|') {
            c = fgetc(file);
        }

        while (c != '\n' && c != EOF)
        {
            ptr->ru_word[count] = (char)c;
            c = fgetc(file);
            count++;
        }   
        ptr->ru_word[count] = '\0';
        count = 0;

        v->data[v->size] = ptr;
        v->size++;
    }

    return v;

}