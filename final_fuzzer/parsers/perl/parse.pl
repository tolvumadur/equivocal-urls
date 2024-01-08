#!/usr/bin/perl
#
#
use feature 'say';
use URI;
use MIME::Base64;

my $desc = $ARGV[0];

my $url_b64 = <STDIN> ;
 
my $url = decode_base64( $url_b64 );

#say $url;

my $u = 'URI'->new( $url );

sub Esc{  
  my $s = @_[0];
  return encode_base64( $s, "" );
}

printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s",
"Perl URI",
$u->can("scheme")    ? Esc($u->scheme)    : "",
$u->can('authority') ? Esc($u->authority) : "", #Auth
$u->can('userinfo')  ? Esc($u->userinfo)  : "",
$u->can('host')      ? Esc($u->host)      : "",
$u->can('port')      ? Esc($u->port)      : "",
$u->can('path')      ? Esc($u->path)      : "", #Path
$u->can('query')     ? Esc($u->query)     : "",
$u->can('fragment')  ? Esc($u->fragment)  : "",
""
;

exit 0;







