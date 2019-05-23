# -*- coding: utf-8 -*-
###################################################
# 2019-05-23 by Alec - M4 SPORT
###################################################
HOST_VERSION = "1.0"
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _, SetIPTVPlayerLastHostError
from Plugins.Extensions.IPTVPlayer.components.ihost import CHostBase, CBaseHostClass
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, MergeDicts
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper import getDirectM3U8Playlist, getF4MLinksWithMeta, getMPDLinksWithMeta
from Plugins.Extensions.IPTVPlayer.libs.urlparser import urlparser
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads, dumps as json_dumps
from Plugins.Extensions.IPTVPlayer.libs import ph
###################################################

###################################################
# FOREIGN import
###################################################
import os
import urlparse
import datetime
import time
import zlib
import cookielib
import urllib
import base64
from hashlib import sha1
from Components.config import config, ConfigText, ConfigYesNo, getConfigListEntry
from Tools.Directories import resolveFilename, fileExists, SCOPE_PLUGINS
from Screens.MessageBox import MessageBox
###################################################

###################################################
# Config options for HOST
###################################################
config.plugins.iptvplayer.m4sport_id = ConfigYesNo(default = False)

def GetConfigList():
    optionList = []
    optionList.append(getConfigListEntry("m4sport_id:", config.plugins.iptvplayer.m4sport_id))
    return optionList
###################################################

def gettytul():
    return 'M4 Sport'

