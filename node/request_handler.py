import ConfigParser
import urllib
import urllib2

class RequestHandler():
	def __init__(self, config_file):
		parser = ConfigParser.ConfigParser();
		parser.read(config_file);
		self.config = {};
		map( lambda x:self.config.setdefault(x[0], x[1]), parser.items("handler"));

		site = self.config["site"];
		get_task_page = self.config["get_task"];
		self.get_task_url = site + get_task_page;

		notify_page = self.config["notify"];
		self.notify_url = site + notify_page;

		self.node_id = self.config["node_id"];
		self.node_key = self.config["node_key"];

	def get_task(self):
		params = { "id": self.node_id, "key": self.node_key }; 
		opener = urllib2.build_opener();
		post_data = urllib.urlencode(params).encode('utf-8');
		res = opener.open(self.get_task_url, post_data).read();
		if (res == "auth failed"):
			print "auth failed";
			exit();
	
		return res;
	
	def notify_started(self, date):
		params = { "id": self.node_id, "key": self.node_key, "type": "started", "task": date };
		opener = urllib2.build_opener();
		post_data = urllib.urlencode(params).encode('utf-8');
		res = opener.open(self.notify_url, post_data).read();
		if (res == "auth failed"):
			print "auth failed";
			exit();
						
		return res;
	
	def notify_finished(self, date, time_used):
		params = { "id": self.node_id, "key": self.node_key , "type": "finished", "task" : date, "time_used": time_used };
		opener = urllib2.build_opener();
		post_data = urllib.urlencode(params).encode('utf-8');
		res = opener.open(self.notify_url, post_data).read();
		if (res == "auth failed"):
			print "auth failed";
			exit();
		
		return res;

	def notify_terminated(self, date):
		params = { "id": self.node_id, "key": self.node_key , "type": "terminated", "task": date };
		opener = urllib2.build_opener();
		post_data = urllib.urlencode(params).encode('utf-8');
		res = opener.open(self, notify_url, post_data).read();
		if (res == "auth failed"):
			print "auth failed";
			exit();
		
		return res;
