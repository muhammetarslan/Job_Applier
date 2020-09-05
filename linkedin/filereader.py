#######################################################################

"""
This file inputs a text file path,
The first line of the file starts with pros, ...\n
than cons \n
mendatory pros \n
mendatory cons \n
Structered such as:
pros, java, c#
cons, aws, python
m_pros, javascript
m_cons, clearance
"""


def read_pros_cons_text_file(text_path):
    try:
        line_list = open(text_path, 'r').readlines()
    except FileNotFoundError:
        print(
            'File not found. Please create a proscons.txt located in the described path.\n'
            'File format should be like: '
            'The first line of the file starts with pros, ...\n'
            'than cons \n'
            'mendatory pros \n'
            'mendatory cons \n'
        )
        raise FileNotFoundError

    pros = None
    cons = None
    m_pros = None
    m_cons = None

    if line_list[0].find(',') > 0:
        pros = line_list[0].replace('pros, ', '').replace('\n', '')

    if line_list[1].find(',') > 0:
        cons = line_list[1].replace('cons, ', '').replace('\n', '')

    if line_list[2].find(',') > 0:
        m_pros = line_list[2].replace('m_pros, ', '').replace('\n', '')

    if line_list[3].find(',') > 0:
        m_cons = line_list[3].replace('m_cons, ', '').replace('\n', '')

    return [pros, cons, m_pros, m_cons]
