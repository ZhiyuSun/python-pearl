import time


def crawl_page(url):
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    time.sleep(sleep_time)
    print('OK {}'.format(url))


def main(urls):
    for url in urls:
        crawl_page(url)


begin_time = time.time()
main(['url_1', 'url_2', 'url_3', 'url_4'])
end_time = time.time()
run_time = end_time - begin_time
print("程序耗时{}s".format(run_time))