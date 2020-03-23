#include <stdio.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <string.h>
#include <sys/uio.h>

#define BUF_SIZE 256
#define ENTRY_OFFSET 6 //offset is 6 because of the strlen("Name") or strlen("PPid") = 4 + ':' + '<space>' in status file
#define PROC_DIRECTORY "/proc/"

// usage example:
// ./read_cgroup <path/to/save/directory> <path/to/tasks/file>
// example:
// ./read_cgroup . /sys/fs/cgroup/freezer/tasks
// will create file group_list.csv in current directory
int main (int argc, char* argv[]) {
    if (argc < 3) {
        perror("Not enough parameters, provide path\n");
        exit(EXIT_FAILURE);
    }

    char save_path[BUF_SIZE] = "";
    strcat(save_path, argv[1]);
    strcat(save_path, "/group_list.csv");
    FILE* save_file = fopen(save_path, "w");
    char pid[BUF_SIZE];

    FILE* tasks_file = fopen(argv[2], "r");

    char open_path[BUF_SIZE] = "";
    char process_name[BUF_SIZE]= "";
    char parent_pid[BUF_SIZE]= "";
    char tmp[BUF_SIZE]= "";
    char* entry;

    while (fgets(pid, BUF_SIZE, tasks_file)) {
        // remove \n at the end of pid
        pid[strcspn(pid, "\r\n")] = 0;
        strcat(open_path, PROC_DIRECTORY);
        strcat(open_path, pid);
        strcat(open_path, "/status");

        FILE* status_file = fopen(open_path, "r");

        while (fgets(tmp, BUF_SIZE, status_file)) {
            //collect data
            if((entry = strstr(tmp, "Name")))
                sscanf(entry + ENTRY_OFFSET,"%[^\n]s", process_name);

            if((entry = strstr(tmp, "PPid")))
                sscanf(entry + ENTRY_OFFSET,"%[^\n]", parent_pid);
        }

        fprintf(save_file, "%s,%s,%s\n" ,pid, parent_pid, process_name);

        process_name[0] = '\0';
        parent_pid[0] = '\0';
        tmp[0] = '\0';
        open_path[0] = '\0';

        fclose(status_file);
    }

    fclose(save_file);
    fclose(tasks_file);
    return 0;
}
