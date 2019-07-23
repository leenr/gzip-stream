from io import BytesIO
from gzip import decompress

import pytest
from faker import Faker

from gzip_stream import GZIPCompressedStream


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
