from io import StringIO
from io import BytesIO
import os

sio = StringIO('abc')
sio.write('def')
sio.write('ghi')
print(sio.getvalue())