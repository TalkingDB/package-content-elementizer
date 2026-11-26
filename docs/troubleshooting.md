# Troubleshooting

[Docs home](README.md) › Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| `EnvironmentError: CE_DOCX_PAGINATE is enabled but soffice is not on PATH` at import | DOCX pagination is on by default and LibreOffice is not installed | Install `libreoffice-writer` (it is in the [Docker](https://docs.docker.com/get-started/docker-overview/) image), or set `CE_DOCX_PAGINATE=0` |
| PDF fails with a message about a scanned or image only document | The PDF has fewer than `CE_PDF_MIN_TEXT_CHARS` characters of text; [OCR](https://en.wikipedia.org/wiki/Optical_character_recognition) is not supported | Run OCR first (for example with OCRmyPDF), then upload the result |
| `PASSWORD_PROTECTED` failure | The PDF is encrypted | Remove the password and upload again |
| `UNSUPPORTED_FILE_TYPE` failure | The file is not `.pdf` or `.docx` | Convert it first. `.doc` must be saved as `.docx` |
| PDF conversion stops after a long wait | It hit `CE_PDF_CONVERT_TIMEOUT_SECONDS` (3600) | Raise the timeout, or lower `CE_PDF_CONVERT_BATCH_PAGES` |
| The machine runs out of memory on large PDFs | Conversion holds many pages at once | Lower `CE_PDF_CONVERT_BATCH_PAGES` and set `CE_PDF_CONVERT_MAX_MEMORY_MB` |
| DOCX elements have no page numbers | `CE_DOCX_PAGINATE=0`, or the LibreOffice render failed or timed out | Install LibreOffice and turn pagination on; check `CE_DOCX_PAGINATE_TIMEOUT_SECONDS` |
| Spaces or line breaks look different from the original | Text is rebuilt from runs and converted layout, not copied from the screen | Expected for complex layouts; check the element's runs in the JSON |
| Tables in a PDF come out split or with wrong headers | Converting a PDF table to DOCX is a guess about layout | Check the table elements; see the [railway tables benchmark](https://github.com/TalkingDB/talkingdb-benchmarks/tree/main/railway-tables) for a known case |
| `ModuleNotFoundError: No module named 'talkingdb'` | `base-tdb-*` not installed | `make sync MODE=git && poetry install` |

## Further reading

- [OCRmyPDF](https://ocrmypdf.readthedocs.io/), to add a text layer to scanned PDFs
- [pdf2docx: known limitations](https://pdf2docx.readthedocs.io/en/latest/)

---

**Related:** [Architecture](architecture.md) · [Usage and examples](usage-and-examples.md) · [README](../README.md)
