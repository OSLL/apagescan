from collections import Counter

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush

from utilities import create_regions_map

RAM_SIZE = 2 ** 31  # 2 gb
SWAP_SIZE = 20 * (2 ** 20)  # 20 mb
PAGE_SIZE = 4096
block_size = 10  # pixel size
pages_in_block = 64


def draw_hblocks_line(pixmap, start_point, length, width=1):
    painter = QPainter(pixmap)
    painter.setBrush(Qt.black)
    start_x, start_y = start_point
    painter.drawRect(start_x, start_y, length, block_size * width - 1)
    painter.end()


def draw_addr_area(pixmap, area_len, start_pfn, start_coords, regions, pid_color_map):
    painter = QPainter(pixmap)

    x, y = start_coords
    pfn = start_pfn
    width, height = pixmap.width(), pixmap.height()

    pid_counter = Counter()
    pages_count = area_len // PAGE_SIZE

    while pfn < pages_count:
        intervals = regions[pfn:pfn + pages_in_block]

        for interval in intervals:
            pid_counter[interval.data] += 1

        # block has been processed, draw it
        if pfn % pages_in_block == 0:
            most_counted_pid = pid_counter.most_common(1)
            if most_counted_pid:
                pid = most_counted_pid[0][0]
                color = pid_color_map[pid]
                painter.fillRect(x, y, block_size, block_size, QBrush(color))

            if x + block_size >= width - 1:
                y += block_size

            x = (x + block_size) % width

            pid_counter.clear()

        pfn += pages_in_block

    painter.end()


def plot_pids_pagemap(page_data, colors_list, iteration):
    """
        Page size = 4096, i assumed 64 pages in block.
        RAM size in our case = 2**31, so it gives
        2**31 / (64 * 4096) = 2**31 / 2**18 = 2**13 blocks,
        by splitting 2**13 into 2**7 and 2**6,
        we get 128 x 64 blocks RAM visualization,
        each block containing 64 pages

        same for SWAP, resulting in 80x1 blocks
    """
    ram_width, ram_height = 128, 64
    swap_width, swap_height = 80, 1

    pix_width, pix_height = max(ram_width, swap_width) * block_size, (ram_height + swap_height + 1) * block_size

    present_regions = create_regions_map(page_data[0])
    swapped_regions = create_regions_map(page_data[1])

    pid_color_map = dict(zip(page_data[0].keys(), colors_list))

    pixmap = QPixmap(pix_width, pix_height)
    pixmap.fill(Qt.white)

    draw_addr_area(pixmap, RAM_SIZE, 0, (0, 0), present_regions, pid_color_map)
    draw_hblocks_line(pixmap, (0, ram_height * block_size), pix_width)
    draw_addr_area(pixmap, SWAP_SIZE, 0, (0, (ram_height + 1) * block_size), swapped_regions, pid_color_map)

    pixmap.save(f'resources/data/pictures/offsets/p{iteration}.png')