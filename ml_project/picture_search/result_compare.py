# coding=utf8


def filter_old_item_impl(base_file, next_file, out_file, input_sep=','):
    pid_set = set([])
    with open(base_file) as input_base:
        for line in input_base:
            line_arr = line.split(input_sep)
            pid_set.add(line_arr[0])
    with open(next_file) as input_source:
        with open(out_file, 'w') as output_data:
            for line in input_source:
                pid = line.split(',')[0]
                if pid not in pid_set:
                    output_data.write('{0}'.format(line))


def filter_old_item(base_file, next_file, input_sep=','):
    out_put_file_name = next_file + '_filter'
    filter_old_item_impl(base_file, next_file, out_put_file_name, input_sep)


def filter_in_items(base_file, next_file, out_put_file_name, add_index_arr, input_sep=',', output_sep=','):
    item_info_map = {}
    with open(base_file) as input_base:
        for line in input_base:
            line_arr = line.split(input_sep)
            item_info_map[line_arr[0]] = line_arr

    with open(next_file) as input_source:
        with open(out_put_file_name, 'w') as output_data:
            for line in input_source:
                line_arr = line.split(output_sep)
                if line_arr[0] in item_info_map:
                    extra_info = output_sep.join([item_info_map[line_arr[0]][i] for i in add_index_arr])
                    out_line = line.strip() + output_sep + extra_info
                    output_data.write(out_line)


if __name__ == '__main__':
    filter_old_item('/Users/galois/Downloads/search_data/星空', 'xingkong.csv')