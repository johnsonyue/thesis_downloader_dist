import caida
import urllib
import urllib2
import time
import random
import signal

#site = "http://173.26.102.12/downloader/";
site = "http://173.26.102.10:8888/";
get_task_url = site+"get_task.php";
notify_url = site+"notify.php";

node_id = "node10";
node_key = "123456";

date = "";

def get_task():
	params = { "id": node_id, "key": node_key }; 
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(get_task_url, post_data).read();
	if (res == "auth failed"):
		print "auth failed";
		exit();
	
	return res;

def notify_started(date):
	params = { "id": node_id, "key": node_key, "type": "started", "task": date };
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(notify_url, post_data).read();
	if (res == "auth failed"):
		print "auth failed";
		exit();
	
	return res;


def notify_finished(date, time_used):
	params = { "id": node_id, "key": node_key , "type": "finished", "task" : date, "time_used": time_used };
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(notify_url, post_data).read();
	if (res == "auth failed"):
		print "auth failed";
		exit();
	
	return res;


def notify_terminated(date):
	params = { "id": node_id, "key": node_key , "type": "terminated", "task": date };
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(notify_url, post_data).read();
	if (res == "auth failed"):
		print "auth failed";
		exit();
	
	return res;


def sig_handler(sig, frame):
	if (date != ""):
		print notify_terminated(date);
	exit();

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sig_handler);

	while(True):
		date = get_task();
		
		start_time = time.time();
		print notify_started(date);

		caida.download_date(date, proxy_file="proxy_list", mt_num=10);

		end_time = time.time();
		time_used = end_time - start_time;
		print notify_finished(date, time_used);
