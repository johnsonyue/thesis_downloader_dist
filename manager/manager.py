import os

def is_heap_year(year):
	if (not year % 400 or not year % 4):
		return True;
	return False;

def days_in_month(year, month):
	m2d = [0,31,28,31,30,31,30,31,31,30,31,30,31];

	return m2d[month]+(1 if month == 2 and is_heap_year(year) else 0);

def next_day(date):
	y=int(date[:4]);
	m=int(date[4:6]);
	d=int(date[6:8]);
	
	num = days_in_month(y,m);
	if (d+1 > num):
		m = m + 1;
		d = 1;
		if (m > 12):
			y = y + 1;
			m = 1;
	else:
		d = d + 1;
	
	str = "%d%02d%02d" % (y, m, d);
	return str;

def update_state_file(file_name, end_time, start_time="", is_init = False):
	if (is_init):
		if (not os.path.exists(file_name)):
			open(file_name,'wb').close();
		if (start_time == ""):
			print "must provide start_time";
			exit();
	
		st = start_time;
		fp = open(file_name, 'wb');
	
	else:
		if (not os.path.exists(file_name)):
			print ("file does not exist");
			exit();
		fp = open(file_name,'r');
		st = fp.readlines()[-1].split(' ')[0];
		st = next_day(st);
		fp.close();
		fp = open(file_name,'a');
	
	y = int(st[:4]);
	m = int(st[4:6]);
	d = int(st[6:8]);

	ey = int(end_time[:4]);
	em = int(end_time[4:6]);
	ed = int(end_time[6:8]);
	
	while ( y < ey ):
		while ( m <= 12 ):
			num = days_in_month(y, m);
			while( d <= num ):
				str = "%d%02d%02d" % (y, m, d);
				fp.write(str+" unassigned"+'\n');
				d = d + 1;
			d = 1;
			m = m + 1;
		m = 1;
		y = y + 1;
	
	while ( m < em ):
		num = days_in_month(ey, m);
		while ( d <= num ):
			str = "%d%02d%02d" % (y, m, d);
			fp.write(str+" unassigned"+'\n');
			d = d + 1;
		d = 1;
		m = m + 1;
	
	while ( d <= ed ):
		str = "%d%02d%02d" % (y, m, d);
		fp.write(str+" unassigned"+'\n');
		d = d + 1;

	fp.close();

def auth_node(secret_file, node_id, node_key):
	fp = open(secret_file,'r');
	for line in fp.readlines():
		list = line.split(' ');
		if (list[0] == node_id and list[1].strip('\n') == node_key):
			fp.close();
			return True;
	
	fp.close();
	return False;
			
#enum state={finished, unassigned, pending, expired};
def change_state(file_name, date, state):
	fp = open(file_name, 'r');
	lines = fp.readlines();
	fp.close();
	
	fp = open(file_name, 'w');
	for line in lines:
		if (line.split(' ')[0] == date):
			fp.write(date+" "+state);
		else:
			fp.write(line);
	fp.close();

def get_task():
	fp = open(file_name, 'r');
	lines = fp.readlines();
	res = "";
	for i in range(len(lines)-1, -1, -1):
		if(lines[i].split(' ')[1].strip('\n') == "false"):
			res = lines[i];
			break;
		
	return res;

def on_notify():
	

if __name__ == "__main__":
	
#update_state_file("state","20160727",start_time="20070913",is_init=True);
#update_state_file("state","20160802");
