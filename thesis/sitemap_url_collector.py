import requests
import time
import re
from datetime import datetime, date
from tqdm import tqdm
from bs4 import BeautifulSoup

OUTPUT_FILE = "urls_sitemaps_threads3.txt"
BATCH_SIZE  = 50 
DATE_FROM   = date(2024, 1, 1)
DATE_TO     = date(2024, 12, 31)

SITEMAPS = [
    ('apnews.com'                  , 'https://apnews.com/sitemap.xml'),
    ('reuters.com'                 , 'https://www.reuters.com/sitemap.xml'),
    ('nytimes.com'                 , 'https://www.nytimes.com/sitemaps/new/sports.xml'),
    ('washingtonpost.com'          , 'https://www.washingtonpost.com/news-sitemaps/index.xml'),
    ('nbcnews.com'                 , 'https://www.nbcnews.com/sitemap.xml'),
    ('usatoday.com'                , 'https://www.usatoday.com/sitemap/news/sports/olympics/index.xml'),
    ('usatoday.com'                , 'https://www.usatoday.com/sitemap/news/sports/index.xml'),
    ('npr.org'                     , 'https://www.npr.org/sitemap.xml'),
    ('latimes.com'                 , 'https://www.latimes.com/sitemap2.xml'),
    ('newsweek.com'                , 'https://www.newsweek.com/sitemap.xml'),
    ('time.com'                    , 'https://time.com/sitemap.xml'),
    ('axios.com'                   , 'https://www.axios.com/sitemap.xml'),
    ('espn.com'                    , 'https://www.espn.com/static/news/sitemap.xml'),
    ('cbssports.com'               , 'https://www.cbssports.com/sitemap.xml'),
    ('nbcsports.com'               , 'https://www.nbcsports.com/sitemap.xml'),
    ('bleacherreport.com'          , 'https://bleacherreport.com/sitemap.xml'),
    ('sportingnews.com'            , 'https://www.sportingnews.com/us/sitemap.xml'),
    ('si.com'                      , 'https://www.si.com/sitemap.xml'),
    ('deadspin.com'                , 'https://deadspin.com/sitemap.xml'),
    ('foxnews.com'                 , 'https://www.foxnews.com/sitemap.xml'),
    ('nypost.com'                  , 'https://nypost.com/sitemap.xml'),
    ('foxsports.com'               , 'https://www.foxsports.com/sitemap.xml'),
    ('newsmax.com'                 , 'https://www.newsmax.com/sitemap.xml'),
    ('washingtonexaminer.com'      , 'https://www.washingtonexaminer.com/sitemap.xml'),
    ('breitbart.com'               , 'https://www.breitbart.com/sitemap.xml'),
    ('dailywire.com'               , 'https://www.dailywire.com/sitemap.xml'),
    ('theintercept.com'            , 'https://theintercept.com/sitemap.xml'),
    ('motherjones.com'             , 'https://www.motherjones.com/sitemap.xml'),
    ('thenation.com'               , 'https://www.thenation.com/sitemap.xml'),
    ('zerohedge.com'               , 'https://www.zerohedge.com/sitemap.xml'),
    ('thegatewaypundit.com'        , 'https://www.thegatewaypundit.com/sitemap.xml'),
    ('naturalnews.com'             , 'https://www.naturalnews.com/sitemap.xml'),
    ('bbc.com'                     , 'https://www.bbc.com/sitemap.xml'),
    ('bbc.com'                     , 'https://www.bbc.co.uk/sport/sitemap.xml'),
    ('theguardian.com'             , 'https://www.theguardian.com/sitemaps/news.xml'),
    ('independent.co.uk'           , 'https://www.independent.co.uk/sitemap.xml'),
    ('telegraph.co.uk'             , 'https://www.telegraph.co.uk/sitemap.xml'),
    ('skysports.com'               , 'https://www.skysports.com/sitemap.xml'),
    ('sky.com'                     , 'https://news.sky.com/sitemap.xml'),
    ('dailymail.co.uk'             , 'https://www.dailymail.co.uk/sitemap.xml'),
    ('thesun.co.uk'                , 'https://www.thesun.co.uk/sitemap.xml'),
    ('mirror.co.uk'                , 'https://www.mirror.co.uk/sitemap.xml'),
    ('express.co.uk'               , 'https://www.express.co.uk/sitemap.xml'),
    ('metro.co.uk'                 , 'https://metro.co.uk/sitemap.xml'),
    ('france24.com'                , 'https://www.france24.com/sitemap.xml'),
    ('lequipe.fr'                  , 'https://www.lequipe.fr/sitemap.xml'),
    ('lemonde.fr'                  , 'https://www.lemonde.fr/sitemap.xml'),
    ('lefigaro.fr'                 , 'https://www.lefigaro.fr/sitemap.xml'),
    ('liberation.fr'               , 'https://www.liberation.fr/sitemap.xml'),
    ('bfmtv.com'                   , 'https://www.bfmtv.com/sitemap.xml'),
    ('rfi.fr'                      , 'https://www.rfi.fr/sitemap.xml'),
    ('20minutes.fr'                , 'https://www.20minutes.fr/sitemap.xml'),
    ('dw.com'                      , 'https://www.dw.com/en/sitemap.xml'),
    ('spiegel.de'                  , 'https://www.spiegel.de/sitemap.xml'),
    ('bild.de'                     , 'https://www.bild.de/sitemap.xml'),
    ('sport1.de'                   , 'https://www.sport1.de/sitemap.xml'),
    ('kicker.de'                   , 'https://www.kicker.de/sitemap.xml'),
    ('welt.de'                     , 'https://www.welt.de/sitemap.xml'),
    ('marca.com'                   , 'https://www.marca.com/sitemap.xml'),
    ('as.com'                      , 'https://as.com/sitemap.xml'),
    ('mundodeportivo.com'          , 'https://www.mundodeportivo.com/sitemap.xml'),
    ('elpais.com'                  , 'https://elpais.com/sitemap.xml'),
    ('elmundo.es'                  , 'https://www.elmundo.es/sitemap.xml'),
    ('okdiario.com'                , 'https://okdiario.com/sitemap.xml'),
    ('gazzetta.it'                 , 'https://www.gazzetta.it/sitemap.xml'),
    ('corrieredellosport.it'       , 'https://www.corrieredellosport.it/sitemap.xml'),
    ('corriere.it'                 , 'https://www.corriere.it/sitemap.xml'),
    ('repubblica.it'               , 'https://www.repubblica.it/sitemap.xml'),
    ('ansa.it'                     , 'https://www.ansa.it/sitemap.xml'),
    ('record.pt'                   , 'https://www.record.pt/sitemap.xml'),
    ('globo.com'                   , 'https://www.globo.com/sitemap.xml'),
    ('uol.com.br'                  , 'https://www.uol.com.br/sitemap.xml'),
    ('folha.uol.com.br'            , 'https://www.folha.uol.com.br/sitemap.xml'),
    ('estadao.com.br'              , 'https://www.estadao.com.br/sitemap.xml'),
    ('rt.com'                      , 'https://www.rt.com/sitemap.xml'),
    ('sputniknews.com'             , 'https://sputniknews.com/sitemap.xml'),
    ('tass.com'                    , 'https://tass.com/sitemap.xml'),
    ('kyivpost.com'                , 'https://www.kyivpost.com/sitemap.xml'),
    ('euractiv.com'                , 'https://www.euractiv.com/sitemap.xml'),
    ('xinhuanet.com'               , 'https://www.xinhuanet.com/sitemap.xml'),
    ('chinadaily.com.cn'           , 'https://www.chinadaily.com.cn/sitemap.xml'),
    ('cgtn.com'                    , 'https://www.cgtn.com/sitemap.xml'),
    ('globaltimes.cn'              , 'https://www.globaltimes.cn/sitemap.xml'),
    ('scmp.com'                    , 'https://www.scmp.com/sitemap.xml'),
    ('straitstimes.com'            , 'https://www.straitstimes.com/sitemap.xml'),
    ('japantimes.co.jp'            , 'https://www.japantimes.co.jp/sitemap.xml'),
    ('koreatimes.co.kr'            , 'https://www.koreatimes.co.kr/sitemap.xml'),
    ('bangkokpost.com'             , 'https://www.bangkokpost.com/sitemap.xml'),
    ('channelnewsasia.com'         , 'https://www.channelnewsasia.com/sitemap.xml'),
    ('aljazeera.com'               , 'https://www.aljazeera.com/sitemap.xml'),
    ('alarabiya.net'               , 'https://www.alarabiya.net/sitemap.xml'),
    ('thenationalnews.com'         , 'https://www.thenationalnews.com/sitemap.xml'),
    ('timesofisrael.com'           , 'https://www.timesofisrael.com/sitemap.xml'),
    ('haaretz.com'                 , 'https://www.haaretz.com/sitemap.xml'),
    ('dailysabah.com'              , 'https://www.dailysabah.com/sitemap.xml'),
    ('middleeasteye.net'           , 'https://www.middleeasteye.net/sitemap.xml'),
    ('punchng.com'                 , 'https://punchng.com/sitemap.xml'),
    ('premiumtimesng.com'          , 'https://www.premiumtimesng.com/sitemap.xml'),
    ('dailymaverick.co.za'         , 'https://www.dailymaverick.co.za/sitemap.xml'),
    ('news24.com'                  , 'https://www.news24.com/sitemap.xml'),
    ('theafricareport.com'         , 'https://www.theafricareport.com/sitemap.xml'),
    ('africanews.com'              , 'https://www.africanews.com/sitemap.xml'),
    ('timesofindia.com'            , 'https://timesofindia.indiatimes.com/sitemap.xml'),
    ('thehindu.com'                , 'https://www.thehindu.com/sitemap.xml'),
    ('hindustantimes.com'          , 'https://www.hindustantimes.com/sitemap.xml'),
    ('ndtv.com'                    , 'https://www.ndtv.com/sitemap.xml'),
    ('sportskeeda.com'             , 'https://www.sportskeeda.com/sitemap.xml'),
    ('scroll.in'                   , 'https://scroll.in/sitemap.xml'),
    ('dawn.com'                    , 'https://www.dawn.com/sitemap.xml'),
    ('geo.tv'                      , 'https://www.geo.tv/sitemap.xml'),
    ('abc.net.au'                  , 'https://www.abc.net.au/sitemap.xml'),
    ('smh.com.au'                  , 'https://www.smh.com.au/sitemap.xml'),
    ('news.com.au'                 , 'https://www.news.com.au/sitemap.xml'),
    ('skynews.com.au'              , 'https://www.skynews.com.au/sitemap.xml'),
    ('nzherald.co.nz'              , 'https://www.nzherald.co.nz/sitemap.xml'),
    ('stuff.co.nz'                 , 'https://www.stuff.co.nz/sitemap.xml'),
    ('cbc.ca'                      , 'https://www.cbc.ca/sitemap.xml'),
    ('theglobeandmail.com'         , 'https://www.theglobeandmail.com/sitemap.xml'),
    ('nationalpost.com'            , 'https://nationalpost.com/sitemap.xml'),
    ('infobae.com'                 , 'https://www.infobae.com/sitemap.xml'),
    ('clarin.com'                  , 'https://www.clarin.com/sitemap.xml'),
    ('eluniversal.com.mx'          , 'https://www.eluniversal.com.mx/sitemap.xml'),
    ('telesurtv.net'               , 'https://www.telesurtv.net/sitemap.xml'),
    ('emol.com'                    , 'https://www.emol.com/sitemap.xml'),
    ('aftenposten.no'              , 'https://www.aftenposten.no/sitemap.xml'),
    ('aftonbladet.se'              , 'https://www.aftonbladet.se/sitemap.xml'),
    ('svt.se'                      , 'https://www.svt.se/sitemap.xml'),
    ('yle.fi'                      , 'https://yle.fi/sitemap.xml'),
    ('olympics.com'                , 'https://www.olympics.com/en/sitemap.xml'),
    ('eurosport.com'               , 'https://www.eurosport.com/sitemap.xml'),
    ('euronews.com'                , 'https://www.euronews.com/sitemap.xml'),
    ('insidethegames.biz'          , 'https://www.insidethegames.biz/sitemap.xml'),
    ('aroundtherings.com'          , 'https://aroundtherings.com/sitemap.xml'),
    ('cbsnews.com'                 , 'https://www.cbsnews.com/sitemap.xml'),
    ('abcnews.go.com'              , 'https://abcnews.go.com/sitemap.xml'),
    ('msnbc.com'                   , 'https://www.msnbc.com/sitemap.xml'),
    ('theatlantic.com'             , 'https://www.theatlantic.com/sitemap.xml'),
    ('politico.com'                , 'https://www.politico.com/sitemap.xml'),
    ('huffpost.com'                , 'https://www.huffpost.com/sitemap.xml'),
    ('vox.com'                     , 'https://www.vox.com/sitemap.xml'),
    ('thehill.com'                 , 'https://thehill.com/sitemap.xml'),
    ('businessinsider.com'         , 'https://www.businessinsider.com/sitemap.xml'),
    ('rollingstone.com'            , 'https://www.rollingstone.com/sitemap.xml'),
    ('slate.com'                   , 'https://slate.com/sitemap.xml'),
    ('salon.com'                   , 'https://www.salon.com/sitemap.xml'),
    ('wired.com'                   , 'https://www.wired.com/sitemap.xml'),
    ('theathletic.com'             , 'https://theathletic.com/sitemap.xml'),
    ('yardbarker.com'              , 'https://www.yardbarker.com/sitemap.xml'),
    ('fansided.com'                , 'https://fansided.com/sitemap.xml'),
    ('sportscasting.com'           , 'https://www.sportscasting.com/sitemap.xml'),
    ('outsideonline.com'           , 'https://www.outsideonline.com/sitemap.xml'),
    ('thefederalist.com'           , 'https://thefederalist.com/sitemap.xml'),
    ('nationalreview.com'          , 'https://www.nationalreview.com/sitemap.xml'),
    ('townhall.com'                , 'https://townhall.com/sitemap.xml'),
    ('redstate.com'                , 'https://redstate.com/sitemap.xml'),
    ('pjmedia.com'                 , 'https://pjmedia.com/sitemap.xml'),
    ('americanthinker.com'         , 'https://www.americanthinker.com/sitemap.xml'),
    ('thenewamerican.com'          , 'https://thenewamerican.com/sitemap.xml'),
    ('oann.com'                    , 'https://www.oann.com/sitemap.xml'),
    ('jacobin.com'                 , 'https://jacobin.com/sitemap.xml'),
    ('commondreams.org'            , 'https://www.commondreams.org/sitemap.xml'),
    ('truthout.org'                , 'https://truthout.org/sitemap.xml'),
    ('inthesetimes.com'            , 'https://inthesetimes.com/sitemap.xml'),
    ('democracynow.org'            , 'https://www.democracynow.org/sitemap.xml'),
    ('infowars.com'                , 'https://www.infowars.com/sitemap.xml'),
    ('wnd.com'                     , 'https://www.wnd.com/sitemap.xml'),
    ('westernjournal.com'          , 'https://www.westernjournal.com/sitemap.xml'),
    ('patriotpost.us'              , 'https://patriotpost.us/sitemap.xml'),
    ('activistpost.com'            , 'https://www.activistpost.com/sitemap.xml'),
    ('beforeitsnews.com'           , 'https://beforeitsnews.com/sitemap.xml'),
    ('globalresearch.ca'           , 'https://www.globalresearch.ca/sitemap.xml'),
    ('thetimes.co.uk'              , 'https://www.thetimes.co.uk/sitemap.xml'),
    ('eveningstandard.co.uk'       , 'https://www.standard.co.uk/sitemap.xml'),
    ('spectator.co.uk'             , 'https://www.spectator.co.uk/sitemap.xml'),
    ('newstatesman.com'            , 'https://www.newstatesman.com/sitemap.xml'),
    ('morningstaronline.co.uk'     , 'https://morningstaronline.co.uk/sitemap.xml'),
    ('inews.co.uk'                 , 'https://inews.co.uk/sitemap.xml'),
    ('cityam.com'                  , 'https://www.cityam.com/sitemap.xml'),
    ('sportbible.com'              , 'https://www.sportbible.com/sitemap.xml'),
    ('talksport.com'               , 'https://talksport.com/sitemap.xml'),
    ('joe.co.uk'                   , 'https://www.joe.co.uk/sitemap.xml'),
    ('irishtimes.com'              , 'https://www.irishtimes.com/sitemap.xml'),
    ('independent.ie'              , 'https://www.independent.ie/sitemap.xml'),
    ('rte.ie'                      , 'https://www.rte.ie/sitemap.xml'),
    ('thejournal.ie'               , 'https://www.thejournal.ie/sitemap.xml'),
    ('torontostar.com'             , 'https://www.thestar.com/sitemap.xml'),
    ('ottawacitizen.com'           , 'https://ottawacitizen.com/sitemap.xml'),
    ('montrealgazette.com'         , 'https://montrealgazette.com/sitemap.xml'),
    ('thepostmillennial.com'       , 'https://thepostmillennial.com/sitemap.xml'),
    ('rebelnews.com'               , 'https://www.rebelnews.com/sitemap.xml'),
    ('theage.com.au'               , 'https://www.theage.com.au/sitemap.xml'),
    ('theaustralian.com.au'        , 'https://www.theaustralian.com.au/sitemap.xml'),
    ('heraldsun.com.au'            , 'https://www.heraldsun.com.au/sitemap.xml'),
    ('dailytelegraph.com.au'       , 'https://www.dailytelegraph.com.au/sitemap.xml'),
    ('sbs.com.au'                  , 'https://www.sbs.com.au/sitemap.xml'),
    ('perthnow.com.au'             , 'https://www.perthnow.com.au/sitemap.xml'),
    ('couriermail.com.au'          , 'https://www.couriermail.com.au/sitemap.xml'),
    ('adelaidenow.com.au'          , 'https://www.adelaidenow.com.au/sitemap.xml'),
    ('rnz.co.nz'                   , 'https://www.rnz.co.nz/sitemap.xml'),
    ('1news.co.nz'                 , 'https://www.1news.co.nz/sitemap.xml'),
    ('newshub.co.nz'               , 'https://www.newshub.co.nz/sitemap.xml'),
    ('timeslive.co.za'             , 'https://www.timeslive.co.za/sitemap.xml'),
    ('thesouthafrican.com'         , 'https://www.thesouthafrican.com/sitemap.xml'),
    ('iol.co.za'                   , 'https://www.iol.co.za/sitemap.xml'),
    ('businesslive.co.za'          , 'https://www.businesslive.co.za/sitemap.xml'),
    ('citizen.co.za'               , 'https://www.citizen.co.za/sitemap.xml'),
    ('vanguardngr.com'             , 'https://www.vanguardngr.com/sitemap.xml'),
    ('thecable.ng'                 , 'https://www.thecable.ng/sitemap.xml'),
    ('channelstv.com'              , 'https://www.channelstv.com/sitemap.xml'),
    ('tribuneonlineng.com'         , 'https://tribuneonlineng.com/sitemap.xml'),
    ('myjoyonline.com'             , 'https://www.myjoyonline.com/sitemap.xml'),
    ('graphic.com.gh'              , 'https://www.graphic.com.gh/sitemap.xml'),
    ('ghanaweb.com'                , 'https://www.ghanaweb.com/sitemap.xml'),
    ('nation.africa'               , 'https://nation.africa/sitemap.xml'),
    ('standardmedia.co.ke'         , 'https://www.standardmedia.co.ke/sitemap.xml'),
    ('monitor.co.ug'               , 'https://www.monitor.co.ug/sitemap.xml'),
    ('thecitizen.co.tz'            , 'https://www.thecitizen.co.tz/sitemap.xml'),
    ('theeastafrican.co.ke'        , 'https://www.theeastafrican.co.ke/sitemap.xml'),
    ('egyptindependent.com'        , 'https://www.egyptindependent.com/sitemap.xml'),
    ('egypttoday.com'              , 'https://www.egypttoday.com/sitemap.xml'),
    ('madamasr.com'                , 'https://www.madamasr.com/en/sitemap.xml'),
    ('arabnews.com'                , 'https://www.arabnews.com/sitemap.xml'),
    ('jordantimes.com'             , 'https://www.jordantimes.com/sitemap.xml'),
    ('gulfnews.com'                , 'https://gulfnews.com/sitemap.xml'),
    ('khaleejtimes.com'            , 'https://www.khaleejtimes.com/sitemap.xml'),
    ('presstv.ir'                  , 'https://www.presstv.ir/sitemap.xml'),
    ('tehrantimes.com'             , 'https://www.tehrantimes.com/sitemap.xml'),
    ('al-monitor.com'              , 'https://www.al-monitor.com/sitemap.xml'),
    ('jpost.com'                   , 'https://www.jpost.com/sitemap.xml'),
    ('hurriyetdailynews.com'       , 'https://www.hurriyetdailynews.com/sitemap.xml'),
    ('thewire.in'                  , 'https://thewire.in/sitemap.xml'),
    ('opindia.com'                 , 'https://www.opindia.com/sitemap.xml'),
    ('republic.world'              , 'https://www.republic.world/sitemap.xml'),
    ('firstpost.com'               , 'https://www.firstpost.com/sitemap.xml'),
    ('theprint.in'                 , 'https://theprint.in/sitemap.xml'),
    ('livemint.com'                , 'https://www.livemint.com/sitemap.xml'),
    ('indianexpress.com'           , 'https://indianexpress.com/sitemap.xml'),
    ('deccanherald.com'            , 'https://www.deccanherald.com/sitemap.xml'),
    ('tribuneindia.com'            , 'https://www.tribuneindia.com/sitemap.xml'),
    ('sportstar.thehindu.com'      , 'https://sportstar.thehindu.com/sitemap.xml'),
    ('thenews.com.pk'              , 'https://www.thenews.com.pk/sitemap.xml'),
    ('arynews.tv'                  , 'https://arynews.tv/sitemap.xml'),
    ('thedailystar.net'            , 'https://www.thedailystar.net/sitemap.xml'),
    ('dailymirror.lk'              , 'https://www.dailymirror.lk/sitemap.xml'),
    ('newsfirst.lk'                , 'https://newsfirst.lk/sitemap.xml'),
    ('myrepublica.com'             , 'https://myrepublica.nagariknetwork.com/sitemap.xml'),
    ('thestar.com.my'              , 'https://www.thestar.com.my/sitemap.xml'),
    ('nst.com.my'                  , 'https://www.nst.com.my/sitemap.xml'),
    ('nationthailand.com'          , 'https://www.nationthailand.com/sitemap.xml'),
    ('phnompenhpost.com'           , 'https://www.phnompenhpost.com/sitemap.xml'),
    ('myanmartimes.com.mm'         , 'https://www.myanmartimes.com.mm/sitemap.xml'),
    ('philstar.com'                , 'https://www.philstar.com/sitemap.xml'),
    ('inquirer.net'                , 'https://www.inquirer.net/sitemap.xml'),
    ('jakartapost.com'             , 'https://www.thejakartapost.com/sitemap.xml'),
    ('vietnamnews.vn'              , 'https://vietnamnews.vn/sitemap.xml'),
    ('tuoitrenews.vn'              , 'https://tuoitrenews.vn/sitemap.xml'),
    ('saigontimes.vn'              , 'https://english.thesaigontimes.vn/sitemap.xml'),
    ('shine.cn'                    , 'https://www.shine.cn/sitemap.xml'),
    ('sixthtone.com'               , 'https://www.sixthtone.com/sitemap.xml'),
    ('asahi.com'                   , 'https://www.asahi.com/ajw/sitemap.xml'),
    ('mainichi.jp'                 , 'https://mainichi.jp/english/sitemap.xml'),
    ('nhk.or.jp'                   , 'https://www3.nhk.or.jp/nhkworld/sitemap.xml'),
    ('japantoday.com'              , 'https://japantoday.com/sitemap.xml'),
    ('koreaherald.com'             , 'https://www.koreaherald.com/sitemap.xml'),
    ('arirang.com'                 , 'https://www.arirang.com/sitemap.xml'),
    ('themoscowtimes.com'          , 'https://www.themoscowtimes.com/sitemap.xml'),
    ('kyivindependent.com'         , 'https://kyivindependent.com/sitemap.xml'),
    ('ukrinform.net'               , 'https://www.ukrinform.net/sitemap.xml'),
    ('ukraineworld.org'            , 'https://ukraineworld.org/sitemap.xml'),
    ('emerging-europe.com'         , 'https://emerging-europe.com/sitemap.xml'),
    ('balkaninsight.com'           , 'https://balkaninsight.com/sitemap.xml'),
    ('novinite.com'                , 'https://www.novinite.com/sitemap.xml'),
    ('jamaicaobserver.com'         , 'https://www.jamaicaobserver.com/sitemap.xml'),
    ('jamaicagleaner.com'          , 'https://jamaica-gleaner.com/sitemap.xml'),
    ('trinidadexpress.com'         , 'https://trinidadexpress.com/sitemap.xml'),
    ('loopnews.com'                , 'https://www.loopnews.com/sitemap.xml'),
    ('pireport.org'                , 'https://www.pireport.org/sitemap.xml'),
    ('worldathletics.org'          , 'https://www.worldathletics.org/sitemap.xml'),
    ('olympic.org'                 , 'https://www.olympic.org/sitemap.xml'),
    ('swimswam.com'                , 'https://swimswam.com/sitemap.xml'),
    ('gymnastics.sport'            , 'https://www.gymnastics.sport/sitemap.xml'),
    ('flotrack.org'                , 'https://www.flotrack.org/sitemap.xml'),
    ('velonews.com'                , 'https://www.velonews.com/sitemap.xml'),
    ('teamusa.org'                 , 'https://www.teamusa.org/sitemap.xml'),
    ('britishathletics.org.uk'     , 'https://www.britishathletics.org.uk/sitemap.xml'),
    ('mintpressnews.com'           , 'https://www.mintpressnews.com/sitemap.xml'),
    ('off-guardian.org'            , 'https://off-guardian.org/sitemap.xml'),
    ('21stcenturywire.com'         , 'https://21stcenturywire.com/sitemap.xml'),
    ('theduran.com'                , 'https://theduran.com/sitemap.xml'),
    ('grayzone.com'                , 'https://thegrayzone.com/sitemap.xml'),
    ('lewrockwell.com'             , 'https://www.lewrockwell.com/sitemap.xml'),
    ('veteranstoday.com'           , 'https://www.veteranstoday.com/sitemap.xml'),
    ('russiatoday.com'             , 'https://www.rt.com/rss/news/sitemap.xml'),
    ('ria.ru'                      , 'https://ria.ru/export/sitemap.xml'),
    ('pravda.ru'                   , 'https://www.pravda.ru/sitemap.xml'),
    ('rbth.com'                    , 'https://www.rbth.com/sitemap.xml'),
    ('russiainsider.com'           , 'https://russia-insider.com/sitemap.xml'),
    ('southfront.org'              , 'https://southfront.org/sitemap.xml'),
    ('strategic-culture.org'       , 'https://strategic-culture.org/sitemap.xml'),
    ('orientalreview.org'          , 'https://orientalreview.org/sitemap.xml'),
    ('neweasternoutlook.org'       , 'https://journal-neo.su/sitemap.xml'),
    ('stalkerzone.org'             , 'https://stalkerzone.org/sitemap.xml'),
    ('russophile.org'              , 'https://russophile.org/sitemap.xml'),
    ('thesaker.is'                 , 'https://thesaker.is/sitemap.xml'),
    ('inforos.ru'                  , 'https://inforos.ru/en/sitemap.xml'),
    ('rbc.ru'                      , 'https://www.rbc.ru/sitemap.xml'),
    ('sport-express.ru'            , 'https://www.sport-express.ru/sitemap_en.xml'),
    ('championat.com'              , 'https://www.championat.com/sitemap.xml'),
    ('rsport.ria.ru'               , 'https://rsport.ria.ru/sitemap.xml'),
    ('moonofalabama.org'           , 'https://www.moonofalabama.org/sitemap.xml'),
    ('consortiumnews.com'          , 'https://consortiumnews.com/sitemap.xml'),
    ('antiwar.com'                 , 'https://www.antiwar.com/sitemap.xml'),
    ('unz.com'                     , 'https://www.unz.com/sitemap.xml'),
    ('greanvillepost.com'          , 'https://www.greanvillepost.com/sitemap.xml'),
    ('covertactionmagazine.com'    , 'https://covertactionmagazine.com/sitemap.xml'),
    ('popularresistance.org'       , 'https://popularresistance.org/sitemap.xml'),
    ('pbs.org'                     , 'https://www.pbs.org/sitemap.xml'),
    ('sports.yahoo.com'            , 'https://sports.yahoo.com/sitemap.xml'),
    ('msn.com'                     , 'https://www.msn.com/sitemap.xml'),
    ('vice.com'                    , 'https://www.vice.com/sitemap.xml'),
    ('buzzfeednews.com'            , 'https://www.buzzfeednews.com/sitemap.xml'),
    ('thedailybeast.com'           , 'https://www.thedailybeast.com/sitemap.xml'),
    ('mediaite.com'                , 'https://www.mediaite.com/sitemap.xml'),
    ('reason.com'                  , 'https://reason.com/sitemap.xml'),
    ('spectator.org'               , 'https://spectator.org/sitemap.xml'),
    ('chronicleofphilanthropy.com' , 'https://www.philanthropy.com/sitemap.xml'),
    ('outsports.com'               , 'https://www.outsports.com/sitemap.xml'),
    ('gbchannel.com'               , 'https://www.gbnews.com/sitemap.xml'),
    ('dailyrecord.co.uk'           , 'https://www.dailyrecord.co.uk/sitemap.xml'),
    ('heraldscotland.com'          , 'https://www.heraldscotland.com/sitemap.xml'),
    ('walesonline.co.uk'           , 'https://www.walesonline.co.uk/sitemap.xml'),
    ('belfasttelegraph.co.uk'      , 'https://www.belfasttelegraph.co.uk/sitemap.xml'),
    ('irishexaminer.com'           , 'https://www.irishexaminer.com/sitemap.xml'),
    ('intellinews.com'             , 'https://www.intellinews.com/sitemap.xml'),
    ('euobserver.com'              , 'https://euobserver.com/sitemap.xml'),
    ('cepa.org'                    , 'https://cepa.org/sitemap.xml'),
    ('stopfake.org'                , 'https://www.stopfake.org/en/sitemap.xml'),
    ('meduza.io'                   , 'https://meduza.io/sitemap.xml'),
    ('theins.ru'                   , 'https://theins.ru/en/sitemap.xml'),
    ('novayagazeta.eu'             , 'https://novayagazeta.eu/sitemap.xml'),
    ('mbk-news.appspot.com'        , 'https://mbk-news.appspot.com/sitemap.xml'),
    ('dossier.center'              , 'https://dossier.center/sitemap.xml'),
    ('republic.ru'                 , 'https://republic.ru/sitemap.xml'),
    ('rferl.org'                   , 'https://www.rferl.org/sitemap.xml'),
    ('poloniatoday.com'            , 'https://poloniatoday.com/sitemap.xml'),
    ('thenews.pl'                  , 'https://www.thenews.pl/sitemap.xml'),
    ('romaniainsiider.com'         , 'https://www.romania-insider.com/sitemap.xml'),
    ('seenews.com'                 , 'https://seenews.com/sitemap.xml'),
    ('total-croatia-news.com'      , 'https://www.total-croatia-news.com/sitemap.xml'),
    ('prague-post.com'             , 'https://www.praguepost.com/sitemap.xml'),
    ('budapesttimes.hu'            , 'https://budapesttimes.hu/sitemap.xml'),
    ('lithuaniatribune.com'        , 'https://lithuaniatribune.com/sitemap.xml'),
    ('lrt.lt'                      , 'https://www.lrt.lt/en/sitemap.xml'),
    ('err.ee'                      , 'https://news.err.ee/sitemap.xml'),
    ('lsm.lv'                      , 'https://eng.lsm.lv/sitemap.xml'),
    ('mercopress.com'              , 'https://en.mercopress.com/sitemap.xml'),
    ('riotimesonline.com'          , 'https://riotimesonline.com/sitemap.xml'),
    ('brasilwire.com'              , 'https://www.brasilwire.com/sitemap.xml'),
    ('perunews.com'                , 'https://perunews.com/sitemap.xml'),
    ('colombiareports.com'         , 'https://colombiareports.com/sitemap.xml'),
    ('venezuelaanalysis.com'       , 'https://venezuelaanalysis.com/sitemap.xml'),
    ('laht.com'                    , 'https://www.laht.com/sitemap.xml'),
    ('ticotimes.net'               , 'https://ticotimes.net/sitemap.xml'),
    ('belize.com'                  , 'https://www.belizetimes.bz/sitemap.xml'),
    ('allafrica.com'               , 'https://allafrica.com/sitemap.xml'),
    ('africanarguments.org'        , 'https://africanarguments.org/sitemap.xml'),
    ('theafricapodcast.com'        , 'https://www.africanews.com/sport/sitemap.xml'),
    ('ethiopia-insight.com'        , 'https://ethiopia-insight.com/sitemap.xml'),
    ('addisstandard.com'           , 'https://addisstandard.com/sitemap.xml'),
    ('sudantribune.com'            , 'https://sudantribune.com/sitemap.xml'),
    ('mozambiqueminingpost.com'    , 'https://www.mozambiqueminingpost.com/sitemap.xml'),
    ('zimbabwesituation.com'       , 'https://www.zimbabwesituation.com/sitemap.xml'),
    ('newzimbabwe.com'             , 'https://www.newzimbabwe.com/sitemap.xml'),
    ('lusakatimes.com'             , 'https://www.lusakatimes.com/sitemap.xml'),
    ('zambiadailynail.com'         , 'https://www.daily-mail.co.zm/sitemap.xml'),
    ('mwebantu.com'                , 'https://www.mwebantu.com/sitemap.xml'),
    ('dailypost.ng'                , 'https://dailypost.ng/sitemap.xml'),
    ('sunnewsonline.com'           , 'https://www.sunnewsonline.com/sitemap.xml'),
    ('guardian.ng'                 , 'https://guardian.ng/sitemap.xml'),
    ('asiancorrespondent.com'      , 'https://asiancorrespondent.com/sitemap.xml'),
    ('asiatimes.com'               , 'https://asiatimes.com/sitemap.xml'),
    ('thediplomat.com'             , 'https://thediplomat.com/sitemap.xml'),
    ('todayonline.com'             , 'https://www.todayonline.com/sitemap.xml'),
    ('businesstimes.com.sg'        , 'https://www.businesstimes.com.sg/sitemap.xml'),
    ('freemalaysiatoday.com'       , 'https://www.freemalaysiatoday.com/sitemap.xml'),
    ('malaymail.com'               , 'https://www.malaymail.com/sitemap.xml'),
    ('rappler.com'                 , 'https://www.rappler.com/sitemap.xml'),
    ('abs-cbn.com'                 , 'https://news.abs-cbn.com/sitemap.xml'),
    ('gnlm.com.mm'                 , 'https://www.gnlm.com.mm/sitemap.xml'),
    ('khmertimeskh.com'            , 'https://www.khmertimeskh.com/sitemap.xml'),
    ('vientianetimes.org.la'       , 'https://www.vientianetimes.org.la/sitemap.xml'),
    ('ips.org'                     , 'https://www.ipsnews.net/sitemap.xml'),
    ('eurasianet.org'              , 'https://eurasianet.org/sitemap.xml'),
    ('cabar.asia'                  , 'https://cabar.asia/en/sitemap.xml'),
    ('fergana.agency'              , 'https://fergana.agency/en/sitemap.xml'),
    ('akipress.com'                , 'https://akipress.com/sitemap.xml'),
    ('azernews.az'                 , 'https://www.azernews.az/sitemap.xml'),
    ('agenda.ge'                   , 'https://agenda.ge/sitemap.xml'),
    ('civil.ge'                    , 'https://civil.ge/sitemap.xml'),
    ('armenpress.am'               , 'https://armenpress.am/en/sitemap.xml'),
    ('kaztag.kz'                   , 'https://kaztag.kz/en/sitemap.xml'),
    ('ipsnews.net'                 , 'https://www.ipsnews.net/sitemap.xml'),
    ('afp.com'                     , 'https://www.afp.com/en/sitemap.xml'),
    ('snopes.com'                  , 'https://www.snopes.com/sitemap.xml'),
    ('politifact.com'              , 'https://www.politifact.com/sitemap.xml'),
    ('factcheck.org'               , 'https://www.factcheck.org/sitemap.xml'),
    ('fullfact.org'                , 'https://fullfact.org/sitemap.xml'),
    ('bellingcat.com'              , 'https://www.bellingcat.com/sitemap.xml'),
    ('occrp.org'                   , 'https://www.occrp.org/en/sitemap.xml'),
    ('worldrowing.com'             , 'https://worldrowing.com/sitemap.xml'),
    ('worldarchery.sport'          , 'https://www.worldarchery.sport/sitemap.xml'),
    ('ijf.org'                     , 'https://www.ijf.org/sitemap.xml'),
    ('fivb.com'                    , 'https://www.fivb.com/sitemap.xml'),
    ('worldboxing.sport'           , 'https://www.worldboxing.sport/sitemap.xml'),
    ('letsrun.com'                 , 'https://www.letsrun.com/sitemap.xml'),
    ('swimworld.com'               , 'https://www.swimmingworldmagazine.com/sitemap.xml'),
    ('weightliftinghouse.com'      , 'https://www.iwf.net/sitemap.xml'),
    ('inside.fei.org'              , 'https://inside.fei.org/sitemap.xml'),
    ('badmintonworld.tv'           , 'https://bwfbadminton.com/sitemap.xml'),
    ('usatf.org'                   , 'https://www.usatf.org/sitemap.xml'),
    ('trackandfieldnews.com'       , 'https://www.trackandfieldnews.com/sitemap.xml'),
    ('cyclingnews.com'             , 'https://www.cyclingnews.com/sitemap.xml'),
    ('procyclingstats.com'         , 'https://www.procyclingstats.com/sitemap.xml'),
    ('gymnasticsnow.com'           , 'https://www.gymnasticsnow.com/sitemap.xml'),
    ('sportinglife.com'            , 'https://www.sportinglife.com/sitemap.xml'),
]

