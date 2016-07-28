<?php
	$node_id = $_POST["node_id"];
	$node_key = $_POST["node_key"];
	
	echo exec ("python ../run.py auth "+$node_id+" "+$node_key);
?>
