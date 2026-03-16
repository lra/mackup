"""Tests for pathresolver module."""

from mackup.pathresolver import (
    _is_excluded,
    is_glob_pattern,
    parse_paths,
    resolve_paths,
)


class TestParsePaths:
    def test_no_excludes(self):
        includes, excludes = parse_paths({".config/foo", ".config/bar"})
        assert sorted(includes) == [".config/bar", ".config/foo"]
        assert excludes == []

    def test_with_excludes(self):
        includes, excludes = parse_paths(
            {".config/foo", "!.config/foo/cache", ".config/bar"},
        )
        assert sorted(includes) == [".config/bar", ".config/foo"]
        assert excludes == [".config/foo/cache"]

    def test_empty(self):
        includes, excludes = parse_paths(set())
        assert includes == []
        assert excludes == []


class TestIsGlobPattern:
    def test_star(self):
        assert is_glob_pattern("*.json") is True

    def test_question(self):
        assert is_glob_pattern("file?.txt") is True

    def test_bracket(self):
        assert is_glob_pattern("file[0-9].txt") is True

    def test_plain(self):
        assert is_glob_pattern(".config/foo") is False

    def test_exclamation_not_glob(self):
        assert is_glob_pattern("!.config/foo") is False


class TestIsExcluded:
    def test_exact_match(self):
        assert _is_excluded("a/b", ["a/b"]) is True

    def test_prefix_match(self):
        assert _is_excluded("a/b/c/d", ["a/b"]) is True

    def test_no_match(self):
        assert _is_excluded("a/c", ["a/b"]) is False

    def test_partial_name_no_match(self):
        assert _is_excluded("a/bc", ["a/b"]) is False

    def test_glob_exclude(self):
        assert _is_excluded("a/foo.log", ["a/*.log"]) is True

    def test_glob_exclude_no_match(self):
        assert _is_excluded("a/foo.txt", ["a/*.log"]) is False


class TestResolvePaths:
    def test_literal_paths(self, tmp_path):
        result = resolve_paths(
            [".config/foo", ".config/bar"],
            [],
            str(tmp_path),
        )
        assert result == [".config/bar", ".config/foo"]

    def test_glob_expansion(self, tmp_path):
        config_dir = tmp_path / ".config"
        config_dir.mkdir()
        (config_dir / "a.json").touch()
        (config_dir / "b.json").touch()
        (config_dir / "c.txt").touch()

        result = resolve_paths([".config/*.json"], [], str(tmp_path))
        assert result == [".config/a.json", ".config/b.json"]

    def test_glob_with_excludes(self, tmp_path):
        config_dir = tmp_path / ".config"
        config_dir.mkdir()
        (config_dir / "a.json").touch()
        (config_dir / "b.json").touch()

        result = resolve_paths(
            [".config/*.json"],
            [".config/b.json"],
            str(tmp_path),
        )
        assert result == [".config/a.json"]

    def test_directory_with_excludes(self, tmp_path):
        plugins = tmp_path / ".claude" / "plugins"
        plugins.mkdir(parents=True)
        (plugins / "config.json").touch()
        (plugins / "blocklist.json").touch()
        cache_dir = plugins / "cache"
        cache_dir.mkdir()
        repos_dir = plugins / "repos"
        repos_dir.mkdir()

        result = resolve_paths(
            [".claude/plugins"],
            [".claude/plugins/cache", ".claude/plugins/repos"],
            str(tmp_path),
        )
        assert sorted(result) == [
            ".claude/plugins/blocklist.json",
            ".claude/plugins/config.json",
        ]

    def test_nested_excludes(self, tmp_path):
        a = tmp_path / "a" / "b"
        a.mkdir(parents=True)
        (a / "c").mkdir()
        (a / "d").touch()
        (tmp_path / "a" / "e").touch()

        result = resolve_paths(["a"], ["a/b"], str(tmp_path))
        assert result == ["a/e"]

    def test_nonexistent_glob(self, tmp_path):
        result = resolve_paths(["nonexistent/*.json"], [], str(tmp_path))
        assert result == []

    def test_literal_excluded(self, tmp_path):
        result = resolve_paths(
            ["a/b", "a/c"],
            ["a/b"],
            str(tmp_path),
        )
        assert result == ["a/c"]

    def test_no_excludes_no_globs_passthrough(self, tmp_path):
        result = resolve_paths(
            [".config/a", ".config/b"],
            [],
            str(tmp_path),
        )
        assert result == [".config/a", ".config/b"]
