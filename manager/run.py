import sys
import manager

state_file_name = "state";
log_file_name = "log";
secret_file = "nodes";

def usage():
	print "python manage.py <type> <args...>";
	print "       type: get_task/notify/auth";
	print "       get_task: none";
	print "       notify: time, node_id, task, (time_used)";
	print "       auth: ndoe_id, node_key";

def main(argv):
	if (len(argv) <= 1):
		usage();
		exit();
	type = argv[1];
	if (type=="on_notify"):
		if (len(argv) < 5):
			usage();
			exit();
		notify_type = argv[2];
		time_used = "";
		if (len(argv) >=7):
			time_used = argv[6];
		args = {
			"time" : argv[3],
			"node_id" : argv[4],
			"task" : argv[5],
			"time_used" : time_used
		};
		manager.on_notify(log_file_name, state_file_name, notify_type, args);
	elif (type=="get_task"):
		print manager.get_task(state_file);
	elif (type=="auth"):
		node_id = argv[2];
		node_key = argv[3];
		print manager.auth_node(secret_file, node_id, node_key);

if __name__ == "__main__":
	main(sys.argv);
