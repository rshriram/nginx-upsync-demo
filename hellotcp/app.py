# Copyright 2016 IBM Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

## Standard example from python docs
import SocketServer
import os

class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()

        service_version = os.getenv('A8_SERVICE', "hellotcp").split(':')
        version = service_version[1] if len(service_version) == 2 else 'UNVERSIONED'
        greetings='%s, version %s, host %s. Echoing %s' % (service_version[0], version, os.environ.get('HOSTNAME'), self.data)
        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(greetings)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
