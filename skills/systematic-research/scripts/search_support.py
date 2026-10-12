"""Shared bounded HTTP retries and explicit search outcome files (stdlib only)."""
import json
import time
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError


class SearchError(RuntimeError):
    pass


def read_url(request, attempts=3, timeout=30):
    """Retry connection failures, 429 and 5xx; never turn failures into no hits."""
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError, OSError) as error:
            retryable = not isinstance(error, HTTPError) or error.code == 429 or 500 <= error.code < 600
            if not retryable or attempt == attempts - 1:
                raise SearchError(str(error)) from error
            delay = 3 * (attempt + 1)
            if isinstance(error, HTTPError):
                retry_after = error.headers.get('Retry-After') if error.headers else None
                if retry_after:
                    try:
                        delay = max(delay, float(retry_after))
                    except ValueError:
                        try:
                            delay = max(delay, (parsedate_to_datetime(retry_after) - datetime.now(timezone.utc)).total_seconds())
                        except (TypeError, ValueError, OverflowError):
                            pass
            # A long server-requested pause must not be silently shortened.
            if delay > 60:
                raise SearchError(f'{error}; Retry-After exceeds retry budget; retry later') from error
            time.sleep(delay)


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def search_failed(output_dir, source, query, error):
    """Keep previous successful results; record this invocation separately."""
    write_json(Path(output_dir) / 'search-error.json', {
        'status': 'error', 'source': source, 'query': query,
        'timestamp': datetime.now(timezone.utc).isoformat(), 'error': str(error),
    })


def search_succeeded(output_dir, filename, output):
    output.update(status='success', count=len(output['results']))
    write_json(Path(output_dir) / filename, output)
    (Path(output_dir) / 'search-error.json').unlink(missing_ok=True)
