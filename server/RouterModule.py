from http import HTTPStatus
from http.server import BaseHTTPRequestHandler


class Router(BaseHTTPRequestHandler):
    def do_GET(self):
        self.get_full_method_handler(self.command, self.path)

    def do_POST(self):
        self.get_full_method_handler(self.command, self.path)

    def do_PUT(self):
        self.get_full_method_handler(self.command, self.path)

    def do_DELETE(self):
        self.get_full_method_handler(self.command, self.path)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()


    def get_full_method_handler(self, command, path):
        mname = command + path.replace('/', '_')
        if mname.endswith('_') and len(mname) > 4:
            mname = mname[:-1]

        if not hasattr(self, mname):
            self.send_error(
                HTTPStatus.NOT_IMPLEMENTED,
                "Unsupported path (%r)" % path)
            return
        method = getattr(self, mname)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        method()

    def log_message(self, format, *args):
        pass
