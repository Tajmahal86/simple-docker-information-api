import docker
import argparse
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _json(self, json):
        return json.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):

        data = []

        prefix = os.environ['CURRENT_PROJECT'] + '_web_run_'
        client = docker.from_env()
        for cron_container in client.containers.list(all=True, filters={"name": prefix}):
            item = {"name": cron_container.name}

            running_container = client.containers.get(cron_container.name)
            running_container_ps = running_container.top()

            item["status"] = running_container.status
            item["started_at"] = running_container.attrs['State']['StartedAt']

            if (running_container_ps['Processes']):
                for process in running_container_ps['Processes']:
                    # print(process)
                    if 'artisan' in process[7]:
                        item["process"] = process[7]
            data.append(item)

        self._set_headers()
        self.wfile.write(self._json(json.dumps(data)))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._json(json.dumps({"method": "POST!"})))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
