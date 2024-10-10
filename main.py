import threading

from mitmproxy import http
from mitmproxy import ctx
import logging
import random
import subprocess
import time

# 禁用默认日志
logging.getLogger("mitmproxy").setLevel(logging.CRITICAL)
ctx.log.info("监听中...")

status = 0
answers = []


def request(flow: http.HTTPFlow) -> None:
    # 处理请求
    # ctx.log.info(f"Request: {flow.request.method} {flow.request.url}")
    pass


def response(flow: http.HTTPFlow) -> None:
    global status
    global answers
    # 处理响应
    # ctx.log.info(f"Response: {flow.response.status_code} {flow.request.url}")
    if "/leo-game-pk/android/math/pk/match" in flow.request.url:
        ctx.log.info("你这局的对手是: " + flow.response.json()['otherUser']['userName'])
        answers = []
        questions = flow.response.json()['examVO']['questions']
        for question in questions:
            answers.append(question['answer'])
        ctx.log.info("成功获取到题目答案：" + ' '.join(answers))
        status = 1
        thread = threading.Thread(target=answer_write, args=(answers,))
        # 启动线程
        thread.start()


def answer_write(arg):
    global status
    status = 0
    time.sleep(12.4)  # 没想到更好的开局检测方案，不过每局延时差不多，这个延迟刚刚好
    cwd = r'F:\Program Files\Netease\MuMu Player 12\shell'  # adb 所在目录
    swipe = r'.\adb.exe shell input swipe %d %d %d %d 1 '  # 模拟滑动
    jitter = round(random.random(), 2)
    for i in arg:
        ctx.log.info("正在作答：" + i)
        if i == '>':
            subprocess.Popen(swipe % (600 + jitter, 1355 + jitter, 680 - jitter, 1432 - jitter)
                             + '&' + swipe % (680 + jitter, 1432 + jitter, 603 - jitter, 1506 - jitter), shell=True,
                             cwd=cwd)
        elif i == '<':
            subprocess.Popen(swipe % (660 + jitter, 1360 + jitter, 600 - jitter, 1424 - jitter)
                             + '&' + swipe % (600 + jitter, 1424 + jitter, 675 - jitter, 1495 - jitter), shell=True,
                             cwd=cwd)
        elif i == '=':
            subprocess.Popen(swipe % (600 + jitter, 1380 + jitter, 640 - jitter, 1379 - jitter)
                             + '&' + swipe % (600 + jitter, 1424 + jitter, 641 - jitter, 1425 - jitter), shell=True,
                             cwd=cwd)
        else:
            ctx.log.info("尚不支持此答案：" + i)
        time.sleep(0.35)   # 写太快会识别出错，目前这个还算稳定，大部分时间都能正常跑


