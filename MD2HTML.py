# -*- coding:utf-8 -*-

import markdown
import sys
import os
import re

# ********************************************************************
# * constants
# ********************************************************************
myCSS_file_name = 'myStyle.css'
encodings = ('ascii', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 
'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3','iso2022_jp_ext')


# ********************************************************************
# * main
# ********************************************************************
def main():
    # accept input file name
    if len(sys.argv) < 2:
        print 'Please input your markdown file (full path): '
        input_file_name = sys.stdin.readline().rstrip()
    else:
        input_file_name = sys.argv[1]
    
    # replace extention to '.html'
    output_file_name = re.sub(r'\.[^\.]+$', '.html', input_file_name)
    
    # pre-process for specific styles of Markdown
    file_name_pre_processed = pre_process(input_file_name)
    
    # convert Markdown file to HTML file
    convert_md2html(file_name_pre_processed, output_file_name, myCSS_file_name)
    
    # cleaning
    os.remove(file_name_pre_processed)

# ********************************************************************
# * pre-process for specific styles of markdown
# ********************************************************************
def pre_process(input_file_name):
    tag_open = '<pre><code>'
    tag_open_with_title_head = '<pre><span class="code-title">'
    tag_open_with_title_tail = '</span><code>'
    tag_close = '</code></pre>'
    temp_file = open('temp.md', 'w')
    open_flg = False
    
    input_file = open(input_file_name)
    
    for line in input_file.readlines():
        if line.startswith('```'):
            if open_flg:
                open_flg = False
                pre_tag = tag_close
            else:
                open_flg = True
                if line.endswith('`\n'):
                    pre_tag = tag_open
                else:
                    pre_tag = tag_open_with_title_head
                    line = re.sub('$', tag_open_with_title_tail, line) # convert the last character (before new-line code) to tag_open_with_title_tail
            line = line.replace('```', pre_tag)
        temp_file.write(line)
    temp_file.close()
    input_file.close()
    
    return temp_file.name

# ********************************************************************
# * convert Markdown file to HTML file
# ********************************************************************
def convert_md2html(input_file_name, output_file_name, style_sheet_name=None):
    fix_encoding = find_encoding(input_file_name)
    
    input_file = open(input_file_name)
    html = markdown.markdown(input_file.read().decode(fix_encoding))
    
    output_file = open(output_file_name, 'w')
    
    output_file.write('<html>')
    if style_sheet_name is not None:
        output_file.write('<style>')
        output_file.write(open(style_sheet_name).read())
        output_file.write('</style>')
    output_file.write('<body>')
    output_file.write(html.encode(fix_encoding))
    output_file.write('</body>')
    output_file.write('</html>')
    
    output_file.close()

# ********************************************************************
# * find encoding in defined encodings
# ********************************************************************
def find_encoding(input_file_name):
    input_file = open(input_file_name)
    for check_encoding in encodings:
        try:
            input_file.seek(0)
            content = input_file.read()
            content = content.decode(check_encoding)
            fix_encoding = check_encoding
        except UnicodeDecodeError:
            pass
    
    # if the encoding is not found in defined encodings, raise Exception
    if fix_encoding is None:
        print 'Unknown encoding... [%s]' %(input_file_name)
        raise UnicodeDecodeError
    
    return fix_encoding

if __name__ == '__main__':
    main()
