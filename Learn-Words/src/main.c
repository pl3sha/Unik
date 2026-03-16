/* ʕ ᵔᴥᵔ ʔ */
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include "learn_english.h"

int main(int argc, char *argv[]) {
    if(argc != 2) {
        printf("EROR: Добавьте словарь");
        return 0;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file) {
        printf("EROR: %d %s", __LINE__, __func__);
        perror("fopen");
        return 1;
    }
    VECTOR *v = init_array_structs(file);
    fclose(file);

    int user_choice;

    while(1) {
        system("clear");
        printf("1) Перевод\n2) Выход из программы\n");
        printf("Введите номер режима: ");
        scanf("%d", &user_choice);

        switch(user_choice)
        {
            case 1:
                translate(v);
            break;
            case 2:
                return 0;
        }
    }
    
    free_vector(v);
    return 0;
}