import HTMLParser
import urllib
import urllib2
import re
import os
import cookielib

#html parsers.
class iPlaneParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self);
		self.img_cnt=0;
		self.alt="";
		self.file=[];
		self.dir=[];

	def get_attr_value(self, target, attrs):
		for e in attrs:
			key = e[0];
			value = e[1];
			if (key == target):
				return value;

	def handle_starttag(self, tag, attrs):
		if (tag == "img"):
			if (self.img_cnt >=2):
				alt_value = self.get_attr_value("alt", attrs);
				self.alt=alt_value;
			self.img_cnt = self.img_cnt + 1;
		
		if (tag == "a" and self.alt == "[DIR]"):
			href_value = self.get_attr_value("href", attrs);
			self.dir.append(href_value);
		elif (tag == "a" and self.alt != ""):
			href_value = self.get_attr_value("href", attrs);
			self.file.append(href_value);

def get_iplane_tree(dir, username, password):
	url = "https://data-store.ripe.net/datasets/iplane-traceroutes/";
		
	print "logging in...";
	params = { "username": username, "password": password }; 
	cj = cookielib.CookieJar();
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));

	login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo";
	post_data = urllib.urlencode(params).encode('utf-8');

	opener.open(login_url, post_data);
	print "done.";

	f = opener.open(url);
	text = f.read();

	parser = iPlaneParser();
	parser.feed(text);

	file = open("iplane",'wb');
	for e in parser.dir:
		get_year_dir(url+e, dir, opener, file);
	
	file.close();

def get_year_dir(url, dir, opener, file):
	f = opener.open(url);
	text = f.read();
	
	parser = iPlaneParser();
	parser.feed(text);

	for e in parser.file:
		list = e.split('_');
		time = list[1]+list[2]+list[3].split('.')[0];
		file.write(time+":"+url+e+"\n");

def read_auth(auth_file, account):
	ret = [];

	is_provided = False;
	for line in open(auth_file, 'r'):
		if (line=="\n"):
			continue;
		if (is_provided and len(re.findall("#",line)) ==0):
			ret.append(line.strip('\n'));
		elif(is_provided):
			break;

		if (len(re.findall("#"+account,line)) != 0):
			is_provided = True;
	return ret;

#must be of the same length.
def time_cmp(t1, t2):
	for i in range(len(t1)):
		if (t1[i] != t2[i]):
			break;
	if (i < len(t1)):
		return int(t1[i]) - int(t2[i]);
	return 0;
def get_latest_time_fromsite(username, password):
	url = "https://data-store.ripe.net/datasets/iplane-traceroutes/";
		
	print "logging in...";
	params = { "username": username, "password": password }; 
	cj = cookielib.CookieJar();
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));

	login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo";
	post_data = urllib.urlencode(params).encode('utf-8');

	opener.open(login_url, post_data);
	print "done.";

	f = opener.open(url);
	text = f.read();

	parser = iPlaneParser();
	parser.feed(text);
	
	e = parser.dir[-1].strip('/');
	res = parse_latest_year(url+e, opener);
	
	return res;


def parse_latest_year(url, opener):
	f = opener.open(url);
	text = f.read();
	
	parser = iPlaneParser();
	parser.feed(text);
	
	res = parser.file[-1];
	list = res.split('.')[0].split['_'];
	res = list[1]+list[2]+list[3];
	
	return res;
	
def construct_url_fromtime(target_time):
	url = "https://data-store.ripe.net/datasets/iplane-traceroutes/";
	target_year = target_time[:4];
	target_month = target_time[4:6];
	target_day = target_time[6:8];
	
	res = url+target_year+"/traces_"+target_year+"_"+target_month+"_"_target_day+".tar.gz";

	return res;

def 

#downloading with multi-thread support.
def download_caida_restricted_worker_mt_wrapper(url, dir, file, username, password, res_list, started_list, ind, proxy=""):
	started_list[ind] = True;
	res = download_worker.download_caida_restricted_worker(url, dir, file, username, password, proxy);
	res_list[ind] = res;
	started_list[ind] = False;
	

class DownloadThread(threading.Thread):
	def __init__(self, target, args):
		threading.Thread.__init__(self, target=target, args=args);
		self.start_time = time.time();
	
	def get_time_alive(self):
		end_time = time.time();
		return end_time - self.start_time;

def get_alive_thread_cnt(th_pool):
	cnt_alive = 0;
	for i in range(len(th_pool)):
		t = th_pool[i];
		#if (t.is_alive() and t.get_time_alive() >= 1):
		if (t.is_alive() ):
			cnt_alive = cnt_alive + 1;
	for th in th_pool:
		if (not th.is_alive()):
			th_pool.remove(th);
	
	return cnt_alive;

def download_date(date, root_dir="/data/data/caida/ipv4/", proxy_file="", mt_num=0 ):
	auth = read_auth("auth", "caida");
	is_succeeded = False;
	round_cnt = 1;
	while(not is_succeeded):
		try:
			url_list = get_time_list_fromsite(date, auth[0], auth[1]);
			is_succeeded = True;
		except:
			is_succeed = False;
			round_cnt = round_cnt + 1;
			time.sleep(10*round_cnt);

	dir = root_dir+date+"/";
	if (not os.path.exists(dir)):
		os.makedirs(dir);
	
	if (mt_num == 0):
		for url in url_list:
			team = url.split('/')[5];
