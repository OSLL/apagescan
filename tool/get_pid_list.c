#include <stdio.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 256
#define PROC_DIRECTORY "/proc/"

int IsNumeric (const char* ccharptr_CharacterList)
{
    for ( ; *ccharptr_CharacterList; ccharptr_CharacterList++)
        if (*ccharptr_CharacterList < '0' || *ccharptr_CharacterList > '9')
            return 0;
    return 1;
}

// usage example:
// ./readPids <path/to/directory>
// example:
// ./readPids .
// will create file pid_list.csv in current directory
int main (int argc, char* argv[])
{
    if(argc < 2)
    {
        perror("Not enough parameters, provide path\n");
        exit(EXIT_FAILURE);
    }

    struct dirent* dirEntity = NULL;
    DIR* dir_proc = NULL;

    char save_path[BUF_SIZE] = "";
    strcat(save_path, argv[1]);
    strcat(save_path, "/pid_list.csv");
    FILE* f = fopen(save_path, "w");

    dir_proc = opendir(PROC_DIRECTORY);

    char pid_name_path[BUF_SIZE];
    char name[BUF_SIZE];
    FILE* fname;

    while ((dirEntity = readdir(dir_proc)) != 0)
    {
        if (dirEntity->d_type == DT_DIR)
        {
            if (IsNumeric(dirEntity->d_name))
            {
                sprintf(pid_name_path, "/proc/%s/cmdline", dirEntity->d_name);
                fname = fopen(pid_name_path, "r");
                fscanf(fname, "%s", name);

                char cutName[BUF_SIZE];
                char *p = strrchr(name, '/');
                if (p == NULL)
                    strcpy(cutName, name);
                else
                    strcpy(cutName, p+sizeof(char));
                fprintf(f, "%s,%s\n", dirEntity->d_name, cutName);
                fclose(fname);
            }
        }
    }

    fclose(f);
    closedir(dir_proc);
    return 0;
}