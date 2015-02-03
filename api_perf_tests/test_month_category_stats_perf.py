#!/usr/bin/env python
__author__ = 'srininara'
import sys
import gevent
import time
from gevent import monkey
monkey.patch_all()
monkey.patch_socket()
import urllib2


def fetch_url(url):
    """ Fetch a URL and return the total amount of time required.
    """
    t0 = time.time()
    try:
        resp = urllib2.urlopen(url)
        resp_code = resp.code
    except urllib2.HTTPError, e:
        resp_code = e.code

    t1 = time.time()
    print("\t@ %5.2fs got response [%d]" % (t1 - t0, resp_code))
    return t1 - t0


def time_fetch_urls(url, num_jobs):
    """ Fetch a URL `num_jobs` times in parallel and return the
        total amount of time required.
    """
    print("Sending %d requests for %s..." % (num_jobs, url))
    t0 = time.time()
    jobs = [gevent.spawn(fetch_url, url) for i in range(num_jobs)]
    gevent.joinall(jobs)
    t1 = time.time()
    print("\t= %5.2fs TOTAL" % (t1 - t0))
    return t1 - t0


if __name__ == '__main__':

    try:
        num_requests = int(sys.argv[1])
    except IndexError:
        num_requests = 100

    # t0 = time_fetch_urls("http://127.0.0.1:5000/grihasthi/apis/v1.0/monthStatsDaily/2015-1", num_requests)
    t1 = time_fetch_urls("http://127.0.0.1:8000/grihasthi/apis/v1.0/monthStatsCategory/2015-1", num_requests)
    # t1 = time_fetch_urls("http://www.google.co.in", num_requests)
    # t1 = time_fetch_urls("http://127.0.0.1:8000/grihasthi/apis/v1.0/dummy", num_requests)

    print("------------------------------------------")
    # print("SUM TOTAL = %.2fs" % (t0 + t1))