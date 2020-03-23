#ifndef PAGE_TOOL_H
#define PAGE_TOOL_H

#include <stdio.h>
#include <inttypes.h>

#define FILE_PATH_SIZE 256
#define BUF_SIZE 1000
#define INIT_ARR_SIZE 1000
#define RESIZE_C 1.5
#define CHUNK_SIZE 9600 //single pagedata includes 64 + 32 = 96 bytes, buffer for 100 data records
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

uint64_t read_u64(int fd, unsigned long offset);
unsigned long parse_maps_blocks(AddrPair **addresses, FILE *maps_fp);
unsigned long get_page_info_block(int page_fd, int flags_fd, PageInfo **pagemap, unsigned long block_size, uintptr_t vaddr, unsigned long pagemap_pos);
unsigned long get_pages_info(PageInfo **pages, AddrPair *addr_data, unsigned long addr_data_size, int page_fd, int flags_fd);
void create_data_file(PageInfo *data, unsigned long data_size, char *path_to_save);

#endif //PAGE_TOOL_H
