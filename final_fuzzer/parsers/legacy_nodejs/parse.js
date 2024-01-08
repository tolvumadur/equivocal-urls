#!/usr/bin/node

const readline = require("readline");
const legacy_url = require("url");

function b64(thing) {
  if (thing == null) {
    return "";
  }
  //return thing.toString();
  //console.log(thing);
  b = new Buffer(thing);
  //console.log(b.toString("base64"));
  return b.toString("base64");
}

const rl = readline.createInterface({
  input: process.stdin,
  output : null, 
  terminal : false
});

rl.on('line', function(input){
  //console.log(input.trim());
  //console.log(input.slice(2,-1));
  //console.log(typeof(input));
  let url_b64_buff = new Buffer(input, 'ascii');
  //console.log(url_b64_buff);
  //console.log(typeof(url_b64_buff));
  let url_b64 = url_b64_buff.toString("ascii");
  //console.log(url_b64);
  //console.log(typeof(url_b64));
  let url_buff = new Buffer(url_b64, "base64");

  try {

    //console.log(url_buff);

    let url = legacy_url.parse(url_buff.toString());

    if (url == null) {
	    throw new Error("URL failed to parse");
    }

    if (url.hostname == null && url.auth == null && url.protocol == null) {
      console.log("URL decoded incorrectly from base64" + url_buff.toString(""));
      process.exit(15);
    }

    let report = 
      `NodeJS Legacy` + '\t' + 
      b64(url.protocol) + "\t" + //Scheme
      b64((url.auth ? url.auth + "@" : "") + url.hostname + (url.port ? ":" + url.port : "")) + "\t" + //Authority
      b64(url.auth ? url.auth : "") + "\t" + //UserInfo
      b64(url.hostname ? url.hostname : "") + "\t" + //Hostname
      b64(url.port == null ? "" : url.port ) + "\t" + //Port
      b64(url.pathname) + "\t" + //Path
      b64(url.query)  + "\t" + //Query
      b64(url.hash)   + "\t" + //Fragment
    "";    

    let report2 = 
    `NodeJS Legacy` + '\t' + 
    (url.protocol) + "\t" + //Scheme
    ((url.auth ? url.auth + "@" : "") + url.hostname + (url.port ? ":" + url.port : "")) + "\t" + //Authority
    (url.auth ? url.auth : "[4]") + "\t" + //UserInfo
    (url.hostname ? url.hostname : "[5]") + "\t" + //Hostname
    (url.port == null ? "[6]" : url.port ) + "\t" + //Port
    (url.pathname) + "\t" + //Path
    (url.query)  + "\t" + //Query
    (url.hash)   + "\t" + //Fragment
    ""; 


    console.log(report);
    //console.log(report2);

    process.exit(0);
  }
  catch (error) {
    let error_report = `NodeJS Legacy\t\t\t\t\t\t\t\t\t${error}`;
    //console.log(error.stack);
    console.log(error_report);
    process.exit(0);
  }
});



