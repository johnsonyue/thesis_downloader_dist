import caida
import urllib
import urllib2
import time
import random
import signal

site = "http://173.26.102.12/downloader/";
get_task_url = site+"get_task.php";
notify_started_url = site+"notify_started.php";
notify_finished_url = site+"notify_finished.php";
notify_terminated_url = site+"notify_terminated.php";

node_id = "node-12";
node_key = "1q2w3e4r";

date = "";

def get_task():
	params = { "id": node_id, "key": key }; 
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(site+get_task_url, post_data).read();
	if (res == "auth failed"):
		print "auth failed";
		exit();
	
	return res;

def notify_started(date):
	params = { "id": node_id, "key": key , "date": date };
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(site+notify_started_url, post_data).read();


def notify_finished(date, st, et, ut):
	params = { "id": node_id, "key": key , "date": date, "st": st, "et": et, "ut": ut };
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(site+notify_finished_url, post_data).read();
	if (res == "auth failed"):
		print "auth failed";
		exit();


def notify_terminated(date):
	params = { "id": node_id, "key": key , "time": date };
	opener = urllib2.build_opener();
	post_data = urllib.urlencode(params).encode('utf-8');
	res = opener.open(site+notify_terminated_url, post_data).read();
	if (res == "auth failed"):
		print "auth failed";
		exit();


def sig_handler(sig, frame):
	if (date != ""):
		notify_terminated(date);
	print "termianted";
	sys.exit(0);

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sig_handler);
	while(True):
		date = get_task();
		
		start_time = time.time();
		start_strftime = time.strftime("%Y-%m-%d %H:%M:%S");
		
		notify_started(date);
		#caida.download_date(date, proxy_file="proxy_list", mt_num=10);

		end_time = time.time();
		end_strftime = time.strftime("%Y-%m-%d %H:%M:%S");
		time_used = end_time - start_time;
		
		notify_finished(date, start_strtime, end_strftime);
