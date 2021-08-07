from detector import detect
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import tempfile
import uuid

hostName = "localhost"
serverPort = 8080
minProbability = 50

class FileUploadServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Received GET request")
        filename = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))

        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes("{", "utf-8"))
            print("Valid image found, detecting objects...")
            for detection in detect(filename, minProbability):
                self.wfile.write(bytes("""\"{0}\": {1},""".format(str(detection[0]), str(detection[1])), "utf-8"))
            self.wfile.write(bytes("}", "utf-8"))
            print("Object detection completed")
        except:
            print("sumting wong")
            self.send_response(500)


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), FileUploadServer)

    print("Awaiting commands...")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")