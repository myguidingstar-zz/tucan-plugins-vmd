###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import logging
logger = logging.getLogger(__name__)

import urllib

from core.download_plugin import DownloadPlugin
from core.url_open import URLOpen

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		link = None
		try:
			page = URLOpen().open(url)
			for lines in page:
				if 'xmlURL=http://mp3.zing.vn/xml/song-xml/' in lines:
					songxml = lines.split('xmlURL=http://mp3.zing.vn/xml/song-xml/')[1].split('&skin=http://static.mp3.zing.vn/skins')[0].strip()
					xml = URLOpen().open('http://mp3.zing.vn/xml/song-xml/'+songxml)
					for line in xml:
						if '<source><![CDATA[' in line:
							mp3link = line.split('<source><![CDATA[')[1].split(']]></source>')[0].strip()
					if not mp3link:
						return
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			try:
				handle = URLOpen().open(mp3link, None, content_range)
			except:
				return self.set_limit_exceeded()
			else:
				return handle


	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		size_found = 0
		try:
			# 'xmlURL=http://mp3.zing.vn/xml/song-xml/'
			page = URLOpen().open(url)
			for lines in page:
				if 'xmlURL=http://mp3.zing.vn/xml/song-xml/' in lines:
					songxml = lines.split('xmlURL=http://mp3.zing.vn/xml/song-xml/')[1].split('&skin=http://static.mp3.zing.vn/skins')[0].strip()
					xml = URLOpen().open('http://mp3.zing.vn/xml/song-xml/'+songxml)
					for line in xml:
						if '<title><![CDATA[' in line:
							name = line.split('<title><![CDATA[')[1].split(']]></title>')[0].strip()
						if '<source><![CDATA[' in line:
							mp3link = line.split('<source><![CDATA[')[1].split(']]></source>')[0].strip()
							#get file size before download
							site = urllib.urlopen(mp3link)
							meta = site.info()
							size = int(meta.getheaders("Content-Length")[0]) / 1024
							if size > 1024:
								unit = "KB"
							else:
								size_found = 0
								name = None
								size = -1
								unit = None
								break
						#if '<link><![CDATA[' in line:
							#songlink =line.split('<link><![CDATA[')[1].split(']]></link>')[0].strip()
							#if not (songlink == url):
								#name = None
								#size = -1
								#unit = None
								#break
						if '<performer><![CDATA[' in line:
							name +=' - '+line.split('<performer><![CDATA[')[1].split(']]></performer>')[0].strip()
							name += '.mp3'

		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
