import caida
import urllib
import urllib2
import time
import random
import signal

#site = "http://173.26.102.12/downloader/";
site = "http://172.17.0.9/web/";
get_task_url = site+"get_task.php";
notify_url = site+"notify.php";

node_id = "node12";
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
		notify_terminated(date);
	print "termianted";
	exit(0);

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sig_handler);
	date = get_task();
	print notify_started(date);

	'''
	while(True):
		date = get_task();
		
		start_time = time.time();
		notify_started(date);

		#caida.download_date(date, proxy_file="proxy_list", mt_num=10);
		time.sleep(random.randint(1,5));

		end_time = time.time();
		time_used = end_time - start_time;
		notify_finished(date, time_used);

	'''
