import requests
from scrapy import Selector
from bs4 import BeautifulSoup


class QZSpider(object):
    def __init__(self, usr, pwd, url):
        self.usr = usr
        self.pwd = pwd
        self.url = url
        self.response_url = None
        self.session = requests.session()
        self._kcb = "/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL"
        self._cj = "/jsxsd/kscj/cjcx_list"
        self._kjs = "/jsxsd/kbxx/jsjy_query2"

    def login(self):
        r = self.session.post(url=self.url + '/jsxsd/xk/LoginToXk', data={
                'USERNAME': self.usr,
                'PASSWORD': self.pwd
        })
        if r.text.find('学生个人中心') == -1:
            return {
                'success': False
            }
        else:
            bs = BeautifulSoup(r.text, 'html.parser')
            name = bs.find_all('div', id='Top1_divLoginName')[0].contents[0].split('(')[0]
            return {
                'success': True,
                'name': name,
                'academy': '未获取'
            }

    def get_cj(self, xnxq):
        try:
            res = {
                'success': True,
                'result': []
            }
            data = {"kksj": xnxq, "kcxz": '', "kcmc": '', "xsfs": 'all', }
            html = self.session.post(url=self.url + self._cj, data=data).text
            bs = BeautifulSoup(html, 'html.parser')
            cj_table_tag = bs.find_all("table", id="dataList")[0]
            trs = cj_table_tag.contents
            while '\n' in trs:
                trs.remove('\n')
            for tr in trs[1:]:
                tds = tr.contents
                while '\n' in tds:
                    tds.remove('\n')
                course = {
                    'kcmc': tds[3].text,
                    'kclbmc': tds[7].text,
                    'xf': tds[5].text,
                    'ksxzmc': tds[9].text,
                    'kcxzmc': tds[10].text,
                    'zcj': tds[4].text
                }
                res['result'].append(course)
            return res
        except Exception as e:
            return {'success': False}

    def get_pm(self):
        try:
            data = {
                "kksj": '',
                "kcxz": '',
                "kcmc": '',
                "xsfs": 'all',
            }
            html = self.session.post(url=self.url + self._cj, data=data).text
            sel = Selector(text=html)
            s1 = sel.xpath("/html/body/div[3]/text()")[8].extract()
            s2 = sel.xpath("/html/body/div[3]/text()")[9].extract()
            dic = {
                'success': True,
                'desc': (s1 + s2).replace('\r', '').replace('\n', '').replace('\t', ''),
                'pm': [

                ]
            }
            bs = BeautifulSoup(html, 'html.parser')
            pm_table_tag = bs.find_all("table", id="dataList")[2]
            table_children = pm_table_tag.contents
            while '\n' in table_children:
                table_children.remove('\n')
            rows = table_children[1:]
            for row in rows:
                cols = row.contents
                while '\n' in cols:
                    cols.remove('\n')
                dic['pm'].append({
                    'xnxq': cols[1].string,
                    'xfj': cols[2].string,
                    'bjpm': cols[3].string,
                    'zypm': cols[4].string
                })

            return dic
        except Exception as e:
            return {'success': False}

    def get_kjs(self, xnxqh, jxlbh, zc, zc2, xq, xq2, jc, jc2, jsbh='', bjfh='=', rnrs='', jszt='5'):
        """
        xnxqh: 2020-2021-2
        jxlbh: 一教 001， 二教 003，学研 014，全部
        jsbh: 教室编号，留空
        bjfh: 比较符号  rnrs:容纳人数
        jszt: 教室状态，空教室：5
        zc:周次 从zc到zc2
        xq:星期 从xq到xq2
        jc: 节次从jc到jc2 两位，位数不足补0，如jc='03' jc2='04'
        """
        typewhere = 'jszq'
        try:
            data = {
                'typewhere': typewhere,
                'xnxqh': xnxqh,
                'jxlbh': jxlbh,
                'jsbh': jsbh,
                'bjfh': bjfh,
                'rnrs': rnrs,
                'jszt': jszt,
                'zc': zc,
                'zc2': zc2,
                'xq': xq,
                'xq2': xq2,
                'jc': jc,
                'jc2': jc2
            }
            html = self.session.post(url=self.url + self._kjs, data=data, timeout=100).text
            # print(html)
            bs = BeautifulSoup(html, 'html.parser')
            table_tag = bs.find_all("table", id="dataList")[0]

            table_children = table_tag.contents
            while '\n' in table_children:
                table_children.remove('\n')
            # 去除表头b表尾多余信息
            table_children = table_children[2:-2]
            l_kjs = []
            for row in table_children:
                td_tag = row.contents[1]
                td_tag_children = td_tag.contents
                js = td_tag_children[2].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                js = js.split('(')[0]
                l_kjs.append(js)
            dic = {
                'success': True,
                'kjs': l_kjs
            }
            return dic
        except Exception as e:
            return {'success': False}

    def get_summer_kcb(self, xnxqh='2020-2021-3', week=1):
        try:
            data = {
                'zc': week,
                'xnxq01id': xnxqh,
                'sfFD': 1
            }
            html = self.session.post(url=self.url + self._kcb, data=data, timeout=300).text
            bs = BeautifulSoup(html, 'html.parser')
            table_tag = bs.find_all("table", id="kbtable")[0]
            table_children = table_tag.contents
            while '\n' in table_children:
                table_children.remove('\n')
            table_children = table_children[1:-1]

            time = ['0102', '0304', '05', '0607', '0809', '1011', '12']

            kcb = []

            for t, tr in zip(time, table_children):
                tr_children = tr.contents
                while '\n' in tr_children:
                    tr_children.remove('\n')
                td_tags = tr_children[1:]
                day = ['1', '2', '3', '4', '5', '6', '7']
                for d, td in zip(day, td_tags):  # 遍历当前time周一到周日的开课情况
                    td_children = td.contents
                    while '\n' in td_children:
                        td_children.remove('\n')
                    l_content = td_children[3].contents  # 提取核心内容
                    while '\xa0' in l_content:
                        l_content.remove('\xa0')

                    if len(l_content) != 0:
                        teacher = None
                        classroom = None
                        zc = None

                        for c in l_content[1:]:
                            try:
                                if c.get('title') == '老师':
                                    teacher = c.contents[0]
                                if c.get('title') == '周次(节次)':
                                    zc = c.contents[0]
                                    zc = zc.split('(')[0]
                                if c.get('title') == '教室':
                                    classroom = c.contents[0]
                            except:
                                continue

                        kc = {
                            'jsxm': teacher,
                            'jsmc': classroom,
                            'kkzc': zc,
                            'kcsj': d + t,
                            'kcmc': l_content[0]

                        }
                        kcb.append(kc)
            return {'success': True, 'kcb': kcb}
        except Exception as e:
            return {'success': False}


if __name__ == '__main__':
    Q = QZSpider("171002412", "tao285714", "http://ymq-manage.natapp1.cc")

    print(Q.login())
    print(Q.get_pm())
