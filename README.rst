===========
gzip-stream
===========

`gzip-stream` is a super-tiny library that will help you compress by GZIP
on-the-fly.

`GZIPCompressedStream` class instance acting like an any other stream (in fact,
`GZIPCompressedStream` inherits `io.RawIOBase <https://docs.python.org/3/library/io.html#io.RawIOBase>`_),
but wraps another stream and compress it on-the-fly.

.. code-block:: python

    from gzip_stream import GZIPCompressedStream
    from my_upload_lib import MyUploadClient

    upload_client = MyUploadClient()
    with open('my_very_big_1tb_file.txt') as file_to_upload:
        compressed_stream = GZIPCompressedStream(
            file_to_upload,
            compression_level=7
        )
        upload_client.upload_fileobj(compressed_stream)

`GZIPCompressedStream` does not read entire stream, but instead read it
by chunks, until compressed output size will not satisfy read size.

`AsyncGZIPDecompressedStream` class can async read from another source
with zlib and gzip decompression on-the-fly

.. code-block:: python
    # aiobotocore example

    import aiobotocore

    from gzip_stream import AsyncGZIPDecompressedStream

    AWS_ACCESS_KEY_ID = "KEY_ID"
    AWS_SECRET_ACCESS_KEY = "ACCESS_KEY"
    BUCKET = "AWESOME_BUCKET"

    upload_client = MyAsyncUploadClient()
    session = aiobotocore.get_session()
    async with session.create_client(
        service_name="s3",
        endpoint_url="s3_endpoint",
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
    ) as client:
        response = await client.get_object(Bucket=BUCKET, Key='my_very_big_1tb_file.txt.gz')
        async for decompressed_chunk in GzipAsyncReaderWrapper(response["Body"])):
            await upload_client.upload_fileobj(decompressed_chunk)


Module works on Python ~= 3.5.

Installation
------------
.. code-block:: bash

    pip install gzip-stream


License
-------
Public Domain: `CC0 1.0 Universal <https://creativecommons.org/publicdomain/zero/1.0/>`_.
