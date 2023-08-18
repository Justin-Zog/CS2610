import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path


class CS2610Assn1(BaseHTTPRequestHandler):
    def do_GET(self):

        path = self.path
        self.handlePaths(path)


    def handlePaths(self, path):

        strippedPath = path.strip("/")

        if Path(strippedPath).is_file():
            if "404" in strippedPath:
                self.wfile.write(b"HTTP/1.1 404 Not Found\n")
            elif "418" in strippedPath:
                self.wfile.write(b"HTTP/1.1 418 I'm a Teapot\n")
            elif "403" in strippedPath:
                self.wfile.write(b"HTTP/1.1 403 Forbidden\n")
            else:
                self.wfile.write(b"HTTP/1.1 200 OK\n")

            self.sendHeaders(strippedPath, False)
            return

        elif path == "/":
            self.wfile.write(b"HTTP/1.1 301 Redirected\n")
            self.send_header("Location", "/index.html")

        elif "bio" in strippedPath.lower():
            self.wfile.write(b"HTTP/1.1 301 Redirected\n")
            self.send_header("Location", "/about.html")

        elif strippedPath.lower() == "tips" or strippedPath.lower() == "help":
            self.wfile.write(b"HTTP/1.1 301 Redirected\n")
            self.send_header("Location", "/techtips+css.html")

        elif strippedPath.lower() == "teapot":
            self.wfile.write(b"HTTP/1.1 301 Redirected\n")
            self.send_header("Location", "/418.html")

        elif strippedPath.lower() == "forbidden":
            self.wfile.write(b"HTTP/1.1 301 Redirected\n")
            self.send_header("Location", "/403.html")

        elif strippedPath.lower() == "debugging":
            self.wfile.write(b"HTTP/1.1 200 OK\n")
            self.sendHeaders(strippedPath, True)
            return

        elif Path(strippedPath + ".html").is_file():
            self.wfile.write(b"HTTP/1.1 301 Redirected\n")
            self.send_header("Location", f"{strippedPath}.html")

        else:
            self.wfile.write(b"HTTP/1.1 301 Redirected\n")
            self.send_header("Location", "/404.html")

        self.sendHeaders("", True)
        return


    def sendHeaders(self, path, is301):

        bytes_read = None

        self.send_header("Server", "Zawg's Magnificent Server")
        self.send_header("Date", f"{self.date_time_string()}")
        self.send_header("Cache-Control", "max-age=10")

        if not is301:
            f = open(path, "rb")
            bytes_read = f.read()
            f.close()
            fileSize = len(bytes_read)
            contentType = mimetypes.guess_type(path)[0]

            self.send_header("Content-Length", f"{fileSize}")
            self.send_header("Content-Type", f"{contentType}")

        if path == "debugging":
            self.send_header("Content-Type", "text/html")
            bytes_read = self.debugging()

        self.send_header("Connection", "close")
        self.end_headers()

        if not is301 or path == "debugging":
            self.wfile.write(bytes_read)


    def debugging(self):
        # Get the headers
        requestHeaders = ""

        for header, value in self.headers.items():
            requestHeaders += f"<li> <code> <em> {header}: {value} </em> </code> </li>\n"

        return (bytes(f'''<!DOCTYPE html>
<html lang='en'>
  <head>
    <title> Debugging Information </title>
    <meta charset='utf-8'>
    <link rel='stylesheet' href='style.css' type='text/css'>
  </head>
  <body>
    <div>
        <h1> Server Debugging Page </h1>
        <h2> All This Info At Your Fingertips </h2>
        <p> <code> You are visiting <em> {self.path} </em> from the IP address <em> {self.client_address[0]} </em> port number <em> {self.client_address[1]} </em> </code> </p>
        <p> <code> It is now {self.date_time_string()} </code> </p>
        <ul>
          <li> <code> <em> Command: </em> {self.command} </code> </li>
          <li> <code> <em> Path: </em> {self.path} </code> </li>
          <li> <code> <em> Request Version: </em> {self.request_version} </code> </li>
          <li> <code> <em> Version String: </em> {self.version_string()} </code> </li>
        </ul>
        <h4> Request Headers </h4>
        <ol>
          {requestHeaders}
        </ol>
        <p> <code> Go back: <a href="index.html"> Home </a> </code> </p>
    </div>
  </body>
</html>      
''', "utf-8"))


if __name__ == '__main__':
    server_address = ('localhost', 8000)
    print(f"Serving from http://{server_address[0]}:{server_address[1]}")
    print("Press Ctrl-C to quit\n")
    try:
        HTTPServer(server_address, CS2610Assn1).serve_forever()
    except KeyboardInterrupt:
        print(" Exiting")
        exit(0)
