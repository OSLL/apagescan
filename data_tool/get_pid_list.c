#include <stdio.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define BUF_SIZE 256
#define PROC_DIRECTORY "/proc/"

int str_is_digit(const char *str){
    unsigned int i = 0;
    for (; isdigit(str[i]); i++);
    return i == strlen(str);
}

// usage example:
// ./get_pid_list <path/to/directory>
// example:
// ./get_pid_list .
// will create file pid_list.csv in current directory
int main (int argc, char* argv[]) {
    if(argc < 2){
        perror("Not enough parameters, provide path\n");
        exit(EXIT_FAILURE);
    }

    struct dirent* dir_info = NULL;
    DIR* dir_proc = NULL;

    char save_path[BUF_SIZE] = "";
    strcat(save_path, argv[1]);
    strcat(save_path, "/pid_list.csv");
    FILE* result = fopen(save_path, "w");

    dir_proc = opendir(PROC_DIRECTORY);

    char pid_name_path[BUF_SIZE] = "";
    char pid_raw_name[BUF_SIZE] = "";
    FILE* fname;

    while ((dir_info = readdir(dir_proc))) {
        if (dir_info->d_type == DT_DIR && str_is_digit(dir_info->d_name)) {
            sprintf(pid_name_path, "/proc/%s/cmdline", dir_info->d_name);
            fname = fopen(pid_name_path, "r");
            fscanf(fname, "%s", pid_raw_name);

            char pid_name[BUF_SIZE] = "";
            char *pid_cut_name = strrchr(pid_raw_name, '/');
            if (pid_cut_name == NULL) {
                strcpy(pid_name, pid_raw_name);
            } else {
                strcpy(pid_name, pid_cut_name + sizeof(char));
            }
            fprintf(result, "%s,%s\n", dir_info->d_name, pid_name);
            fclose(fname);
        }
    }
    fclose(result);
    closedir(dir_proc);
    return 0;
}