_URL_DATE_RE = re.compile(
    r"[/_-](?P<y>20\d{2})[/_-](?P<m>0[1-9]|1[0-2])(?:[/_-](?P<d>0[1-9]|[12]\d|3[01]))?"
)

def _parse_date(value):
    if not value:
        return None
    value = value.strip()[:25]
    for fmt in ("%Y%m%d%H%M%S", "%Y%m%d", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value[:len(fmt)], fmt).date()
        except ValueError:
            continue
    return None

def _date_from_url(url):
    m = _URL_DATE_RE.search(url)
    if not m:
        return None
    try:
        return date(int(m.group("y")), int(m.group("m")),
                    int(m.group("d")) if m.group("d") else 1)
    except (ValueError, TypeError):
        return None

def in_date_range(dt):
    if dt is None:
        return True
    return DATE_FROM <= dt <= DATE_TO

# Olympics terms
_OLYMPIC_TERMS = [
    "olympic", "olympics", "olymp", "paris 2024", "paris2024",
    "jeux olympiques", "juegos olimpicos", "olimpiadi",
    "2024 games", "summer games", "jo 2024", "jo-2024",
]

# Reject terms
_TITLE_BLOCKLIST = [
    "euro 2024", "champions league", "world cup", "formula 1", "f1",
    "tour de france", "nfl", "nba", "nhl", "mlb",
]

