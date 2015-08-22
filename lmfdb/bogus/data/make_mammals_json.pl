#!/usr/bin/perl

while (<>) {
  chomp;
  ($name, $common, $rank, $value) = split /:/;
  $common = lc($common);

print<<HERE
{"name":"$name","common":"$common","rank":"$rank","value":"$value"}
HERE
}
