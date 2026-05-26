#!/usr/bin/env python
csvfile = './query_results.txt'
new_format_file = './new_format.csv'
with open(new_format_file, 'w') as new_fmt:
    with open(csvfile) as cfile:
        header_line = cfile.readline()
        new_fmt.write(header_line)
        cfile.readline()
        for row in cfile:
            id = row[0:3].strip()
            print(id)
            label = row[4:25].strip()
            print(label)
            date = row[26:37].strip()
            print(date)
            inparens = row[38:47].strip()
            parent_id = row[48:55].strip()
            id_dum = row[56:60].strip()
            colour = row[60:68].strip()
            level = row[67:72].strip()
            l1 = ';'.join([id, label, date, inparens, parent_id, colour, level])
            new_fmt.write(l1+"\n")
