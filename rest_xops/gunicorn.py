from multiprocessing import cpu_count

bind = "127.0.0.1:8000"
workers = cpu_count()
timeout = 60
graceful_timeout = 10
loglevel = "error"
errorlog = "/var/log/rest_xops/xops.log"
