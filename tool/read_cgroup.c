#include <stdio.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <string.h>
#include <sys/uio.h>

#define BUF_SIZE 256
#define PROC_DIRECTORY "/proc/"

// usage example:
// ./readPids <path/to/save/directory> <path/to/tasks/file>
// example:
// ./readPids . /sys/fs/cgroup/freezer/tasks
// will create file group_list.csv in current directory
int main (int argc, char* argv[])
{

    if(argc < 3)
    {
        perror("Not enough parameters, provide path\n");
        exit(EXIT_FAILURE);
    }

    char save_path[BUF_SIZE] = "";
    strcat(save_path, argv[1]);
    strcat(save_path, "/group_list.csv");
    FILE* save_file = fopen(save_path, "w");
    char pid[BUF_SIZE];

    FILE* tasksFile = fopen(argv[2], "r");

    char open_path[BUF_SIZE] = "";
    char process_name[BUF_SIZE]= "";
    char parent_pid[BUF_SIZE]= "";
    char tmp[BUF_SIZE]= "";
    char* entry;

    while (fgets(pid, BUF_SIZE, tasksFile))
    {
        // remove \n at the end of pid
        pid[strcspn(pid, "\r\n")] = 0;
        strcat(open_path, PROC_DIRECTORY);
        strcat(open_path, pid);
        strcat(open_path, "/status");

        FILE* statusFile = fopen(open_path, "r");

        while(fgets(tmp, BUF_SIZE, statusFile)) //here we read line
        {
            //collect data
            if((entry = strstr(tmp, "Name")))
                sscanf(entry+6,"%[^\n]s", process_name); //offset is 6 because of the strlen("Name") = 4 + ':' + '<space>' in status file
            if((entry = strstr(tmp, "PPid")))
                sscanf(entry+6,"%[^\n]", parent_pid); //same for "PPid"
        }

        fprintf(save_file, "%s,%s,%s\n" ,pid, parent_pid, process_name);

        process_name[0] = '\0';
        parent_pid[0] = '\0';
        tmp[0] = '\0';
        open_path[0] = '\0';

        fclose(statusFile);
    }

    fclose(save_file);
    fclose(tasksFile);
}

