import sys
import os
import manager

state_file_name = "state";
log_file_name = "log";

def usage():
	print "python manage.py <type> <args...>";
	print "       type: get_task/notify";
	print "       get_task: none";
	print "       notify: time, node_id, task, (time_used)";

def get_all_pid():
	return [ i for i in os.listdir('/proc') if i.isdigit()];

def get_all_fd(file_path):
	all_fd = [];
	for pid in get_all_pid():
		fd_dir = '/proc/{pid}/fd'.format(pid = pid);
       		if os.access(fd_dir, os.R_OK) == False:
			continue;

		for fd in os.listdir(fd_dir):
			fd_path = os.path.join(fd_dir, fd);
			if os.path.exists(fd_path) and os.readlink(fd_path) == file_path:
				all_fd.append(fd_path);

        return all_fd;

def is_occupied(file_name):
	file_path = os.path.join(os.getcwd() ,file_name);
	fd_num = len(get_all_fd(file_path));
	
	return fd_num >= 1;

def main(argv):
	if (len(argv) <= 1):
		usage();
		exit();
	type = argv[1];
	if (type=="on_notify"):
		if (len(argv) < 5):
			usage();
			exit();
		notify_type = argv[1];
		time_used = "";
		if (len(argv) >=6):
			time_used = argv[5];
		args = {
			"time" : argv[2],
			"node_id" : argv[3],
			"task" : argv[4],
			"time_used" : time_used
		};
		manager.on_notify(log_file_name, state_file_name, notify_type, args);
	elif (type=="get_task"):
		print manager.get_task(state_file);

if __name__ == "__main__":
	main(sys.argv);
