# -*- coding: utf-8 -*-
# @Author  : Stone
# @Email   : Stone@spidereye.cn
import json
from mitmproxy import ctx
import mitmproxy
from flask import Flask, request
from peopleDailyCommentSpider import getCommentData

app = Flask(__name__)
app.debug = True


# https://wap.peopleapp.com/article/5484122/5403224
@app.route('/', methods=['get'])
def getComments():
    rticleID = request.args.get('id')
    try:
        with open(rticleID + '-comments.json', 'r', encoding='utf-8') as F:
            comments = F.read()
            print(comments)
        return json.loads(comments)
    except Exception as E:
        print(E)
        return 'error'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
