"""Stage the same reviewed application payload for the native OpenWrt SDK."""
import io
from pathlib import Path
import tarfile
import build

root = build.ROOT
ipk, _ = build.build()
dest = root / 'release-assets/root'
dest.mkdir(parents=True, exist_ok=True)
with tarfile.open(ipk, 'r:gz') as outer:
    payload = outer.extractfile('./data.tar.gz').read()
with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as data:
    # Only our locally generated payload, with explicit regular files/directories.
    for entry in data:
        relative = Path(entry.name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe package path')
        target = dest / relative
        if entry.isdir():
            target.mkdir(parents=True, exist_ok=True)
            target.chmod(entry.mode)
        elif entry.isfile():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data.extractfile(entry).read())
            target.chmod(entry.mode)
        else:
            raise ValueError('Unexpected package member')
