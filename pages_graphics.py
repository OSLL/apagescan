from collections import Counter

from cairo import ImageSurface, Context, Format

from utilities import create_regions_map

RAM_SIZE = 2 ** 31  # 2 gb
SWAP_SIZE = 20 * (2 ** 20)  # 20 mb
PAGE_SIZE = 4096
block_size = 10  # pixel size
pages_in_block = 64

"""
Page size = 4096, i assumed 64 pages in block.
RAM size in our case = 2**31, so it gives
2**31 / (64 * 4096) = 2**31 / 2**18 = 2**13 blocks,
by splitting 2**13 into 2**7 and 2**6,
we get 128 x 64 blocks RAM visualization,
each block containing 64 pages    
same for SWAP, resulting in 80x1 blocks
"""


def draw_hblocks_line(context, start_point, length, width_in_blocks=1):
    """Draws horizontal line using blocks (size of <block_size> pixels)

    :param context: cairo context
    :param start_point: start coordinates on context to start drawing from
    :param length: length of line in pixels
    :param width_in_blocks: width of a line counted in <block_size>
    :return: None
    """
    start_x, start_y = start_point
    context.rectangle(start_x, start_y, length, block_size * width_in_blocks - 1)
    context.set_source_rgb(0, 0, 0)
    context.fill()


def draw_addr_area(context_data, area_len, regions_map, pid_color_map, start_point=(0, 0), start_pfn=0):
    """Draws processes' pages, combining them in blocks (size of <block_size> pixels) of different colors related to the process

    :param context_data: contains tuple (cairo context, context width, context height)
    :param area_len: length in bytes of memory part the is being displayed
    :param regions_map: tree of intervals (start_phys_index, end_phys_index, pid) that maps areas of pages in memory to processes
    :param pid_color_map: map of pids to colors for drawing
    :param start_point: start coordinates on context to start drawing from
    :param start_pfn: index of page in physical memory to start counting from
    :return: None
    """
    context, width, height = context_data

    x, y = start_point
    pfn = start_pfn

    pid_counter = Counter()
    pages_count = area_len // PAGE_SIZE

    while pfn < pages_count:
        intervals = regions_map[pfn:pfn + pages_in_block]

        for interval in intervals:
            pid_counter[interval.data] += 1

        # block has been processed, draw it
        if pfn % pages_in_block == 0:
            most_counted_pid = pid_counter.most_common(1)
            if most_counted_pid:
                pid = most_counted_pid[0][0]
                color = pid_color_map[pid]
                context.rectangle(x, y, block_size, block_size)
                context.set_source_rgb(color.redF(), color.greenF(), color.blueF())
                context.fill()

            if x + block_size >= width - 1:
                y += block_size

            x = (x + block_size) % width

            pid_counter.clear()

        pfn += pages_in_block


def plot_pids_pagemap(page_data, colors_list, iteration):
    """Creates an image of visual representation of device physical memory

    :param page_data: page data divided into present and swapped parts, containing info for each page of a group of processes
    :param colors_list: list of colors (QColor), so every process can be marked by unique color
    :param iteration: number of current iteration
    :return: None
    """
    ram_width, ram_height = 128, 64
    swap_width, swap_height = 80, 1

    pix_width, pix_height = max(ram_width, swap_width) * block_size, (ram_height + swap_height + 1) * block_size

    present_regions = create_regions_map(page_data[0])
    swapped_regions = create_regions_map(page_data[1])

    pid_color_map = dict(zip(page_data[0].keys(), colors_list))

    surface = ImageSurface(Format.RGB24, pix_width, pix_height)

    context = Context(surface)
    context.scale(1, 1)

    context.save()
    context.set_source_rgba(1., 1., 1., 1.)
    context.paint()
    context.restore()

    draw_addr_area((context, pix_width, pix_height),
                   RAM_SIZE,
                   present_regions,
                   pid_color_map)
    draw_hblocks_line(context, (0, ram_height * block_size), pix_width)
    draw_addr_area((context, pix_width, pix_height),
                   SWAP_SIZE,
                   swapped_regions,
                   pid_color_map,
                   (0, (ram_height + 1) * block_size))

    surface.write_to_png(f'resources/data/pictures/offsets/p{iteration}.png')
    surface.finish()