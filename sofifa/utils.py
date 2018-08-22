import requests
from bs4 import BeautifulSoup

class RedirectException(Exception):
    pass

cookie = {
    'playerCol': 'ae%2Coa%2Cpt%2Cvl%2Cwg%2Ctt%2Cwi%2Chi%2Cts%2Csho%2Cpi%2Cgu%2Cle%2Cpf%2Crc%2Ccr%2Cta%2Cfi%2Che%2Csh%2Cvo%2Cdr%2Ccu%2Cfr%2Clo%2Cbl%2Cto%2Cac%2Csp%2Cag%2Cre%2Cba%2Csa%2Csl%2Cwi%2Cwk%2Cjt%2Ctp%2Cso%2Cju%2Cst%2Csr%2Cln%2Cte%2Car%2Cin%2Cpo%2Cvi%2Cpe%2Ccm%2Ctd%2Cma%2Ctg%2Cgd%2Cgh%2Cgk%2Cgp%2Cgr%2Csk%2Caw%2Cdw%2Cir%2Cpac%2Cpas%2Cdri%2Cdef%2Cphy',
    'teamCol': 'oa%2Cat%2Cmd%2Cdf%2Cps%2Ctb%2Cwi%2Chi%2Cts%2Csho%2Cpi%2Cgu%2Cle%2Cpf%2Crc%2Ccr%2Cta%2Cfi%2Che%2Csh%2Cvo%2Cdr%2Ccu%2Cfr%2Clo%2Cbl%2Cto%2Cac%2Csp%2Cag%2Cre%2Cba%2Csa%2Csl%2Cwi%2Cwk%2Cjt%2Ctp%2Cso%2Cju%2Cst%2Csr%2Cln%2Cte%2Car%2Cin%2Cpo%2Cvi%2Cpe%2Ccm%2Ctd%2Cma%2Ctg%2Cgd%2Cgh%2Cgk%2Cgp%2Cgr%2Csk%2Caw%2Cdw%2Cir%2Cpac%2Cpas%2Cdri%2Cdef%2Cphy'
}

def get_page(url):
    page = requests.get(url, cookies=cookie, allow_redirects=False)
    if page.status_code == 200:
        return BeautifulSoup(page.text, 'html.parser')
    else:
        raise RedirectException("Sofifa redirected request!")

def build_url(base_url, query_string, offset):
    return f'{base_url}?{query_string}&offset={offset}'

def get_integeres_from_text(text):
    return ''.join(c for c in text if c.isdigit())
