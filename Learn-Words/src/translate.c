/* ʕ ᵔᴥᵔ ʔ */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include "learn_english.h"

void print (VECTOR *ptr, int count, int correct) {
    system("clear");
    
    for (int i = 0; i < count; i++)
    {
        printf("-----\n");
        printf("ENG: %s\nRU: %s\nUSER:%s\nRESULT: %c\n\n", ptr->data[i]->eng_word, ptr->data[i]->ru_word, ptr->data[i]->user_word, ptr->data[i]->comparison_result);
    }
    printf("Correct: %d/%d\n--- %.1f ---\n", correct, count, (((float)correct/(float)count) * (float)100));
} 

int oral_translation(VECTOR *v) {
	char *check;
	char buffer[2];

	while(1) {
		for (int i = 0; i < v->size; i++) 
		{	
			system("clear"); 
			printf("Введите 'q' для выхода\n");
			printf("-----\n");

			printf("%s\n", v->data[i]->ru_word);
			check = fgets(buffer, sizeof(buffer), stdin);
			if (check == NULL)
			{
				printf("EROR: %d\n",__LINE__);
			}
			
			if(buffer[0] == '\n') {
				printf("%s\n", v->data[i]->eng_word);
				check = fgets(buffer, sizeof(buffer), stdin);
				if (check == NULL)
				{
					printf("EROR: %d\n",__LINE__);
				}	
				if(buffer[0] == '\n') {
					continue;
				}
			}

			buffer[strcspn(buffer, "\n")] = '\0';

			if(strcmp(buffer, "q") == 0){
				return 0;
			}		
		}
	}

	return 0;	
}

int random_wrtitten_translation(VECTOR *v) {
	
	VECTOR *ptr = init_vector();
	char *check;
	int count = 0;
	int correct = 0;
	int random;

	srand(time(NULL));

	for (int i = 0; i < v->size; i++) 
	{	
		if (ptr->size >= ptr->capacity) {
            realloc_vector(ptr);
        }

        random = rand() % v->size;

		system("clear"); 
		printf("Ведите 'q' для выхода\n");
		printf("-----\n");

		printf("%s\n", v->data[random]->ru_word);
		check = fgets(v->data[random]->user_word, SIZE_WORD, stdin);
		if (check == NULL)
		{
			printf("EROR: %d\n",__LINE__);
		}
		v->data[random]->user_word[strcspn(v->data[random]->user_word, "\n")] = '\0';

		ptr->data[i] = v->data[random];

		if(strcmp(v->data[random]->user_word, "q") == 0){
			print(ptr, count, correct);
			free_vector(ptr);
			return 0;
		}		

		if(strcmp(v->data[random]->user_word, v->data[random]->eng_word) == 0) {
			v->data[random]->comparison_result = '+';
			correct++;
		}
		else {
			v->data[random]->comparison_result = '-';
		}
		count ++;
		ptr->size++;
	}
	print(ptr, count, correct);
	free(ptr);

	return 0;	
}

int translate(VECTOR *v) {
	int user_choice = 0;

	while(1) {
		printf("1) Писменный(random0\n2) Устный(обычный)\n3) Выход\n");
		printf("Выберите режим перевода: ");
		scanf("%d", &user_choice);
		getchar();

		switch(user_choice)
		{
			case 1:
				random_wrtitten_translation(v);
				break;
			case 2:
				oral_translation(v);
				break;
			case 3:
				return 0;
		}
	}
}