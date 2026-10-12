import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse
from urllib.error import HTTPError, URLError

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/systematic-research/scripts'
sys.path.insert(0, str(SCRIPTS))


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ATOM = b'''<feed xmlns="http://www.w3.org/2005/Atom">
<entry><id>https://arxiv.org/abs/2604.13536v1</id><title>Example</title>
<summary>Example abstract</summary><author><name>Author</name></author>
<published>2026-04-01T00:00:00Z</published></entry></feed>'''


class SearchTests(unittest.TestCase):
    def test_arxiv_query_not_double_encoded(self):
        arxiv = load('search-arxiv')
        with patch('urllib.request.urlopen', return_value=io.BytesIO(ATOM)) as request:
            arxiv.search_arxiv('agent filesystem', category='cs.OS')
        url = request.call_args.args[0].full_url
        self.assertTrue(url.startswith('https://'))
        self.assertEqual(parse_qs(urlparse(url).query)['search_query'],
                         ['cat:cs.OS AND (all:agent AND all:filesystem)'])

    def test_arxiv_failure_is_not_empty_success(self):
        arxiv = load('search-arxiv')
        with patch('urllib.request.urlopen', side_effect=URLError('offline')), patch('time.sleep'):
            with self.assertRaises(Exception):
                arxiv.search_arxiv('agent')

    def test_arxiv_published_only_forwarded_and_empty_written(self):
        arxiv = load('search-arxiv')
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(arxiv, 'search_arxiv', return_value=[]) as search:
                with patch.object(sys, 'argv', ['search-arxiv.py', 'agent', '--published-only', '--output', directory]):
                    arxiv.main()
            self.assertTrue(search.call_args.kwargs['published_only'])
            data = json.loads((Path(directory) / 'results.json').read_text())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['count'], 0)

    def test_openalex_uses_current_types_and_handles_null_locations(self):
        academic = load('search-academic')
        body = json.dumps({'results': [{'title': 'Example', 'primary_location': None}]}).encode()
        with patch('urllib.request.urlopen', return_value=io.BytesIO(body)) as request:
            results = academic.search_academic('filesystem')
        params = parse_qs(urlparse(request.call_args.args[0].full_url).query)
        self.assertIn('type:article', params['filter'][0])
        self.assertNotIn('proceedings-article', params['filter'][0])
        self.assertEqual(len(results), 1)

    def test_openalex_failure_returns_nonzero_and_preserves_previous_results(self):
        academic = load('search-academic')
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / 'search-results.json'
            result.write_text('previous successful search')
            with patch.object(sys, 'argv', ['search-academic.py', 'x', '--output', directory]):
                with patch('urllib.request.urlopen', side_effect=URLError('offline')), patch('time.sleep'):
                    with self.assertRaises(SystemExit) as error:
                        academic.main()
            self.assertNotEqual(error.exception.code, 0)
            self.assertEqual(result.read_text(), 'previous successful search')
            self.assertEqual(json.loads((Path(directory) / 'search-error.json').read_text())['status'], 'error')

    def test_verifier_preserves_arxiv_id_from_url(self):
        verify = load('verify-against-source')
        self.assertEqual(verify.extract_arxiv_id({'url': 'https://arxiv.org/abs/2604.13536v2'}), '2604.13536')

    def test_retry_after_then_success(self):
        import search_support
        error = HTTPError('https://example.test', 429, 'limited', {'Retry-After': '7'}, None)
        with patch('urllib.request.urlopen', side_effect=[error, io.BytesIO(b'ok')]) as request:
            with patch('time.sleep') as sleep:
                self.assertEqual(search_support.read_url('https://example.test'), b'ok')
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(7.0)

    def test_nontransient_error_not_retried(self):
        import search_support
        error = HTTPError('https://example.test', 400, 'bad query', {}, None)
        with patch('urllib.request.urlopen', side_effect=error) as request:
            with self.assertRaises(search_support.SearchError):
                search_support.read_url('https://example.test')
        self.assertEqual(request.call_count, 1)

    def test_api_error_feed_not_a_paper(self):
        arxiv = load('search-arxiv')
        body = ATOM.replace(b'https://arxiv.org/abs/2604.13536v1', b'https://arxiv.org/api/errors#query')
        with patch('urllib.request.urlopen', return_value=io.BytesIO(body)):
            with self.assertRaises(Exception):
                arxiv.search_arxiv('agent')

    def test_missing_web_dependency_is_reported_not_import_exit(self):
        web = load('search-web')
        with patch.dict(sys.modules, {'ddgs': None, 'duckduckgo_search': None}):
            with self.assertRaisesRegex(Exception, 'requirements.txt'):
                web.search_web('agent')

    def test_failed_web_search_preserves_prior_results(self):
        web = load('search-web')
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / 'search-results.json'
            result.write_text('previous')
            with patch.object(web, 'search_web', side_effect=RuntimeError('offline')):
                with patch.object(sys, 'argv', ['search-web.py', 'agent', '--output', directory]):
                    with self.assertRaises(SystemExit) as error:
                        web.main()
            self.assertEqual(error.exception.code, 1)
            self.assertEqual(result.read_text(), 'previous')

    def test_verification_cannot_pass_partial_failure_with_fix(self):
        verify = load('verify-against-source')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'results.json'
            path.write_text(json.dumps({'results': [{'title': 'A'}, {'title': 'B'}]}))
            responses = [({'verified': True}, ['TITLE MISMATCH']), ({'verified': False}, ['API unreachable'])]
            with patch.object(verify, 'verify_entry', side_effect=responses), patch('time.sleep'):
                with patch.object(sys, 'argv', ['verify.py', str(path), '--fix']):
                    with self.assertRaises(SystemExit) as error:
                        verify.main()
            self.assertEqual(error.exception.code, 2)
            self.assertFalse(json.loads(path.read_text())['verified_against_source'])

    def test_non_arxiv_identifier_not_routed_to_arxiv(self):
        verify = load('verify-against-source')
        self.assertIsNone(verify.extract_arxiv_id({'id': 'https://openalex.org/W123'}))

    def test_success_clears_old_failure(self):
        import search_support
        with tempfile.TemporaryDirectory() as directory:
            search_support.search_failed(directory, 'arxiv', 'x', 'offline')
            search_support.search_succeeded(directory, 'results.json', {'results': []})
            self.assertFalse((Path(directory) / 'search-error.json').exists())

    def test_long_retry_after_not_shortened(self):
        import search_support
        error = HTTPError('https://example.test', 429, 'limited', {'Retry-After': '120'}, None)
        with patch('urllib.request.urlopen', side_effect=error), patch('time.sleep') as sleep:
            with self.assertRaisesRegex(search_support.SearchError, 'retry later'):
                search_support.read_url('https://example.test')
        sleep.assert_not_called()

    def test_openalex_key_only_in_header(self):
        academic = load('search-academic')
        with patch.dict('os.environ', {'OPENALEX_API_KEY': 'test-key'}):
            with patch('urllib.request.urlopen', return_value=io.BytesIO(b'{"results": []}')) as call:
                academic.search_academic('filesystem')
        request = call.call_args.args[0]
        self.assertEqual(request.get_header('Authorization'), 'Bearer test-key')
        self.assertNotIn('test-key', request.full_url)

    def usenix(self):
        path = SCRIPTS.parent / 'search-engines/cs/system/search-usenix.py'
        spec = importlib.util.spec_from_file_location('usenix', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_usenix_requires_years(self):
        usenix = self.usenix()
        with patch.object(sys, 'argv', ['search-usenix.py', 'fast']):
            with self.assertRaises(SystemExit) as error:
                usenix.main()
        self.assertEqual(error.exception.code, 2)

    def test_usenix_failure_does_not_write_empty_results(self):
        usenix = self.usenix()
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(usenix, 'fetch_page', side_effect=RuntimeError('offline')):
                with patch.object(sys, 'argv', ['search-usenix.py', 'fast', '--year', '2025', '--output', directory]):
                    with self.assertRaises(SystemExit) as error:
                        usenix.main()
            self.assertEqual(error.exception.code, 1)
            self.assertFalse((Path(directory) / 'results.json').exists())
            self.assertTrue((Path(directory) / 'search-error.json').exists())

    def test_usenix_title_filter_can_have_real_zero_hits(self):
        usenix = self.usenix()
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(usenix, 'fetch_page', return_value='<html/>'):
                with patch.object(usenix, 'parse_papers', return_value=[{'title': 'An unrelated paper'}]):
                    with patch.object(sys, 'argv', ['search-usenix.py', 'fast', '--year', '2025', '--query', 'snapshot', '--output', directory]):
                        usenix.main()
            data = json.loads((Path(directory) / 'results.json').read_text())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['count'], 0)


if __name__ == '__main__':
    unittest.main()
