
bind = "unix:/var/run/yang/yangre.sock"

workers = 2

max_requests = 1000
timeout = 20
keep_alive = 2

user = 'yang'
group = 'yang'

preload = True

accesslog = '/var/yang/logs/uwsgi/yangre-access.log'
errorlog = '/var/yang/logs/uwsgi/yangre-error.log'
loglevel = 'debug'
#change log format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'