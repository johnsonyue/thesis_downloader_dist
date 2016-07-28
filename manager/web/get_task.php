<?php
	$code_path = parse_init_file("config.ini");
	$node_id = $_POST["node_id"];
	$node_key = $_POST["node_key"];
	
	echo exec ("python ".$code_path."/run.py auth ".$node_id." ".$node_key);
?>
