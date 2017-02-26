# coding:utf-8
'''
Created on 2017��2��19��

@author: raytine
'''
import requests
from MyLogging import Log
from bs4 import BeautifulSoup
from Singleton import singleton
from random import choice
# from cPickle
my_log = Log('agent')

@singleton
class Agent():
    def __init__(self):
        '''
        .初始化代理
        self:
            success_rate:
                type:dict
                content:不同代理正确率计算
            agent_pool:
                type:dict
                content:代理池{ip:{port:--,safe:--}}
            fail_agent_pool:
                type:list
                content:失败的代理[ip]
        '''
        self.success_rate = {'KuaiDaiLi':1, 'Proxy360':1, 'XiCiDaiLi':1}
        self.agent_pool = {}
        self.fail_agent_pool = []
        
    def __del__(self):
        pass
    
    def addAgent(self, ip, port, safe, agent_type):
        '''
        .添加代理的函数
        para:
            ip:
                type:str
                content:代理ip
            port:
                type:str
                content:代理端口
            safe:
                type:str
                content:代理类型
            agent_type:
                type:str
                content:代理网站名称
        '''
        if ip in self.fail_agent_pool:
            return
        a_agent = dict(zip(['port', 'safe', 'type'], [port, safe, agent_type]))
        self.success_rate[agent_type] += 1
        self.agent_pool[ip] = a_agent
    
    def delAgent(self, ip):
        '''
        .删除失败代理函数
        ip:
            type:str
            content:失败代理的ip
        '''
        fail = self.agent_pool.pop(ip)
        self.success_rate[fail['type']] -= 1
        self.fail_agent_pool.append(ip)
        self.fail_agent_pool = self.fail_agent_pool[-100:]
    
    def getAgent(self):
        if len(self.agent_pool) < 100:
            self.getKuaiDaiLiAgent()
            self.getProxy360Agent()
            self.getXiCiDaiLiAgent()
        ran = choice(self.agent_pool.keys())
        return ran, self.agent_pool[ran]

    def getKuaiDaiLiAgent(self):
        header = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Host':'www.kuaidaili.com',
                    'Referer':'http://www.kuaidaili.com/',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                  }
        session = requests.Session()
        res = session.get('http://www.kuaidaili.com/', headers=header)
        if res.status_code!=200:
            return False
        soup = BeautifulSoup(res.text, "lxml")
        trs = soup.select('.table')[0].tbody.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            safe = tds[2].text.strip()
            self.addAgent(ip, port, safe, 'KuaiDaiLi')
    
    def getProxy360Agent(self):
        header = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Host':'www.proxy360.cn',
                    'Referer':'https://www.baidu.com/link?url=TseXMi0WAcePZcpWE0JpI51UGiRswpZnzcCz_eO02RbfaxUWtLh709DpM12UPZ8a&wd=&eqid=a17a010a000042240000000558aaf90a',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                  }
        session = requests.Session()
        res = session.get('http://www.proxy360.cn/default.aspx', headers=header)
        if res.status_code!=200:
            return False
        soup = BeautifulSoup(res.text, "lxml")
        items = soup.select('.proxylistitem')
        for item in items:
            span = item.find_all('span')
            ip = span[0].text.strip()
            port = span[1].text.strip()
            safe = span[2].text.strip()
            self.addAgent(ip, port, safe, 'Proxy360')
    
    def getXiCiDaiLiAgent(self):
        header = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Host':'www.xicidaili.com',
                    'If-None-Match':'W/"6c441f9f016f0ef1827efb31a2678fdf"',
                    'Referer':'https://www.baidu.com/link?url=T6FJB0JU0A3Fq3p30ElLbme4yKRr6e0PCaRGxfnGSHSmWUbdo5Y3K2H8qvbnPMfa&wd=&eqid=fc53a63100003b990000000558aafbd9',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                  }
        session = requests.Session()
        res = session.get('http://www.xicidaili.com/', headers=header)
        if res.status_code!=200:
            return False
        soup = BeautifulSoup(res.text, "lxml")
        items = soup.select('.odd')
        for item in items:
            span = item.find_all('td')
            ip = span[1].text.strip()
            port = span[2].text.strip()
            safe = span[4].text.strip()
            self.addAgent(ip, port, safe, 'XiCiDaiLi')
    

if __name__ == '__main__':
    agent = Agent()
#     agent.getKuaiDaiLiAgent()
#     agent.getProxy360Agent()
#     agent.getXiCiDaiLiAgent()
    print agent.getAgent()