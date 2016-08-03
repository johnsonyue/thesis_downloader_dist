import sys
import manager
import ConfigParser

def usage():
	print "python manage.py <type> <args...>";
	print "       type: get_task/notify/auth";
	print "       get_task";
	print "       on_notify notify_type, node_id, task, (time_used)";
	print "       auth ndoe_id, node_key";

def main(argv):
	if (len(argv) <= 1):
		usage();
		exit();
	type = argv[1];
	
	parser = ConfigParser.ConfigParser();
	parser.read("config.ini");
	config = {};
	map( lambda x:config.setdefault(x[0], x[1]), parser.items("files") );

	state_file_name = config["state_file_name"];
	log_file_name = config["log_file_name"];
	secret_file = config["secret_file"];
	
	if (type=="on_notify"):
		if (len(argv) < 5):
			usage();
			exit();
		notify_type = argv[2];
		time_used = "";
		if (len(argv) >=6):
			time_used = argv[5];
		args = {
			"node_id" : argv[3],
			"task" : argv[4],
			"time_used" : time_used
		};
		print manager.on_notify(log_file_name, state_file_name, notify_type, args);
	elif (type=="get_task"):
		print manager.get_task(state_file_name);
	elif (type=="auth"):
		node_id = argv[2];
		node_key = argv[3];
		print manager.auth_node(secret_file, node_id, node_key);
if __name__ == "__main__":
	main(sys.argv);
