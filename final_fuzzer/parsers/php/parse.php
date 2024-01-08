<?php

  function b64($s) {
	  return base64_encode($s);	
  }

  $stderr = fopen('php://stderr', 'w');

  if ($argc != 2) {
      fwrite($stderr,"Expected 2 args, got $argc. Abort\n");
      exit(1);
  }

  $desc = $argv[1];

  if (strcmp($desc,"testing") == 0) {
      echo "Test in progress...\n";
  } 

  $f = fopen( 'php://stdin', 'r' );

  $url_b64 = trim(fgets($f));

  $url = base64_decode($url_b64);

  if (strcmp($desc,"testing") == 0) {
    echo "Got URL. It is\n$url\n";
  } 

  $f = filter_var($url,FILTER_VALIDATE_URL, FILTER_NULL_ON_FAILURE);
  if ($f == null) {
    echo "PHP parse_url\t\t\t\t\t\t\t\t\tfilter_var does not recognize this url";
    exit(0);
  }


  $p = parse_url($url);

  if ($p == false) {
    echo "PHP parse_url\t\t\t\t\t\t\t\t\tparse_url failed to parse this url";
    exit(0);
  }

  $scheme   = isset($p['scheme'])   ? b64($p['scheme']) : '';
  $host     = isset($p['host'])     ? b64($p['host'])   : '';
  $port     = isset($p['port'])     ? b64($p['port'])   : '';
  $username = isset($p['user'])     ? b64($p['user'])   : '';

  $password = isset($p['pass'])     ? b64($p['pass'])   : '';
  $userinfo = "$username$password";
  $password = ($username || $password) ? "$password@" : '';
  $authority = ($port) ? "$username$password$host:$port" : "$username$password$host";

  $path     = isset($p['path'])     ? b64($p['path'])   : '';
  $query    = isset($p['query'])    ? b64($p['query'])  : '';
  $fragment = isset($p['fragment']) ? b64($p['fragment']) : '';

  $report = "PHP parse_url\t$scheme\t$authority\t$userinfo\t$host\t$port\t$path\t$query\t$fragment\t";

  echo $report
?>
