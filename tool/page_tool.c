#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <limits.h>
#include "page_tool.h"

AddrPair *addr_data;
PageInfo *pages_data;
const char *pid_str;

//function reads an 64-bit number from file
uint64_t read_u64(int fd, unsigned long offset) {
    unsigned long nread;
    uint64_t data;
    nread = pread(fd, &data, sizeof(uint64_t), (off_t)(offset) * sizeof(uint64_t));
    if (nread < sizeof(uint64_t)) {
        perror("Error with reading u64\n");
        exit(EXIT_FAILURE);
    }
    return data;
}

//function initializes an array of AddrPair structures  and fills it with pairs of block's start and end addresses
unsigned long parse_maps_blocks(AddrPair **addresses, FILE *maps_fp) {
    if (*addresses != NULL) {
        perror("Addresses pointer should be NULL before calling parse_blocks()\n");
        exit(EXIT_FAILURE);
    }
    unsigned long size = INIT_ARR_SIZE;
    *addresses = (AddrPair *) malloc(size * sizeof(AddrPair));
    unsigned long counter = 0;
    char buffer[BUF_SIZE] = "";

    unsigned long vm_start;
    unsigned long vm_end;
    unsigned long long pgoff;
    int major, minor;
    char r, w, x, s;
    unsigned long ino;
    int values_count;

    while (fgets(buffer, sizeof(buffer), maps_fp)) {
        if (counter == size - 1) {
            size *= RESIZE_C;
            *addresses = (AddrPair *) realloc(*addresses, size * sizeof(AddrPair));
        }
        values_count = sscanf(buffer, "%lx-%lx %c%c%c%c %llx %x:%x %lu", &vm_start,
                              &vm_end,
                              &r, &w, &x, &s,
                              &pgoff,
                              &major, &minor,
                              &ino);
        (*addresses)[counter].begin = vm_start;
        (*addresses)[counter].end = vm_end;
        if (values_count < 10) {
            fprintf(stderr, "unexpected line: %s\n", buffer);
            continue;
        }
        counter++;
        buffer[0] = '\0';
    }
    return counter;
}

unsigned long get_page_info_block(int page_fd,
                                  int flags_fd,
                                  PageInfo **pagemap,
                                  unsigned long block_size,
                                  uintptr_t vaddr,
                                  unsigned long pagemap_pos) {
    unsigned long nread;
    uint64_t data[block_size];
    nread = pread(page_fd, data, block_size * sizeof(uint64_t), (off_t)((vaddr / PAGE_SIZE) * sizeof(uint64_t)));

    unsigned long off = pagemap_pos;
    uint64_t flags_data;
    for (unsigned long i = 0; i < block_size; i++) {
        (*pagemap)[off + i].addr = vaddr + i * PAGE_SIZE;
        (*pagemap)[off + i].pfn = PFN(data[i]);
        (*pagemap)[off + i].file_page = PAGE_FILE(data[i]);
        (*pagemap)[off + i].shared_anon = (*pagemap)[off + i].file_page == 1 ? 0 : 1;
        (*pagemap)[off + i].swapped = PAGE_SWAPPED(data[i]);
        (*pagemap)[off + i].present = PAGE_PRESENT(data[i]);
        if ((*pagemap)[off + i].present == 1) {
            flags_data = read_u64(flags_fd, (*pagemap)[off + i].pfn);
            (*pagemap)[off + i].dirty = PAGE_DIRTY(flags_data);
            (*pagemap)[off + i].anon = PAGE_ANON(flags_data);
        } else {
            (*pagemap)[off + i].swap_offset = SWAP_OFFSET(data[i]);
            (*pagemap)[off + i].dirty = 0;
            (*pagemap)[off + i].anon = 0;
        }
    }
    return nread / sizeof(uint64_t);
}

