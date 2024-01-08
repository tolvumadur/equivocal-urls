import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Base64;

class Parser
{

    private static String b64(String u) {
		if (u == null) {
			return "";
		}
		return Base64.getEncoder().encodeToString(u.getBytes());
    }    

    public static void main(String args[])
    {
        if (args.length != 1) {
            System.err.println("Wrong number of args. Expected 1, got " + String.valueOf(args.length));
            System.exit(1);
        }


        boolean t = false;
        if (args[0].equals("testing")) {
            System.out.println("This is a test, I see");
            t=true;
        }

        String input = "";
        String err = "";
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        try {
            input = br.readLine();

        }
        catch (IOException e) {
            System.err.println("Error reading input of url b64: " + e.getMessage());
        }
            
        if (t) {
            System.out.println(input);
        }

        byte[] decoded = Base64.getDecoder().decode(input);

        if (t) {
            System.out.println(new String(decoded));
        }

        String ufo = "";
		String authority = "";

        try {
            URI url = new URI(new String(decoded));
            ufo = url.getUserInfo();
        
			String report = String.format("Java.net.URI\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t",
			b64(url.getScheme()),
			b64(authority),
			b64(url.getUserInfo()),
			b64(url.getHost()),
			b64(String.valueOf(url.getPort())),
			b64(url.getPath()),
			b64(url.getQuery()),
			b64(url.getFragment())
			);

            System.out.println(report);
            System.exit(0);
    	}
		catch (URISyntaxException e) {
        	String report = e.getMessage();
	    	System.out.println(String.format("Java.net.URI\t\t\t\t\t\t\t\t\t%s", (report)));
		//report += e.getStackTrace();
            	//System.err.println(report);
        }
	}
}
