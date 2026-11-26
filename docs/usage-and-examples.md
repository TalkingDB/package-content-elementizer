# Usage and examples

[Docs home](README.md) › Usage and examples

## Parse a file over HTTP

```bash
curl -s -X POST http://localhost:8091/content/parse \
  -F "document_file=@annual-report.pdf" \
  -F 'metadata={"scope": "org"}' > parsed.json
```

`metadata` is optional; it is a JSON string with request scope and tracing fields (see `Metadata` in [base-tdb-models](https://github.com/TalkingDB/base-tdb-models/blob/main/talkingdb/models/metadata/metadata.py)). The response is `{"document": ..., "file_index": ...}`.

Look at the outline with [jq](https://jqlang.github.io/jq/):

```bash
jq '.file_index' parsed.json | head -40
```

## Parse a file in process

```python
import asyncio
from talkingdb.helpers.client import config      # reads CLIENT_MODE, CE_HOST from the environment
from talkingdb_ce.client import CEClient

client = CEClient(config)           # CLIENT_MODE=direct (default): no server needed
with open("annual-report.pdf", "rb") as fh:
    result = asyncio.run(client.parse_file(file_bytes=fh.read(), file_name="annual-report.pdf"))
```

With `CLIENT_MODE=api` and `CE_HOST=http://localhost:8091`, the same code calls a running server instead.

[module-ttt](https://github.com/TalkingDB/module-ttt/blob/main/app/services/jobs.py) builds a `CEClient` this way for every ingestion job and passes a cancel check, so a cancelled upload stops the conversion process.

## Run without LibreOffice

On a laptop without LibreOffice you can still parse DOCX files; you lose page numbers:

```bash
export CE_DOCX_PAGINATE=0
make local
```

PDFs still get page numbers, because those come from the PDF itself.

## Large PDFs

Long PDFs are converted in batches. Tune these if conversion is slow or the machine runs out of memory:

```bash
export CE_PDF_CONVERT_BATCH_PAGES=25        # fewer pages per batch
export CE_PDF_CONVERT_MAX_MEMORY_MB=4096    # cap the conversion process
export CE_PDF_CONVERT_TIMEOUT_SECONDS=7200  # allow more time
```

## What an element looks like

Paragraphs keep their text runs (bold, italic, colour), their style (Heading 1, List, Normal) and their page. Tables keep rows, cells and which rows or columns are headers, so a cell can later be read together with its column name. The full shapes are in [`talkingdb/models/document/elements/`](https://github.com/TalkingDB/base-tdb-models/tree/main/talkingdb/models/document/elements) of base-tdb-models.

For a public, measured example of why table structure matters, see the [railway tables benchmark](https://github.com/TalkingDB/talkingdb-benchmarks/tree/main/railway-tables), which shows rows lost at PDF page breaks by standard extraction.

---

**Related:** [Architecture](architecture.md) · [Troubleshooting](troubleshooting.md) · [README](../README.md)