# URL terms
_URL_GROUP_A = [
    "olympic", "olympics", "olymp", "jeux-olympiques",
    "juegos-olimpicos", "olimpiadi", "olympische",
    "gymnastics", "triathlon", "decathlon", "velodrome", "aquatics",
]
_URL_GROUP_B = ["paris", "paris-2024", "paris2024", "2024", "summer-2024"]
_URL_BLOCKLIST = [
    "election", "vote", "ballot", "trump", "biden", "harris",
    "ukraine", "russia", "gaza", "israel", "climate", "hurricane",
    "earthquake", "shooting", "murder", "crime", "police",
    "nfl", "nba", "nhl", "mlb", "euro-2024", "champions-league",
    "world-cup", "formula-1", "tour-de-france", "super-bowl",
]

# check title
def _title_is_olympic(url_tag) -> bool:
    for tag_name in ("news:title", "title", "news:keywords"):
        tag = url_tag.find(tag_name)
        if tag and tag.text.strip():
            text = tag.text.strip().lower()
            has_olympic   = any(t in text for t in _OLYMPIC_TERMS)
            has_blocklist = any(b in text for b in _TITLE_BLOCKLIST)
            return has_olympic and not has_blocklist
    return None  

# check url
def _url_is_olympic(url: str) -> bool:
    u = url.lower()
    if any(bad in u for bad in _URL_BLOCKLIST):
        return False
    if any(s in u for s in ["paris-2024-olympic", "olympic-games-2024",
                             "olympics-2024", "paris-olympics",
                             "summer-olympics-2024"]):
        return True
    return any(a in u for a in _URL_GROUP_A) and any(b in u for b in _URL_GROUP_B)


