'''
Copyright (c) 2012, Tarek Galal <tarek@wazapp.im>

This file is part of Wazapp, an IM application for Meego Harmattan platform that
allows communication with Whatsapp users

Wazapp is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation, either version 2 of the License, or (at your option) any later 
version.

Wazapp is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
Wazapp. If not, see http://www.gnu.org/licenses/.
'''

import httplib,urllib
from utilities import Utilities
from xml.dom import minidom

import threading
from PySide import QtCore
from PySide.QtCore import QThread
#from wadebug import StatusRequestDebug

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

class WAMediaUploader(QThread):

	status = None
	result = None
	params = []
	conn = None
	
	done = QtCore.Signal(str);
	fail = QtCore.Signal();

	def __init__(self):
		#_d = StatusRequestDebug();
		#self._d = _d.debug;
		register_openers()
		super(WAMediaUploader,self).__init__();

	def onResponse(self, name, value):
		if name == "status":
			self.status = value
		elif name == "result":
			self.result = value
			
	def addParam(self,name,value):
		self.params.append({name:value.encode('utf-8')});

	def clearParams(self):
		self.params = [];
	
	def getUrl(self):
		return  self.base_url+self.req_file;

	def getUserAgent(self):
		agent = "WhatsApp/1.2 S40Version/microedition.platform";
		#agent = "WhatsApp/2.6.7 iPhone_OS/5.0.1 Device/Unknown_(iPhone4,1)";
		return agent;	
	
	

	def sendRequest(self, image, name):
		image = image.replace("file://","")
		self.params =  [param.items()[0] for param in self.params];
		
		params = urllib.urlencode(self.params);
		
		print "Opening connection to "+self.base_url;
		#self.conn = httplib.HTTPSConnection(self.base_url,443);
		'''headers = {"User-Agent":self.getUserAgent(),
			"Content-Type":"application/x-www-form-urlencoded",
			"Accept":"*/*",
			"Accept-Language":"en-us",
			"Accept-Encoding":"gzip, deflate"
			};
		
		print headers;
		print params;'''

		print "Uploading "+image;
		datagen, headers = multipart_encode(name,{"file": open(image, "rb")})
		
		print datagen;
		print headers;

		request = urllib2.Request("https://mms.whatsapp.net/client/iphone/upload.php", datagen, headers)
		print urllib2.urlopen(request).read()

		
		'''self.conn.request("POST",self.req_file,datagen,headers);
		resp=self.conn.getresponse()
 		response=resp.read();
 		self._d(response);
 		self.done.emit(response);
 		return response;'''


