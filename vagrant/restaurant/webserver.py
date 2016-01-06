from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from string import Template

import database_setup as ds
import cgi
import re

engine = create_engine('sqlite:///restaurantmenu.db')
ds.Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)

delete_regex = re.compile("/restaurant/\d*/delete$")
edit_regex = re.compile("/restaurant/\d*/edit$")


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += hello_form_tmpl()
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants"):
                session = db_session()
                restaurants = ds.fetch_restaurants(session)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += ''' <a href='/restaurants/new'> New Restaurant</a> </br> </br>'''

                for restaurant in restaurants:
                    output += restaurant.name + " <a href='restaurant/" + str(
                        restaurant.id) + "/edit'>edit</a>" + " <a href='restaurant/" + str(
                        restaurant.id) + "/delete'>delete</a>" + "</br>"

                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += restaurant_form_tmpl()
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = db_session()

                path_c = self.path.split('/')
                r_id = path_c[2]
                restaurant = ds.fetch_restaurant(session, r_id)

                output = ""
                output += "<html><body>"

                if restaurant:
                    tmpl = restaurant_delete_tmpl()
                    output += tmpl.safe_substitute(name=restaurant.name, ID=str(restaurant.id))
                    output += self.path + " " + type(self.path).__name__ + " " + str(path_c[2]) + " " + str(path_c)
                else:
                    pass

                output += "</body></html>"
                self.wfile.write(output)
                return

            if edit_regex.search(self.path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = db_session()

                path_c = self.path.split('/')
                r_id = path_c[2]
                restaurant = ds.fetch_restaurant(session, r_id)

                output = ""
                output += "<html><body>"

                if restaurant:
                    tmpl = restaurant_edit_tmpl()
                    output += tmpl.safe_substitute(name=restaurant.name, ID=str(restaurant.id))

                output += "</body></html>"
                self.wfile.write(output)
                return

            else:
                output = ""
                match = edit_regex.search(self.path)
                print str(match)
                raise IOError

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)


    def do_POST(self):
        # noinspection PyBroadException
        try:
            if self.path.endswith("/hello"):
                self.send_response(301)
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('message')

                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % message_content[0]
                output += hello_form_tmpl()
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if self.path.endswith("/restaurants/new"):

                session = db_session()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')
                    print type(name)
                    ds.create_restaurant(session, name[0])

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if delete_regex.search(self.path):

                session = db_session()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    message_content = fields.get('message')

                    restaurant = ds.fetch_restaurant(session, int(message_content[0]))

                    if restaurant:
                        ds.delete_restaurant(session, restaurant)

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if edit_regex.search(self.path):

                session = db_session()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name_content = fields.get('name')
                    id_content = fields.get('ID')

                    restaurant = ds.update_restaurant(session, id_content[0], name_content[0])

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

        except:
            pass


def restaurant_form_tmpl():
    return '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                    <h2>Restaurant Name: </h2><input name="name" type="text" >
                    <input type="submit" value="Submit"> </form>'''


def restaurant_delete_tmpl():
    return Template('''<form method='POST' enctype='multipart/form-data' action='/restaurant/$ID/delete'>
                    <h2>Delete $name with id: $ID </h2>
                    <input name="message" type="hidden" value="$ID" ><input type="submit" value="Delete">
                    <a href="/restaurants">Cancel</a></form>''')

def hello_form_tmpl():
    return '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name="message" type="text" ><input type="submit" value="Submit"> </form>'''


def restaurant_edit_tmpl():
    return Template('''<form method='POST' enctype='multipart/form-data' action='/restaurant/$ID/edit'>
                    <h2>Edit $name with id: $ID </h2>
                    <input name="ID" type="hidden" value="$ID" >
                    <input name="name" value="$name" >
                    <input type="submit" value="Edit">
                    <a href="/restaurants">Cancel</a></form>''')


def main():
    try:
        port = 8081
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server... "
        server.socket.close()


if __name__ == '__main__':
    main()

