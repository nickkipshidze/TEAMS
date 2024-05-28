from http.server import HTTPServer
from server import HTTPRequestHandler

def main():
    serveraddr = ("127.0.0.1", 3301)
    httpd = HTTPServer(serveraddr, HTTPRequestHandler)
    print(f"{serveraddr[0]} - [+] Starting server on port {serveraddr[1]}...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()