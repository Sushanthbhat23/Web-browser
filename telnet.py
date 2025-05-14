import socket

class URL:
    #parses through the url 
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"

        if "/" not in url:
            url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url

    #sets up connection between 2 computers  
    def request(self):
        s = socket.socket(
            family = socket.AF_INET,
            type = socket.SOCK_STREAM,
            proto = socket.IPPROTO_TCP,
        )
        s.connect((self.host, 80))

        #sets upe request to the other server
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding = "utf8", newline = "\r\n") #used to read the servers response

        #splitting response into pieces
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
    
        