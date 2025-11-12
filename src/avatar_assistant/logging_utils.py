import logging, sys
def get_logger(name="aa"):
    lg = logging.getLogger(name)
    if lg.handlers: return lg
    lg.setLevel(logging.INFO)
    h = logging.StreamHandler(sys.stderr)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    h.setFormatter(fmt); lg.addHandler(h)
    return lg
