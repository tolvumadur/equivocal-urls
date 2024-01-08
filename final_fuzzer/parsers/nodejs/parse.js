#!/usr/bin/node

const readline = require("readline")

function b64(thing) {
  b = new Buffer(thing);
  return b.toString("base64");
}

const rl = readline.createInterface({
  input: process.stdin,
  output : null, 
  terminal : false
});

rl.on('line', function(input){
  //console.log(input.trim());
  let url_buff = new Buffer(input.trim(), 'base64')
  
  try {
    let url = new URL(url_buff);

    let auth = (url.username || url.password) ? (url.username ? url.username : "") + (url.password ? ":" + url.password : "" ) : undefined 

    let report = 
      `WHATWG NodeJS` + '\t' + 
      b64(url.protocol) + "\t" + //Scheme
      b64((auth ? auth + "@" : "") + url.hostname + (url.port ? ":" + url.port : "")) + "\t" + //Authority
      b64(auth ? auth : "") + "\t" + //UserInfo
      b64(url.hostname) + "\t" + //Hostname
      b64(url.port) + "\t" + //Port
      b64(url.pathname) + "\t" + //Path
      b64(url.search)  + "\t" + //Query
      b64(url.hash)   + "\t" + //Fragment
    "";    

    console.log(report);

    process.exit(0);
  }
  catch (error) {
    let error_report = `WHATWG NodeJS\t\t\t\t\t\t\t\t\t${error}`;

    console.log(error_report);
    //console.log(new URL(url_buff))
    process.exit(0);
  }
});



