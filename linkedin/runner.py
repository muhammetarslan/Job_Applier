from utils import *
from filereader import read_pros_cons_text_file

pros, cons, m_pros, m_cons = read_pros_cons_text_file('../proscons.txt')


def applier():
    login()
    res = search_sdet()
    for posting in res:
        time.sleep(1)
        applied = apply_if_fit(job_description(), pros, cons, m_pros, m_cons)
        if applied:
            save_applied()
        posting.click()
    while page_number < 2:
        time.sleep(2)
        res = change_page_get_new_list()
        for posting in res:
            time.sleep(1)
            applied = apply_if_fit(job_description(), cons, m_pros, m_cons)
            if applied:
                save_applied()
            print(job_description())
            posting.click()


applier()
