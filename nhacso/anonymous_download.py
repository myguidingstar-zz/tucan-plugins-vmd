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
			it = URLOpen().open('http://nhacso.net/flash/song/xnl/1/id/'+url[-13:-5])
			for line in it:
				if '<mp3link><![CDATA[' in line:
					mp3link = line.split('<mp3link><![CDATA[')[1].split(']]></mp3link>')[0].strip()
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
			it = URLOpen().open('http://nhacso.net/flash/song/xnl/1/id/'+url[-13:-5])
			for line in it:
				if '<name><![CDATA[' in line:
					name = line.split('<name><![CDATA[')[1].split(']]></name>')[0].strip()
				if '<mp3link><![CDATA[' in line:
					mp3link = line.split('<mp3link><![CDATA[')[1].split(']]></mp3link>')[0].strip()
					#get file size before download
					site = urllib.urlopen(mp3link)
					meta = site.info()
					size = int(meta.getheaders("Content-Length")[0]) / 1024
					if size > 1024:
						unit = "KB"
						name = None
						size = -1
						unit = None
						break
					else:
						size_found = 0
				#remove from old version: 
				#if '<songlink><![CDATA[' in line:
					#songlink =line.split('<songlink><![CDATA[')[1].split(']]></songlink>')[0].strip()
					#if not (songlink == url):
						#name = None
						#size = -1
						#unit = None
						#break
				if '<artist><![CDATA[' in line:
					name +=' - '+line.split('<artist><![CDATA[')[1].split(']]></artist>')[0].strip()
					name += '.mp3'

		except Exception, e:
			name = None
			size = -1
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
