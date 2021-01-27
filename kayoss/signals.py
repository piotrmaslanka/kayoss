import collections


signals = collections.defaultdict(list)


def handle_signal(signame: str):
    for signal in signals[signame]:
        signal()


def register_signal(signame: str, callable):
    signals[signame].append(callable)
