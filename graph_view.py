import matplotlib.patches as mpatches
import numpy as np
from matplotlib.figure import Figure


def barplot_pids_pagemap(page_data, highlighted_pids, iteration=''):
    """Displays 2 bar plot for each pid marked as highlighted and saves them to .png
    * 1 bar is [swapped % |     clean %     |    dirty %  ]
    * 2 bar is [swapped % | not anonymous % | anonymous % ]

    :param page_data: ordered dict with pid as key, and data frame, containing info about each page as value
    :param highlighted_pids: list of pids to be shown
    :param iteration: number of iteration of data collecting
    :return: None
    """
    # TODO Remove hardcoded values, use values depending on widget size
    width = 13
    height = 2
    fig = Figure(figsize=(width, height), dpi=100, facecolor='white')  # Figure constructor
    ax = fig.add_subplot()

    flags_colors = {'Swapped': 'yellow',
                    'Clean': 'lime',
                    'Dirty': 'blue',
                    'Not Anon': 'orange',
                    'Anon': 'red'
                    }

    for i, pid in enumerate(highlighted_pids):
        pid_pages_data = page_data.get(pid)
        total_pages = len(pid_pages_data)

        present_flag_count = get_flags_count(pid_pages_data, column=1)
        dirty_flag_count = get_flags_count(pid_pages_data, column=2)
        anon_flag_count = get_flags_count(pid_pages_data, column=3)

        is_dirty_bar = get_percentage_values(total_pages, present_flag_count, dirty_flag_count)
        is_anon_bar = get_percentage_values(total_pages, present_flag_count, anon_flag_count)

        plot_bar(ax, is_dirty_bar, y_offset=-i * 2,
                 colors=[flags_colors.get('Swapped'), flags_colors.get('Clean'), flags_colors.get('Dirty')])
        plot_bar(ax, is_anon_bar, y_offset=-i * 2 - 1,
                 colors=[flags_colors.get('Swapped'), flags_colors.get('Not Anon'), flags_colors.get('Anon')])

    # Set ticks and legend
    ax.set_ylabel('Pid number')
    ax.set_yticks([-x * 2 - 0.5 for x in range(len(highlighted_pids))])
    ax.set_yticklabels(highlighted_pids)
    ax.set_xlabel('Total pages, %')
    ax.set_xlim([0, 100])
    ax.legend(handles=[mpatches.Patch(color=flags_colors.get(flag), label=flag) for flag in flags_colors],
              bbox_to_anchor=(1, 1), loc='upper left', ncol=1, fontsize='small')
    # Save data to png
    ax.figure.savefig('resources/data/pictures/barplot/b' + iteration + '.png')


def get_flags_count(data, column):
    """From data-dataFrame forms the dict for specific flag. Each flag data is in the certain column

    :param data: dataFrame containing info about each page of process
    :param column: number of column in data-dataFrame.
    :return: dict like {0: <Number of 0-values in that column>, 1: <Number of 1-values in that column>}
    :rtype: Dict
    """
    unique, counts = np.unique(data[column], return_counts=True)
    return dict(zip(unique, counts))


def get_percentage_values(total_pages, present_flag, any_flag):
    """Calculate width of the bar plot in percentage ratio format

    :param total_pages: the total number of pages for process
    :param present_flag: dict formed by get_flags_count(data, column) function. {0: <number of swapped pages>, 1: <number of present pages>}
    :param any_flag: dict formed by get_flags_count(data, column) function. (ex. {0: <number of clean pages>, 1: <number of dirty pages>})
    :return: list of the widths for the bar plot (ex. [10, 50, 40]: 10% + 50% + 40% = 100%)
    :rtype: List
    """
    flags_count_data = [present_flag.get(0, 0),  # swapped
                        present_flag.get(1, 0) - any_flag.get(1, 0),  # present - any
                        any_flag.get(1, 0)]
    return [100 * flag_pages_count / total_pages for flag_pages_count in flags_count_data]


def plot_bar(ax, bar_data, y_offset, colors):
    """Displays a horizontal bar plot

    :param ax: axes instance in the coordinate system
    :param bar_data: the widths of the bars, formed by def get_percentage_values(total_pages, present_flag, any_flag)
    :param y_offset: the heights of the bars in y axes in the coordinate system. 0 offset - the highest bar.
    :param colors: list of colors for bar data
    :return: None
    """
    for i, bar_value in enumerate(bar_data):
        ax.barh(y=y_offset, width=bar_value, left=sum(bar_data[:i]), color=colors[i])
