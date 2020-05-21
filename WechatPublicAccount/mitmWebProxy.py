# -*- coding: utf-8 -*-
# @Author  : Stone
# @Email   : Stone@spidereye.cn
import json

from mitmproxy import ctx
import mitmproxy


# 所有的请求都会经过request
def request(flow):
    info = ctx.log.info
    d = {}
    if flow.request.host == 'mp.weixin.qq.com':  # 过滤请求，如果host是xxx则写入请求相关信息
        d['url'] = flow.request.url
        d['host'] = flow.request.host
        d['headers'] = flow.request.headers
        d['method'] = flow.request.method
        # if flow.request.method == 'POST':
        if 'appmsg_comment?action=getcomment&' in flow.request.url:
            print(flow.request.url)
            print(flow.request.cookies)
            print(flow.request.headers)
            d['body'] = flow.request.get_text()
            fp = open("aaaa.txt", 'a+', encoding='utf-8')
            fp.write(str(d) + '\n')


def response(flow: mitmproxy.http.HTTPFlow):
    # 忽略非 360 搜索地址
    if flow.request.host != "'mp.weixin.qq.com':":
        if 'appmsg_comment?action=getcomment&' in flow.request.url:
            commentsDict= flow.response.text
            with open('comments.json', 'w', encoding='utf-8') as F:
                F.write(str(commentsDict))
