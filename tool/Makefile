CFLAGS := -Ofast -static -march=armv7-a
CC := arm-linux-gnueabi-gcc

all: get_pid_list pagemap read_cgroup transfer clean

get_pid_list: get_pid_list.c
	$(CC) $(CFLAGS) $< -o $@

pagemap: page_tool.c
	$(CC) $(CFLAGS) $< -o $@

read_cgroup: read_cgroup.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f get_pid_list pagemap read_cgroup

transfer: get_pid_list pagemap read_cgroup
	adb push $^ /data/local/testing/
