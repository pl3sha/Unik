/* ʕ ᵔᴥᵔ ʔ */
#ifndef LEARN_ENGLISH_H
#define LEARN_ENGLISH_H

#define SIZE_WORD 128
#define INIT_CAPACITY 25

typedef struct
{   
    char eng_word[SIZE_WORD];
    char ru_word[SIZE_WORD];
    char user_word[SIZE_WORD];
    char comparison_result;
} WORDS;

typedef struct 
{
    WORDS **data;
    int size;
    int capacity;
} VECTOR;

void free_vector(VECTOR *v);
VECTOR *init_vector();
void realloc_vector(VECTOR *v);
VECTOR *init_array_structs(FILE *file);

int translate(VECTOR *v);
int random_wrtitten_translation(VECTOR *v);
int oral_translation(VECTOR *v);
#endif