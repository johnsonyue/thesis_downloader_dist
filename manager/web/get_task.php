<?php
	$config = parse_ini_file("config.ini");
	$code_path = $config["code_path"];

	$node_id = $_POST["id"];
	$node_key = $_POST["key"];
	
	if (exec("python $code_path/run.py auth ".$node_id." ".$node_key) == "True"){
		echo exec("python $code_path/run.py get_task");
	}
	else{
		echo "auth failed";
	}
?>
