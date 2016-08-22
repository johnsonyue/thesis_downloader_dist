import urllib
import urllib2
import os
import cookielib
import copy

#caida restricted.
def download_caida_restricted_worker(url, dir, file, username, password, proxy=""):
	passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm();
	passwd_mgr.add_password("topo-data", url, username, password);

	opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwd_mgr));

	if(proxy != ""):
		opener.add_handler(urllib2.ProxyHandler({"http":proxy}));

	if not os.path.exists(dir):
		os.makedirs(dir);

	res = True;
	ex = None;
	try:
		if not os.path.exists(dir+file):
			f = opener.open(url, timeout=10);
			fp = open(dir+file, 'wb');
			fp.write(f.read());
			fp.close();
			f.close();
	except Exception, e:
		ex = e;
		res = False;
		if os.path.exists(dir+file):
			os.remove(dir+file);
	
	if res:
		print url.split('/')[-1] + " " + proxy + " " + str(res) + " " + (str(ex) if ex!=None else "succeeded");
	
	return res;

def download_iplane_restricted_worker(url, dir, file, username, password):
	print "logging in...";
	login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo";
	params = { "username": username, "password": password }; 
	cj = cookielib.CookieJar();
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));

	post_data = urllib.urlencode(params).encode('utf-8');

	f = opener.open(login_url, post_data);
	print "done.";
	
	print f.read();
	
	'''	
	if not os.path.exists(dir):
		os.makedirs(dir);

	CHUNK = 16*1024;
	if not os.path.exists(dir+file):
		f = opener.open(url);
		fp = open(dir+file, 'wb');
		while True:
			chunk = f.read(CHUNK);
			if not chunk:
				break;
			fp.write(chunk);
		fp.close();
	'''

def get_iplane_file_size(url, opener):
	request = urllib2.Request(url);
	request.get_method = lambda : "HEAD";
	f = opener.open(request);
	
	print f.info();

def get_iplane_opener(username, password):
	print "logging in...";
	login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo";
	params = { "username": username, "password": password }; 
	cj = cookielib.CookieJar();
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
	post_data = urllib.urlencode(params).encode('utf-8');

	opener.open(login_url, post_data);
	print "done.";
	
	return opener;

def download_segemented_iplane_restricted_worker(url, opener, start, end):
	return "";
	
def download_irr_delegate(url_list, dir, file):
	if not os.path.exists(root+dir+file):
		urllib.urlretrieve(url, root+dir+file);

#auth = ["johnsonyuehit@163.com", "yuzhuoxun123"];
auth = ["15b903031@hit.edu.cn", "yuzhuoxun123"];
#url = "https://topo-data.caida.org/team-probing/list-7.allpref24/team-1/daily/2007/cycle-20070913/daily.l7.t1.c000027.20070916.amw-us.warts.gz"
#url = "https://data-store.ripe.net/datasets/iplane-traceroutes/2016/traces_2016_08_11.tar.gz";
url = "https://topo-data.caida.org/README.ark.txt"
#opener = get_iplane_opener(auth[0], auth[1]);
#opener.open(url);
#download_iplane_restricted_worker(url, "temp/", "temp", "15b903031@hit.edu.cn", "yuzhuoxun123");
#download_iplane_restricted_worker(url, "temp/", "temp", "johnsonyuehit@163.com", "johnsonyue123");

passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm();
passwd_mgr.add_password("topo-data", url, auth[0], auth[1]);
opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwd_mgr));

request=urllib2.Request(url);
request.add_header("Range", "bytes=65536-65546");
f = opener.open(request);
print f.info();
fp = open("temp", 'wb');
fp.write(f.read());
fp.close();
f.close();

#get_iplane_file_size(url, opener);