//function initializes an array of PageInfo structures and fills it with info about each process's page
unsigned long get_pages_info(PageInfo **pages, AddrPair *addr_data, unsigned long addr_data_size, int page_fd, int flags_fd) {
    if (*pages != NULL) {
        perror("Pages pointer should be NULL before calling get_pages()\n");
        exit(EXIT_FAILURE);
    }
    unsigned long size = INIT_ARR_SIZE;
    *pages = (PageInfo *) malloc(size * sizeof(PageInfo));
    unsigned long pages_counter = 0;
    unsigned long block_size;
    unsigned long nread;
    for (unsigned long i = 0; i < addr_data_size; i++) {
        block_size = (addr_data[i].end - addr_data[i].begin) / PAGE_SIZE;
        if (pages_counter + block_size >= size - 1) {
            size = (unsigned long) (size + block_size + 1);
            *pages = (PageInfo *)realloc(*pages, size * sizeof(PageInfo));
        }
        nread = get_page_info_block(page_fd, flags_fd, pages, block_size, addr_data[i].begin, pages_counter);
        pages_counter += nread;
    }
    return pages_counter;
}

void create_data_file(PageInfo *data, unsigned long data_size, char *path_to_save) {
    char filename[BUF_SIZE] = "";
    strcat(filename, path_to_save);
    strcat(filename, "/");
    strcat(filename, pid_str);
    strcat(filename, "_page_data");
    printf("Path to saved data: %s\n", filename);
    FILE *result = fopen(filename, "w");

    if (result == NULL) {
        fprintf(stderr, "Error with creating %s\n", filename);
        exit(EXIT_FAILURE);
    }

    char file_buffer[CHUNK_SIZE];
    memset(file_buffer, 0, CHUNK_SIZE);
    unsigned long buffer_count = 0;
    unsigned long i = 0;

    uint64_t page_offset = 0;
    uint32_t flags_data = 0;
    while (i < data_size) {
        flags_data = 0;

        //skip pages filled with 0
        if (data[i].swapped || data[i].present) {
            INITIALIZE_CUSTOM_DIRTY(flags_data, data[i].dirty);
            INITIALIZE_CUSTOM_ANON(flags_data, data[i].anon);
            INITIALIZE_CUSTOM_PRESENT(flags_data, data[i].present);

            page_offset = data[i].present == 1 ? data[i].pfn : data[i].swap_offset;
            memcpy(file_buffer + buffer_count, &page_offset, sizeof(uint64_t));
            buffer_count += sizeof(uint64_t);
            memcpy(file_buffer + buffer_count, &flags_data, sizeof(uint32_t));
            buffer_count += sizeof(uint32_t);
        }
        i++;
        // if the chunk is big enough, write it.
        if (buffer_count >= CHUNK_SIZE) {
            fwrite(file_buffer, buffer_count, 1, result);
            buffer_count = 0;
            memset(file_buffer, 0, CHUNK_SIZE);
        }
    }
    // Write remainder
    if (buffer_count > 0) {
        fwrite(file_buffer, buffer_count, 1, result);
    }
    fclose(result);
}

//execute: ./a.out <pid> <path_to_save_data>
//example: ./page 8345 .
int main(int argc, char *argv[]) {
    if (argc < 3) {
        perror("Not enough parameters: pid or path wasn't provided by user\n");
        exit(EXIT_FAILURE);
    }
    pid_str = argv[1];
    char path[FILE_PATH_SIZE];
    int pid = atoi(pid_str);
    sprintf(path, "/proc/%d/maps", pid);

    FILE *fp = fopen(path, "r");
    if (fp == NULL) {
        perror("Error with opening a maps file");
        exit(EXIT_FAILURE);
    }

    addr_data = NULL;
    pages_data = NULL;

    unsigned long addr_data_size = parse_maps_blocks(&addr_data, fp);
    printf("Mapped blocks count: %ld\n", addr_data_size);
    fclose(fp);

    sprintf(path, "/proc/%d/pagemap", pid);
    int page_fd = open(path, O_RDONLY);
    if (page_fd < 0) {
        perror("Error with opening a pagemap file");
        exit(EXIT_FAILURE);
    }

    sprintf(path, "/proc/kpageflags");
    int flags_fd = open(path, O_RDONLY);
    if (flags_fd < 0) {
        perror("Error with opening a flags file");
        exit(EXIT_FAILURE);
    }

    unsigned long pages_data_size = get_pages_info(&pages_data, addr_data, addr_data_size, page_fd, flags_fd);

    printf("Pages scanned: %ld\n", pages_data_size);
    create_data_file(pages_data, pages_data_size, argv[2]);
    free(addr_data);
    free(pages_data);
    close(page_fd);
    close(flags_fd);
    return 0;
}
