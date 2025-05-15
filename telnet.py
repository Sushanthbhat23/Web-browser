import socket

class URL:
    # parses through the url 
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"

        # FIX: Changed the condition to handle paths correctly
        if "/" in url:
            self.host, url = url.split("/", 1)
            self.path = "/" + url
        else:
            self.host = url
            self.path = "/"

    # sets up connection between 2 computers  
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, 80))

        # sets up request to the other server
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n") # used to read the servers response

        # splitting response into pieces and recording statusline
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        # recording header
        response_headers = {}
        while True:
            line = response.readline()
            if line == '\r\n': break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

            # making sure that certain headers that tell us data is sent in an unusual way is not present
            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers

            # reading other content
            content = response.read()
            s.close()
            return content # returns the content that has been read in this function
        
    def show(self, body):
        in_tag = False
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False  # FIX: Changed to False (was True before)
            elif not in_tag:
                print(c, end="")  # NOTE: Removed extra space for cleaner output
    
    # loading the url
    def load(self):  # FIX: Removed `url` parameter since `self` already contains the URL
        body = self.request()  # NOTE: Uses the URL stored in `self`
        self.show(body)

if __name__ == "__main__":
    import sys
    url = URL(sys.argv[1])  # Parse the URL from command line
    url.load()  # Now correctly calls `load()` without arguments
        