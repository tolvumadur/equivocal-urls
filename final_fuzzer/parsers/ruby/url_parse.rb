#!/usr/bin/ruby
require "base64"
require "uri"

until ARGV.empty? do
  desc = ARGV.shift
end

errors = ""

url_b64 = gets

def esc(s)
  if s.nil? then
    return ""
  end
  if s.is_a? Integer
    return Base64.strict_encode64(s.to_s)
  end
  return Base64.strict_encode64(s)
end

url = Base64.decode64(url_b64)
begin
  u = URI(url)
rescue URI::InvalidURIError => err
    errm = err.message.split("\n")[0]
    puts "Ruby uri\t\t\t\t\t\t\t\t\t#{(errm)}'}"
    exit
end

ufo = u.userinfo
username = ufo
password = ""

if (!ufo.nil?) then 
    if ufo.include? ':' then
      ufo_arr = ufo.split(':', 2)
      username = ufo_arr[0]
      password = ufo_arr[1]
    end
end

#query_parameters = "{}"
#if !u.query.nil? then 
#  query_parameters = URI.decode_www_form(u.query)
#end

#if "#{query_parameters}".eql? "[]"
#  query_parameters = "{}"
#end

authority = ""

unless u.host.nil?
  authority = u.host
end

unless u.port.nil?
  authority = authority + ":" + u.port.to_s
end
unless u.userinfo.nil? || u.userinfo == ""
  authority = u.userinfo + "@" + authority
end

puts "Ruby uri\t#{esc(u.scheme)}\t#{esc(authority)}\t#{esc(u.userinfo)}\t#{esc(u.host)}\t#{esc(u.port)}\t#{esc(u.path)}\t#{esc(u.query)}\t#{esc(u.fragment)}\t"
