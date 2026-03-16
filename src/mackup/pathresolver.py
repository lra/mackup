"""Path resolver for glob and exclude pattern support in mackup cfg files."""

import fnmatch
import glob
import os


def parse_paths(raw_paths: set[str]) -> tuple[list[str], list[str]]:
    """Split raw paths into includes and excludes.

    Paths prefixed with '!' are excludes. All others are includes.
    """
    includes = []
    excludes = []
    for path in raw_paths:
        if path.startswith("!"):
            excludes.append(path[1:])
        else:
            includes.append(path)
    return includes, excludes


def is_glob_pattern(path: str) -> bool:
    """Check if a path contains glob characters (* ? [)."""
    return any(c in path for c in ("*", "?", "["))


def resolve_paths(
    includes: list[str],
    excludes: list[str],
    base_dir: str,
) -> list[str]:
    """Resolve includes/excludes/globs into concrete file paths.

    Args:
        includes: List of paths or glob patterns to include.
        excludes: List of paths or patterns to exclude.
        base_dir: The base directory (typically home dir) for resolving paths.

    Returns:
        Sorted list of concrete relative file paths.
    """
    result: list[str] = []

    for path in includes:
        if is_glob_pattern(path):
            # Expand glob relative to base_dir
            abs_pattern = os.path.join(base_dir, path)
            for match in glob.glob(abs_pattern):
                rel_path = os.path.relpath(match, base_dir)
                if not _is_excluded(rel_path, excludes):
                    result.append(rel_path)
        elif _has_matching_excludes(path, excludes):
            # Directory with excludes: expand children, filter out excluded
            result.extend(
                _expand_directory_with_excludes(path, excludes, base_dir),
            )
        elif not _is_excluded(path, excludes):
            # Literal path, no excludes apply
            result.append(path)

    return sorted(set(result))


def _has_matching_excludes(path: str, excludes: list[str]) -> bool:
    """Check if any exclude is a child of the given path."""
    return any(excl == path or excl.startswith(path + "/") for excl in excludes)


def _expand_directory_with_excludes(
    dir_path: str,
    excludes: list[str],
    base_dir: str,
) -> list[str]:
    """Expand a directory's immediate children, filtering out excluded ones."""
    abs_dir = os.path.join(base_dir, dir_path)
    if not os.path.isdir(abs_dir):
        if _is_excluded(dir_path, excludes):
            return []
        return [dir_path]

    result = []
    for child in os.listdir(abs_dir):
        child_path = os.path.join(dir_path, child)
        if not _is_excluded(child_path, excludes):
            result.append(child_path)
    return result


def _is_excluded(path: str, excludes: list[str]) -> bool:
    """Check if path matches any exclude pattern (exact, prefix, or fnmatch)."""
    for excl in excludes:
        if path == excl or path.startswith(excl + "/"):
            return True
        if is_glob_pattern(excl) and fnmatch.fnmatch(path, excl):
            return True
    return False
