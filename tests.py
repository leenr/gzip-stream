import asyncio
import gzip
from gzip import decompress
from io import BytesIO
from pathlib import Path

import pytest
from faker import Faker

from gzip_stream import (
    GZIPCompressedStream, AsyncGZIPDecompressedStream,
    BaseAsyncIteratorReader, BUFFER_SIZE
)


@pytest.mark.parametrize(
    'data', [
        b'', b't', b'test',
        Faker().text(4 * 1024).encode(),
        Faker().text(256 * 1024).encode()
    ],
    ids=['0 bytes', '1 bytes', '4 bytes',
         'fake text - ~4 KB', 'fake text - ~256 KB']
)
def test_basic(data):
    input_stream = BytesIO(data)
    output_stream = GZIPCompressedStream(input_stream, compression_level=5)
    assert decompress(output_stream.read()) == data


class FakeAsyncReader(BaseAsyncIteratorReader):
    def __init__(self, filename: Path):
        self._fp = open(str(filename), 'rb')
        self._lock = asyncio.Lock()

    async def read(self, size: int = BUFFER_SIZE):
        async with self._lock:
            return self._fp.read(size)

    def __del__(self):
        self._fp.close()


@pytest.mark.parametrize(
    'expected',
    [
        '', 't', 'test',
        Faker().text(4 * 1024),
        Faker().text(256 * 1024)
    ],
    ids=['0 bytes', '1 bytes', '4 bytes',
         'fake text - ~4 KB', 'fake text - ~256 KB']
)
@pytest.mark.asyncio
async def test_gzip_aiter_async_reader(expected, tmpdir):
    tmp_file = tmpdir / 'temp.txt'
    with gzip.open(str(tmp_file), 'wb') as f:
        f.write(expected.encode('utf-8'))

    buffer = BytesIO()
    async for chunk in AsyncGZIPDecompressedStream(FakeAsyncReader(tmp_file)):
        buffer.write(chunk)
    buffer.seek(0)
    assert buffer.read().decode('utf-8') == expected


@pytest.mark.parametrize(
    'buff_size',
    [
        2,
        4,
        8,
        16,
        1024
    ],
    ids=['2 bytes', '4 bytes', '8 bytes',
         '16 bytes', '1 KB']
)
@pytest.mark.asyncio
async def test_buffer_gzip_async_reader(tmpdir, buff_size):
    plain_text = 'hello world' * 1000

    tmp_file = tmpdir / 'temp.txt'
    with gzip.open(str(tmp_file), 'wb') as f:
        f.write(plain_text.encode('utf-8'))

    buffer = BytesIO()
    reader = AsyncGZIPDecompressedStream(FakeAsyncReader(tmp_file))
    while True:
        chunk = await reader.read(buff_size)
        if not chunk:
            break
        buffer.write(chunk)
    buffer.seek(0)
    assert buffer.read().decode('utf-8') == plain_text
