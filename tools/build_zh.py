#!/usr/bin/env python3
"""Regenerate the static Chinese pages: python3 tools/build_zh.py.

English HTML is the source; translations live in translations/zh-CN.json.
New untranslated text stops the build instead of silently publishing mixed copy.
"""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import json
import os

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = json.loads((ROOT / 'translations/zh-CN.json').read_text())
SOURCES = [ROOT / 'index.html', *sorted((ROOT / 'research').glob('*.html')),
           *sorted((ROOT / 'projects').glob('*.html'))]


def translate(text):
    key = text.strip()
    if not key:
        return text
    if key not in TRANSLATIONS:
        raise ValueError(f'Missing Chinese translation: {key}')
    value = TRANSLATIONS[key]
    # Preserve spacing around unchanged names and technical terms.
    return text if value == key else value


class ChinesePage(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.destination = ROOT / 'zh' / source.relative_to(ROOT)
        self.output = []
        self.language_link = False

    def local_url(self, value):
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            return value
        target = (self.source.parent / url.path).resolve()
        relative = target.relative_to(ROOT)
        if target.suffix == '.html':
            target = ROOT / 'zh' / relative
        path = os.path.relpath(target, self.destination.parent).replace(os.sep, '/')
        return urlunsplit(('', '', path, url.query, url.fragment))

    def start(self, tag, attrs, closed=False):
        data = dict(attrs)
        language_link = tag == 'a' and 'language-switch' in data.get('class', '').split()
        if language_link:
            self.language_link = True
        result = []
        for key, value in attrs:
            if value is None:
                result.append(key)
                continue
            if tag == 'html' and key == 'lang':
                value = 'zh-CN'
            elif language_link and key == 'href':
                value = os.path.relpath(self.source, self.destination.parent).replace(os.sep, '/')
            elif language_link and key in ('lang', 'hreflang'):
                value = 'en'
            elif language_link and key == 'aria-label':
                value = 'Switch to English'
            elif key in ('href', 'src'):
                value = self.local_url(value)
            elif key in ('alt', 'aria-label') and value:
                value = translate(value)
            elif tag == 'meta' and key == 'content' and (
                data.get('name') == 'description' or
                data.get('property') in ('og:title', 'og:description')
            ):
                value = translate(value)
            result.append(f'{key}="{escape(value, quote=True)}"')
        self.output.append('<' + tag + (' ' + ' '.join(result) if result else '') + ('/>' if closed else '>'))

    def handle_starttag(self, tag, attrs):
        self.start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self.start(tag, attrs, True)

    def handle_endtag(self, tag):
        self.output.append(f'</{tag}>')
        if tag == 'a':
            self.language_link = False

    def handle_data(self, data):
        self.output.append(escape('English' if self.language_link else translate(data), quote=False))

    def handle_decl(self, declaration):
        self.output.append('<!' + declaration + '>')

    def handle_comment(self, data):
        self.output.append('<!--' + data + '-->')


def main():
    pages = []
    for source in SOURCES:
        parser = ChinesePage(source)
        parser.feed(source.read_text())
        parser.close()
        pages.append((parser.destination, ''.join(parser.output)))
    for destination, html in pages:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html)
    print(f'Generated {len(pages)} Chinese pages.')


if __name__ == '__main__':
    main()
