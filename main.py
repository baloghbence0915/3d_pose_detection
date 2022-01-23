from http.server import HTTPServer
from server.APIServerModule import APIServer

hostName = "0.0.0.0"
serverPort = 8080

webServer = HTTPServer((hostName, serverPort), APIServer)

try:
    print("Server starts at http://%s:%s" % (hostName, serverPort))
    webServer.serve_forever()
except:
    pass

webServer.server_close()
print("Server stopped.")
