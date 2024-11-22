
import base64
import pickle
import functools
import hashlib
from pathlib import Path
from typing import Callable, Any, Tuple

# Cache storage
MEMORY_CACHE = {}
DISK_CACHE_DIR = Path("./cache")

# Ensure the disk cache directory exists
DISK_CACHE_DIR.mkdir(parents=True, exist_ok=True)

def list_tree(directory, indent=0):
    if not directory.exists():
        return f"{directory} does not exist.\n"

    tree = []
    for item in directory.iterdir():
        tree.append(" " * indent + f"- {item.name}")
        if item.is_dir():
            tree.append(list_tree(item, indent + 2))  # Recursively append subdirectory content

    return "\n".join(tree)


def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def cache_to_memory_and_disk(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(image, *args, **kwargs) -> Tuple[Any, Any]:
        # Generate the cache key
        image.seek(0)  # Ensure the image is at the start
        image_key = base64.b64encode(image.read()).decode("utf-8")
        image.seek(0)  # Reset for the function to reuse the file

        # Create a hashed key for disk storage
        hashed_key = hash_key(image_key)

        # Check in-memory cache
        if hashed_key in MEMORY_CACHE:
            print("Cache hit: Memory")
            return MEMORY_CACHE[hashed_key]

        # Check disk cache
        disk_cache_file = DISK_CACHE_DIR / f"{hashed_key}.pkl"
        if disk_cache_file.exists():
            print("Cache hit: Disk")
            with open(disk_cache_file, "rb") as f:
                result = pickle.load(f)
                MEMORY_CACHE[hashed_key] = result  # Store back in memory for faster access
                return result

        # Call the original function and cache the result
        print("Cache miss")
        result = func(image, *args, **kwargs)
        MEMORY_CACHE[hashed_key] = result

        # Store to disk
        with open(disk_cache_file, "wb") as f:
            pickle.dump(result, f)

        return result

    return wrapper
