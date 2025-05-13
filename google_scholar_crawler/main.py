

from scholarly import scholarly, ProxyGenerator
import jsonpickle
import json
from datetime import datetime
import os

# Setup proxy
pg = ProxyGenerator()
pg.FreeProxies()  # Use free rotating proxies
scholarly.use_proxy(pg)
author: dict = scholarly.search_author_id("40KXmRMAAAAJ")

# author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
name = author['name']
	@@ -20,4 +25,4 @@
  "message": f"{author['citedby']}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
