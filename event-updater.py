#Author: Petite Software
#Create Date: 24/04/2019
#Last Edit: 24/04/2019

from lxml import html
import cherrypy
import requests
from os.path import abspath
import json
import datetime
from dateutil import parser
import cherrypy_cors
cherrypy_cors.install()





class Events(object):
    @cherrypy.expose
    def index(self):
        return """ 
            <form method="post" action="UpdateEvents"> 
            Name:<input type="text" name="name"><br>
            Start Date:<input type="date" name="start_date"><br>
            Start Time:<input type="text" name="start_time"><br>
            End Date:<input type="date" name="end_date"><br>
            End Time:<input type="text" name="end_time"><br>
            Facebook link:<input type="text" name="fb_link"><br>
            Ticket Link:<input type="text" name="ticket_link"><br>
            Cover Src:<input type="text" name="cover_link"><br>
            Location Name:<input type="text" name="location"><br>
            <input type="submit"> 
            </form>
            """ 


 
    @cherrypy.expose()
    def getEventsJson(self):
            with open('events.json') as json_file:
                data = json.load(json_file)    
            return json.dumps(data)


    # @cherrypy.expose
    # def addEvent(self):
    # return """ 
    #     <form method="post" action="UpdateEvents"> 
    #     Name:<input type="text" name="name"><br>
    #     Start Date:<input type="date" name="start_date"><br>
    #     Start Time:<input type="text" name="start_time"><br>
    #     End Date:<input type="date" name="end_date"><br>
    #     End Time:<input type="text" name="end_time"><br>
    #     Facebook link:<input type="text" name="fb_link"><br>
    #     Ticket Link:<input type="text" name="ticket_link"><br>
    #     Cover Src:<input type="text" name="cover_link"><br>
    #     Location Name:<input type="text" name="location"><br>
    #     <input type="submit"> 
    #     </form>
    #     """ 



    @cherrypy.expose() 
    def UpdateEvents(self, name, start_date, start_time, end_date, end_time, fb_link, ticket_link, cover_link, location): 
        event = {
            "name": name,
            "start_date": start_date,
            "start_time": start_time,
            "end_date": end_date,
            "end_time": end_time,
            "fb_link": fb_link,
            "ticket_link": ticket_link,
            "cover_link": cover_link,
            "location": location
        }

        with open('events.json') as json_file:
            now = datetime.datetime.now()
            data = json.load(json_file)
            for p in data['events']:
                if parser.parse(p['end_date']) < now:
                    print(p['name'])
                    del p
                 
        
        data['events'].append(event)
        
        with open('events.json', 'w') as outfile:
            json.dump(data, outfile)

        eventsHtml = "<div>"
        for p in data['events']:
            eventsHtml += " <div class='responsive'> "
            eventsHtml+= "<div class='gallery'>"
            # eventsHtml += "<a target='_blank' href='" + p['fb_link'] + "'>"
            # eventsHtml += "<img src='"+ p['cover_link'] +"' alt='Cinque Terre' width='600' height='400'>"
            eventsHtml +=  "</a>"
            eventsHtml += "<div class='desc'>" + p['name']+ "</div>"
            eventsHtml += "</div>"
            eventsHtml += "</div>"
        eventsHtml += "</div>"


        return """ 
            <form method="post" action="UpdateEvents"> 
            Name:<input type="text" name="name"><br>
            Start Date:<input type="date" name="start_date"><br>
            Start Time:<input type="text" name="start_time"><br>
            End Date:<input type="date" name="end_date"><br>
            End Time:<input type="text" name="end_time"><br>
            Facebook link:<input type="text" name="fb_link"><br>
            Ticket Link:<input type="text" name="ticket_link"><br>
            Cover Src:<input type="text" name="cover_link"><br>
            Location Name:<input type="text" name="location"><br>
            <input type="submit"> 
            </form>


            """  + eventsHtml

# def CORS():
#     cherrypy.response.headers["Access-Control-Allow-Origin"] = "http://localhost"

# if __name__ == '__main__':
#     conf = {
#         '/': {
#             'tools.response_headers.on': True,
#             'tools.response_headers.headers': [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', 'http://localhost')],
#             'server.socket_host': 'http://localhost',
#             'server.socket_port': 8888
#         }
#     }

# cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
cherrypy.quickstart(Events())

