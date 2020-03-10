import cairo

# TODO: width, offsets and length should be calculated from device specifications


#  page_data - dict like {pid1: pid1_page_data, pid2: pid1_page_data}
def plot_pids_pagemap(page_data, colors, index):
    """Creates plot displaying page map and saves the image to '.png'

    :param page_data: dictionary contains data like {pid1: pid1_page_data, pid2: pid1_page_data}
    :param colors: color list
    :param index: number of iteration of data collecting
    """
    width = 2200
    length = 1251  # enough to 2GB of ram and 20mb of swap
    swap_offset = 1202  # offset to draw swap pages, it is 1202 and not 1200 because black line height is 2
    present_area_length = 1200

    surface = cairo.ImageSurface(cairo.Format.RGB24, width, length)
    context = cairo.Context(surface)
    context.scale(1, 1)

    # painting background to white
    context.save()
    context.set_source_rgba(1., 1., 1., 1.)
    context.paint()
    context.restore()

    # drawing horizontal line do divide swap and present
    context.set_source_rgba(0., 0., 0., 1.)  # black
    context.move_to(0, present_area_length)
    context.line_to(width, present_area_length)
    context.stroke()

    # Create dictionary pid - color
    colored_pid = dict(zip(page_data.keys(), colors))

    for pid, data in page_data.items():
        color = colored_pid.get(pid)

        # Remove zero addresses if exist, and sort addresses value
        clear_data = [[d[0], d[1]] for d in data.values if d[0] != 0]
        clear_data.sort()

        # lines
        current = [0, 0] # list to handle current present and swap pages
        streak = [1, 1] # list to handle amount of pages close to each other

        for page in clear_data:
            pfn = page[0]
            is_present = page[1]

            x = int(pfn % width)
            if is_present:
                y = int(pfn // length) * 2
            else:
                y = int(pfn // length) * 2 + swap_offset

            if current[is_present] - pfn == -1:  # first page goes right after another
                streak[is_present] += 1

            if x == width - 1:  # end of current line
                context.set_source_rgba(color.redF(), color.greenF(), color.blueF(), color.alphaF())
                context.move_to(x, y)
                context.line_to(width, y)
                streak[is_present] = 1
                current[is_present] = pfn
                continue

            if current[is_present] - pfn != -1:  # pages are far from each other
                context.set_source_rgba(color.redF(), color.greenF(), color.blueF(), color.alphaF())
                context.move_to(x, y)
                context.line_to(x + streak[is_present], y)
                streak[is_present] = 1
                current[is_present] = pfn

            context.stroke()
    surface.write_to_png(f'resources/data/pictures/offsets/p{index}.png')