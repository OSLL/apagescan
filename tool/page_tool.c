#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <inttypes.h>
#include <sys/types.h>
#include <limits.h>

#define FILE_PATH_SIZE 256
#define BUF_SIZE 1000
#define INIT_ARR_SIZE 1000
#define RESIZE_C 1.5
#define CHUNK_SIZE 4092 //4092 can be divided by 12 so buffer can contain info about 341 pages
#define PAGE_SIZE sysconf(_SC_PAGE_SIZE)

#define PFN(page) (page & 0x7FFFFFFFFFFFFF)            //first 54 bits
#define SWAP_OFFSET(page) (page & 0x7FFFFFFFFFFFE0) //5-54 bits

#define GET_FLAG(data, offset) ((data >> offset) & 1U)
#define PAGE_FILE(page) (GET_FLAG(page, 61))
#define PAGE_SWAPPED(page) (GET_FLAG(page, 62))
#define PAGE_PRESENT(page) (GET_FLAG(page, 63))

#define PAGE_DIRTY(flags_data) (GET_FLAG(flags_data, 4))
#define PAGE_ANON(flags_data) (GET_FLAG(flags_data, 12))

#define VALUE_BITMASK(value, offset) ((uint64_t)value << offset)
#define INITIALIZE_CUSTOM_DIRTY(custom_flags_data, value) (custom_flags_data |=  VALUE_BITMASK(value, 4))
#define INITIALIZE_CUSTOM_ANON(custom_flags_data, value) (custom_flags_data |=  VALUE_BITMASK(value, 12))
#define INITIALIZE_CUSTOM_PRESENT(custom_flags_data, value) (custom_flags_data |=  VALUE_BITMASK(value, 26))

typedef struct {
    unsigned long addr;
    uint64_t pfn;
    uint64_t swap_offset;
    int dirty;
    int shared_anon;
    int file_page;
    int anon;
    int swapped;
    int present;
} PageInfo;

typedef struct {
    unsigned long begin;
    unsigned long end;
} AddrPair;

AddrPair *addr_data;
PageInfo *pages_data;
uint64_t *u_data;
char *pid_str;

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

//function writes data in binary format to buffer
void to_bin(void *data, char *buffer, size_t size) {
    unsigned char *temp = (unsigned char *) data;
    for (int i = 0; i < size; i++) {
        *buffer = temp[i];
        buffer++;
    }
}

//function initializes an array of AddrPair structures  and fills it with pairs of block's start and end addresses
unsigned long parse_maps_blocks(AddrPair **addresses, FILE *maps_fp) {
    if (*addresses != NULL) {
        perror("Addresses pointer should be NULL before calling parse_blocks()\n");
        exit(EXIT_FAILURE);
    }
    unsigned long size = INIT_ARR_SIZE;
    *addresses = (AddrPair *) malloc(size * sizeof(AddrPair));
    int counter = 0;
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
    for (int i = 0; i < block_size; i++) {
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
unsigned long get_pages_info(PageInfo **pages, AddrPair *addr_data, long addr_data_size, int page_fd, int flags_fd) {
    if (*pages != NULL) {
        perror("Pages pointer should be NULL before calling get_pages()\n");
        exit(EXIT_FAILURE);
    }
    unsigned long size = INIT_ARR_SIZE;
    *pages = (PageInfo *) malloc(size * sizeof(PageInfo));
    unsigned long current_addr = 0;
    unsigned long pages_counter = 0;
    unsigned long block_size;
    unsigned long nread;
    unsigned long k = 0;
    for (unsigned int i = 0; i < addr_data_size; i++) {
        if (addr_data[i].begin > current_addr) {
            (*pages)[pages_counter].addr = current_addr;
            (*pages)[pages_counter].pfn = 0;
            (*pages)[pages_counter].file_page = 0;
            (*pages)[pages_counter].swapped = -1;
            (*pages)[pages_counter].present = -1;
            (*pages)[pages_counter].dirty = -1;
            (*pages)[pages_counter].anon = -1;
            pages_counter++;
            current_addr = addr_data[i].begin;
            k++;
        }
        block_size = (addr_data[i].end - addr_data[i].begin) / PAGE_SIZE;
        if (pages_counter + block_size >= size - 1) {
            size = (unsigned long) (size + block_size + 1);
            *pages = realloc(*pages, size * sizeof(PageInfo));
        }
        nread = get_page_info_block(page_fd, flags_fd, pages, block_size, addr_data[i].begin, pages_counter);
        pages_counter += nread;
        current_addr = addr_data[i].end;
    }
    printf("Amount of unused blocks: %ld\n", k);
    return pages_counter;
}

int create_data_file(PageInfo *data, unsigned long data_size, char *path_to_save) {
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
    unsigned int flags_data = 0;
    void *bin_data = NULL;
    while (i < data_size) {
        flags_data = 0;
        if (data[i].swapped != 0 || data[i].present != 0) {
            if (data[i].present != -1) { //unmapped pages have no flags -> flags_data = 0
                INITIALIZE_CUSTOM_DIRTY(flags_data, data[i].dirty);
                INITIALIZE_CUSTOM_ANON(flags_data, data[i].anon);
                INITIALIZE_CUSTOM_PRESENT(flags_data, data[i].present);

                uint64_t temp_data = data[i].present == 1 ? data[i].pfn : data[i].swap_offset;
                bin_data = &temp_data;
                to_bin(bin_data, &file_buffer[buffer_count], sizeof(uint64_t));
                buffer_count += sizeof(uint64_t);
                bin_data = &flags_data;
                to_bin(bin_data, &file_buffer[buffer_count], sizeof(unsigned int));
                buffer_count += sizeof(unsigned int);
            }
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
    return 0;
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