import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

WORKERS = 30 

HEADERS   = {"User-Agent": "Mozilla/5.0 (compatible; OlympicsResearchBot/1.0)"}
SESSION   = requests.Session() 

_lock        = threading.Lock() 
seen_urls    = set()
rejected     = {"date": 0, "relevance": 0}

def _write_url(url):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def add_url(url):
    url = url.split("?")[0].split("#")[0].rstrip("/")
    if not url or not url.startswith("http"):
        return False
    with _lock:
        if url in seen_urls:
            return False
        seen_urls.add(url)
        n = len(seen_urls)
    _write_url(url)
    if n % BATCH_SIZE == 0:
        print(f" {n:,} URLs saved so far", flush=True)
    return True

def _inc_rejected(key):
    with _lock:
        rejected[key] += 1


_SKIP_CHILD = ["video", "image", "photo", "podcast", "author",
               "tag", "category", "page", "misc", "static", "amp"]

def _fetch(url):
    try:
        r = SESSION.get(url, headers=HEADERS, timeout=15)
        return r if r.status_code == 200 else None
    except Exception:
        return None

def _collect_child_urls(sitemap_url, depth=0):
    if depth > 4:
        return [], []

    r = _fetch(sitemap_url)
    if r is None:
        return [], []

    try:
        soup = BeautifulSoup(r.text, "lxml-xml")
    except Exception:
        return [], []

    children_found = soup.find_all("sitemap")
    if children_found:
        child_urls = []
        for sm in children_found:
            loc = sm.find("loc")
            if not loc:
                continue
            child_url = loc.text.strip()
            child_dt = _date_from_url(child_url)
            if child_dt and not in_date_range(child_dt):
                continue
            cl = child_url.lower()
            if any(p in cl for p in _SKIP_CHILD):
                continue
            child_urls.append(child_url)
        return [], child_urls

    article_urls = []
    date_skip    = 0
    rel_skip     = 0

    for url_tag in soup.find_all("url"):
        loc = url_tag.find("loc")
        if not loc:
            continue
        raw_url = loc.text.strip()
        if not raw_url.startswith("http"):
            continue

        lastmod = url_tag.find("lastmod")
        lastmod_str = lastmod.text.strip() if lastmod else ""
        dt = _parse_date(lastmod_str) or _date_from_url(raw_url)
        if not in_date_range(dt):
            date_skip += 1
            continue

        title_result = _title_is_olympic(url_tag)
        if title_result is True:
            article_urls.append(raw_url)
        elif title_result is False:
            rel_skip += 1
        else:
            if _url_is_olympic(raw_url):
                article_urls.append(raw_url)
            else:
                rel_skip += 1

    with _lock:
        rejected["date"]      += date_skip
        rejected["relevance"] += rel_skip

    return article_urls, []

