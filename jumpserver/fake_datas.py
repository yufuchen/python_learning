import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

t = ThreadPoolExecutor(max_workers=8)
t.submit()
print(uuid.uuid4())