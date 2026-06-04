import urllib.request, json, re
req = urllib.request.Request('https://lite.duckduckgo.com/lite/', data=b'q=partisipasi+masyarakat+musrenbang+mojokerto', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
urls = re.findall(r'href="([^"]+)"', html)
print([u for u in urls if 'http' in u][:5])