def process_domain(domain, root_sitemap_url):
    added = 0
  
    queue = [(root_sitemap_url, 0)]
    visited_sitemaps = set()

    with ThreadPoolExecutor(max_workers=5) as inner:
        while queue:
            futures = {}
            for url, depth in queue:
                if url not in visited_sitemaps:
                    visited_sitemaps.add(url)
                    futures[inner.submit(_collect_child_urls, url, depth)] = depth

            queue = []
            for fut in as_completed(futures):
                depth = futures[fut]
                try:
                    articles, children = fut.result()
                    for url in articles:
                        if add_url(url):
                            added += 1
                    for child_url in children:
                        queue.append((child_url, depth + 1))
                except Exception:
                    pass

    return added


if __name__ == "__main__":

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("")

    pbar = tqdm(total=len(SITEMAPS), desc="Domains", unit="site")

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(process_domain, domain, url): domain
            for domain, url in SITEMAPS
        }
        for fut in as_completed(futures):
            domain = futures[fut]
            try:
                added = fut.result()
                if added:
                    tqdm.write(f"{domain}  +{added} URLs")
                else:
                    tqdm.write(f"{domain}  (0)")
            except Exception as e:
                tqdm.write(f"{domain}  error: {e}")
            pbar.update(1)

    pbar.close()

    print("\n")
    print(f"Total unique URLs : {len(seen_urls):,}")
    print(f"Rejected (date)   : {rejected['date']:,}")
    print(f"Rejected (topic)  : {rejected['relevance']:,}")
    print(f"Saved to          : {OUTPUT_FILE}")