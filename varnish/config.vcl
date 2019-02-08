vcl 4.0;

backend default {
  .host = "api";
  .port = "80";
}

/*
sub vcl_recv {
  if (req.method == "PURGE"){
    return (purge);
  }
  if (req.method == "REFRESH") {
    set req.method = "GET";
    set req.hash_always_miss = true;
  }
}
*/

sub vcl_backend_response {
  set beresp.ttl = 10s;

  if (bereq.url ~ "^/v1/challenges$") {
    set beresp.ttl = 5m;
  }
  else if (bereq.url ~ "^/v1$") {
    set beresp.ttl = 1y;
  }
}
