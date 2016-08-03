import caida
import request_handler
import config
import time
import signal

date = "";

def sig_handler(sig, frame):
	if (date != ""):
		print notify_terminated(date);
	exit();

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sig_handler);
	handler = request_handler.RequestHandler("config.ini");
	proxy_file = config.get_config_section_dict("config.ini", "proxy")["proxy_file"];

	while(True):
		date = handler.get_task();
		print date;
		
		start_time = time.time();
		print handler.notify_started(date);

		caida.download_date(date, proxy_file=proxy_file, mt_num=10);

		end_time = time.time();
		time_used = end_time - start_time;
		print handler.notify_finished(date, time_used);
