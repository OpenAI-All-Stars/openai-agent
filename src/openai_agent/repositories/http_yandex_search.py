import asyncio
import json
import logging
import os
from xml.etree import ElementTree

import aiohttp
import backoff

from openai_agent.deps import http_client


logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.constant, (aiohttp.ClientError, asyncio.TimeoutError), max_tries=3)
async def search(query: str) -> str:
    client = http_client.get()
    resp = await client.get(
        os.getenv('YANDEX_SEARCH_URL') or 'https://yandex.ru/search/xml',
        params={
            'apikey': os.getenv('YANDEX_SEARCH_API_KEY'),
            'folderid': os.getenv('YANDEX_FOLDERID'),
            'filter': 'none',
            'lr': '225',
            'l10n': 'ru',
            'query': query,
            'page': 1,
        },
    )
    resp.raise_for_status()
    data = await resp.text()

    root = ElementTree.fromstring(data)

    results = []
    for doc in root.iter('doc'):
        description = []
        e = doc.find('charset')
        charset = e.text if e else 'utf-8'
        passages = doc.find('passages')
        if passages is not None:
            for passage in passages:
                description.append(ElementTree.tostring(passage, encoding=charset, method='text').decode())
        else:
            title = doc.find('title')
            if title:
                description.append(ElementTree.tostring(title, encoding=charset, method='text').decode())

        e = doc.find('url')
        if e is not None:
            results.append({
                'url': e.text,
                'description': '\n'.join(description)
            })

    if not results:
        return f'search fail: {data}'

    return json.dumps(results)