class m4sport(CBaseHostClass):

    def __init__(self):
        CBaseHostClass.__init__(self, {'history':'m4sport.hu', 'cookie':'m4sport.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
        self.HEADER = {'User-Agent':self.USER_AGENT, 'DNT':'1', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, br'}
        self.AJAX_HEADER = dict(self.HEADER)
        self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest'} )
        self.MAIN_URL = zlib.decompress(base64.b64decode('eJzLKCkpKLbS1y8vL9fLNSkuyC8q0cso1S/LTEnNz9YHAK3xCyM='))
        self.DEFAULT_ICON_URL = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c81KS7ILyqJz8lPz9cryEsHAI25EXM='))
        self.ICON_URL_ELO = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c81KS7ILyqJz8lPz49PzcnXK8hLBwDYJxMS'))
        self.ICON_URL_FOCI = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c81KS7ILyqJz8lPz49Py0/O1CvISwcA66gTcw=='))
        self.aid = config.plugins.iptvplayer.m4sport_id.value
        self.aid_ki = ''
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        
    def getFullIconUrl(self, url):
        url = url.replace('&amp;', '&')
        return CBaseHostClass.getFullIconUrl(self, url)
        
    def getPage(self, baseUrl, addParams = {}, post_data = None):
        if addParams == {}:
            addParams = dict(self.defaultParams)
        
        def _getFullUrl(url):
            if self.cm.isValidUrl(url):
                return url
            else:
                return urlparse.urljoin(baseUrl, url)
            
        addParams['cloudflare_params'] = {'domain':self.up.getDomain(baseUrl), 'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT, 'full_url_handle':_getFullUrl}
        sts, data = self.cm.getPageCFProtection(baseUrl, addParams, post_data)
        return sts, data
        
    def listMainMenu(self, cItem):
        try:
            n_bx = self.malvadst('1', '11', 'm4_boxutca')
            if n_bx != '' and self.aid:
                self.aid_ki = 'ID: ' + n_bx + '\n'
            else:
                self.aid_ki = ''
            msg_boxutca = self.aid_ki + 'm4sport - v' + HOST_VERSION + '\n\nBoxutca adásainak megjelenítése...'
            n_f = self.malvadst('1', '11', 'm4_foci')
            if n_f != '' and self.aid:
                self.aid_ki = 'ID: ' + n_f + '\n'
            else:
                self.aid_ki = ''
            msg_foci = self.aid_ki + 'Magyar Foci adásainak megjelenítése...'
            n_sh = self.malvadst('1', '11', 'm4_sporthirek')
            if n_sh != '' and self.aid:
                self.aid_ki = 'ID: ' + n_sh + '\n'
            else:
                self.aid_ki = ''
            msg_sporthirek = self.aid_ki + 'Sporthírek adásainak megjelenítése...'
            n_sk = self.malvadst('1', '11', 'm4_kozvetitesek')
            if n_sk != '' and self.aid:
                self.aid_ki = 'ID: ' + n_sk + '\n'
            else:
                self.aid_ki = ''
            msg_kozvetitesek = self.aid_ki + 'Sportközvetítések megjelenítése...'
            n_krs = self.malvadst('1', '11', 'm4_kereses')
            if n_krs != '' and self.aid:
                self.aid_ki = 'ID: ' + n_krs + '\n'
            else:
                self.aid_ki = ''
            msg_kereses = self.aid_ki + 'Keresés eredményeinek megjelenítése...'
            n_krse = self.malvadst('1', '11', 'm4_kereses_elozmeny')
            if n_krse != '' and self.aid:
                self.aid_ki = 'ID: ' + n_krse + '\n'
            else:
                self.aid_ki = ''
            msg_keres_elozmeny = self.aid_ki + 'Keresés az előzmények között...'
            n_elo = self.malvadst('1', '11', 'm4_elo')
            if n_elo != '' and self.aid:
                self.aid_ki = 'ID: ' + n_elo + '\n'
            else:
                self.aid_ki = ''
            msg_elo = self.aid_ki + 'M4 élőadásának megjelenítése...'
            MAIN_CAT_TAB = [{'category': 'list_main', 'title': 'BOXUTCA', 'tab_id': 'boxutca', 'desc': msg_boxutca, 'icon':self.DEFAULT_ICON_URL},
                            {'category': 'list_main', 'title': 'MAGYAR FOCI', 'tab_id': 'foci', 'desc': msg_foci, 'icon':self.ICON_URL_FOCI},
                            {'category': 'list_main', 'title': 'SPORTHÍREK', 'tab_id': 'sporthirek', 'desc': msg_sporthirek, 'icon':self.DEFAULT_ICON_URL},
                            {'category': 'list_main', 'title': 'SPORTKÖZVETÍTÉSEK', 'tab_id': 'kozvetitesek', 'desc': msg_kozvetitesek, 'icon':self.DEFAULT_ICON_URL},
                            {'category': 'search', 'title': 'Keresés', 'search_item': True, 'tab_id': 'kereses', 'desc': msg_kereses, 'icon':self.DEFAULT_ICON_URL },
                            {'category': 'search_history', 'title': 'Keresés az előzmények közt', 'tab_id': 'keres_elozmeny', 'desc': msg_keres_elozmeny, 'icon':self.DEFAULT_ICON_URL}
                           ]
            self.listsTab(MAIN_CAT_TAB, cItem)
            pvt = 'M4 ÉLŐADÁSA'
            pvd = msg_elo
            pvu = zlib.decompress(base64.b64decode('eJzLKCkpKLbS1y8vL9fLTU3JTMzOyczO1sso1c810U3NydcHANGcC+w='))
            icon = self.ICON_URL_ELO
            params = MergeDicts(cItem, {'good_for_fav':False, 'title':pvt, 'url':pvu, 'url2':pvu, 'desc':pvd, 'icon':icon, 'md': 'elo'})
            self.addVideo(params)
        except Exception:
            printExc()
            
    def listMainItems(self, cItem):
        mig = 4
        try:
            tabID = cItem.get('tab_id', '')
            if tabID == 'boxutca':
                self.susn('2', '11', 'm4_boxutca')
                cid = '548'
                bid = '4'
            elif tabID == 'foci':
                self.susn('2', '11', 'm4_foci')
                cid = '768'
                bid = '4'
            elif tabID == 'sporthirek':
                self.susn('2', '11', 'm4_sporthirek')
                cid = '1020'
                bid = '4'
            elif tabID == 'kozvetitesek':
                self.susn('2', '11', 'm4_kozvetitesek')
                cid = '1025'
                bid = '4'
                mig = 7
            params = dict(self.defaultParams)
            params['header'] = dict(self.AJAX_HEADER)
            pue = zlib.decompress(base64.b64decode('eJw1yTEOwyAMQNHbZCteOlWKOvQIPQAiwQIqwBaYOlHVu7cL09fXiyLcbwCqasq1MzUxcYDyZacqWAU4j5BqB8GM040mH1A6zFbU59geTjBQO8G93GEzOV+ooeHI992JTX79fBemLlZOxvWdPNKyZQqTXEBbR9mw/fcHOtA8OQ=='))
            for x in range(1, mig):
                puf = pue.format(cid,bid,str(x))
                sts, data = self.getPage(puf, params)
                if not sts: return
                if len(data) == 0: return
                data = json_loads(data)
                for item in data:
                    title = item['title']
                    date_str = item['date'][0:10].replace('.','/').strip()
                    url = item['link']
                    rstr = 'video/' + date_str + '/' 
                    url2 = url.replace('videok//',rstr)
                    desc = item['date'] + '-i adás\n\nA műsor tartalma:\n' + title
                    icon = item['image']
                    params = {'title':title, 'url':url, 'url2':url2, 'desc':desc, 'icon':icon, 'md': 'egyeb'}
                    self.addVideo(params)
        except Exception:
            printExc()

    def listSecondItems(self, cItem):
        try:
            tabID = cItem.get('tab_id', '')
            return
        except Exception:
            printExc()
        
    def getLinksForVideo(self, cItem):
        url = cItem['url']
        url2 = cItem['url2']
        md = cItem['md']
        if md == 'elo':
            self.susn('2', '11', 'm4_elo')
        videoUrls = []
        turl = self.kvlva(url)
        if len(turl) == 0:
            turl = self.kvlva(url2)
        uri = urlparser.decorateParamsFromUrl(turl)
        protocol = uri.meta.get('iptv_proto', '')
        if protocol == 'm3u8':
            retTab = getDirectM3U8Playlist(uri, checkExt=False, checkContent=True)
            videoUrls.extend(retTab)
        elif protocol == 'f4m':
            retTab = getF4MLinksWithMeta(uri)
            videoUrls.extend(retTab)
        elif protocol == 'mpd':
            retTab = getMPDLinksWithMeta(uri, False)
            videoUrls.extend(retTab)
        else:
            videoUrls.append({'name':'direct link', 'url':uri})
        return videoUrls
        
    def kvlva(self, pu=''):
        bu = ''
        try:
            if pu != '':
                sts, data = self.getPage(pu)
                if not sts: return ''
                if len(data) == 0: return ''
                tn = self.cm.ph.getDataBeetwenMarkers(data, 'token":"', '","', False)[1]
                if len(tn) == 0:
                    tn = self.cm.ph.getDataBeetwenMarkers(data, 'streamId":"', '","', False)[1]
                    if len(tn) == 0: return ''
                tul = zlib.decompress(base64.b64decode('eJzLKCkpKLbS1y/ISaxMLdLLTU3JTMzOyczO1ssohQrmpZbDpAsyCuzLMlNS820BYd8Vcw==')) + tn
                sts, data = self.getPage(tul)
                if not sts: return ''
                if len(data) == 0: return ''
                vl = self.cm.ph.getDataBeetwenMarkers(data, 'file": "', '",', False)[1]
                if len(vl) == 0: return ''
                vl = vl.replace('\/','/')
                if vl.startswith('/'):
                    vl = 'https:' + vl
                if not self.cm.isValidUrl(vl):
                    return ''
                if len(vl) != '':
                    bu = vl
        except Exception:
            return ''
        return bu
        
    def malvadst(self, i_md='', i_hgk='', i_mpu=''):
        uhe = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c9IzanUL04sSdQvS8wD0ilJegUZBQD8FROZ'))
        pstd = {'md':i_md, 'hgk':i_hgk, 'mpu':i_mpu}
        t_s = ''
        temp_vn = ''
        temp_vni = ''
        try:
            if i_md != '' and i_hgk != '' and i_mpu != '':
                sts, data = self.cm.getPage(uhe, self.defaultParams, pstd)
                if not sts: return t_s
                if len(data) == 0: return t_s
                data = self.cm.ph.getDataBeetwenMarkers(data, '<div id="div_a_div', '</div>')[1]
                if len(data) == 0: return t_s
                data = self.cm.ph.getAllItemsBeetwenMarkers(data, '<input', '/>')
                if len(data) == 0: return t_s
                for item in data:
                    t_i = self.cm.ph.getSearchGroups(item, 'id=[\'"]([^"^\']+?)[\'"]')[0]
                    if t_i == 'vn':
                        temp_vn = self.cm.ph.getSearchGroups(item, 'value=[\'"]([^"^\']+?)[\'"]')[0]
                    elif t_i == 'vni':
                        temp_vni = self.cm.ph.getSearchGroups(item, 'value=[\'"]([^"^\']+?)[\'"]')[0]
                if temp_vn != '':
                    t_s = temp_vn
            return t_s
        except Exception:
            return t_s
        
    def susn(self, i_md='', i_hgk='', i_mpu=''):
        uhe = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c9IzanUL04sSdQvS8wD0ilJegUZBQD8FROZ'))
        pstd = {'md':i_md, 'hgk':i_hgk, 'mpu':i_mpu }
        try:
            if i_md != '' and i_hgk != '' and i_mpu != '':
                sts, data = self.cm.getPage(uhe, self.defaultParams, pstd)
            return
        except Exception:
            return
        
    def listSearchResult(self, cItem, searchPattern, searchType):
        try:
            printDBG("listSearchResult cItem[%s], searchPattern[%s] searchType[%s]" % (cItem, searchPattern, searchType))
            self.susn('2', '11', 'm4_kereses')
            return
        except Exception:
            return
        return
    
    def handleService(self, index, refresh = 0, searchPattern = '', searchType = ''):
        CBaseHostClass.handleService(self, index, refresh, searchPattern, searchType)
        name = self.currItem.get("name", '')
        category = self.currItem.get("category", '')
        self.currList = []
        if name == None:
            self.listMainMenu( {'name':'category'} )
        elif category == 'list_main':
            self.listMainItems(self.currItem)
        elif category == 'list_second':
            self.listSecondItems(self.currItem)
        elif category in ['search', 'search_next_page']:
            cItem = dict(self.currItem)
            cItem.update({'search_item':False, 'name':'category'}) 
            self.listSearchResult(cItem, searchPattern, searchType)
        elif category == 'search_history':
            self.listsHistory({'name':'history', 'category': 'search'}, 'desc', _("Type: "))
        else:
            printExc()
        CBaseHostClass.endHandleService(self, index, refresh)

class IPTVHost(CHostBase):

    def __init__(self):
        CHostBase.__init__(self, m4sport(), True, [])
