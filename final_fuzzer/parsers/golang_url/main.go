package main

import "os"
import "fmt"
import "net/url"
import "bufio"
import "encoding/base64"

func main() {

	if len(os.Args) != 2  {
		println("Error. No arguments given (or too many). Use 1 argument. use 'testing' for a built-in standalone test")
		os.Exit(2)
	}
	desc := os.Args[1]
	USE(desc)

	url_b64 := ""
	test_url := []byte("")
	errors := []string{}

	reader :=  bufio.NewReader(os.Stdin)
	url_b64, err := reader.ReadString('\n')
	if err != nil {
			errors = append(errors, "Failed to read URL from stdin: " + err.Error())
			println("Failed to read URL from stdin: ", err.Error())
	}
	test_url, err = base64.StdEncoding.DecodeString(url_b64)
	if err != nil {
			errors = append(errors, "Error decoding from base64: " + err.Error())
			println("Error decoding from base64: ", err.Error())
	}

	u, err := url.Parse(string(test_url))
	if err != nil {
		report_fail("Error parsing url: " + (err.Error()))
		//println("Error parsing url: ",err.Error())
	}
	defer func() {
		if r := recover(); r != nil {
			report_fail("Panic parsing url: " + (fmt.Sprintf("%v",r)))
		}
	}()

	report_answ(u)
}

func report_fail(err string) {
	fmt.Printf("Golang net/url\t\t\t\t\t\t\t\t\t" + err)
	os.Exit(0)
}

func report_answ(u *url.URL) {
	if u.User == nil {
	fmt.Println(
		"Golang net/url" + "\t" +
		b64(u.Scheme) + "\t" +
		b64(u.Host) + "\t" +
		"\t" +
		b64(u.Hostname()) + "\t" +
		b64(u.Port()) + "\t" +
		b64(u.Path) + "\t" +
		b64(u.RawQuery) + "\t" +
		b64(u.Fragment) + "\t" + "")
	} else {
		fmt.Println(
			"Golang net/url" + "\t" +
			b64(u.Scheme) + "\t" +
			b64(u.User.String()) + "@" + u.Host + "\t" +
			b64(u.User.String()) + "\t" +
			b64(u.Hostname()) + "\t" +
			b64(u.Port()) + "\t" +
			b64(u.Path) + "\t" +
			b64(u.RawQuery) + "\t" +
			b64(u.Fragment) + "\t" + "")
	}
}

func USE(whatever ...interface{}) {}

func b64(thing string) string {
	return base64.StdEncoding.EncodeToString([]byte(thing))
}