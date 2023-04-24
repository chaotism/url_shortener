import random


def get_proxy() -> str:
    proxy = random.choice(proxies)
    return proxy


proxies = ('',)
