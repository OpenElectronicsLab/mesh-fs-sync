import meshfssync
import tempfile
from pathlib import Path


def test_sha_for_file():
    # $ sha256sum COPYING
    # 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903 COPYING
    sha = "8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903"
    blocksize_4k = 4 * 1024
    with open("./COPYING", "rb") as fp:

        class WrappedFp:
            def read(self, blocksize):
                assert blocksize <= blocksize_4k
                return fp.read(blocksize_4k)

        h = meshfssync.sha256_for_file(WrappedFp(), blocksize_4k)
        assert h == sha


def test_get_dir_state():
    # $ echo 'foo' > foo.txt
    # $ sha256sum foo.txt
    # b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c foo.txt
    foohash = "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c"
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        file1 = tmpdir.joinpath("file1.txt")
        file2 = tmpdir.joinpath("file2.txt")
        file1.write_text("foo\n")
        file2.write_text("bar\n")
        subdir = tmpdir.joinpath("sub")
        subdir.mkdir()
        file3 = subdir.joinpath("file3.txt")
        file3.write_text("baz\n")

        root = meshfssync.get_path_state(tmpdir)
        assert root["type"] == "directory"
        ds = root["dir_state"]

        assert len(ds) == 3
        assert "file1.txt" in ds
        assert "file2.txt" in ds
        assert "sub" in ds

        assert ds["file1.txt"]["sha256"] == foohash
        assert ds["file1.txt"]["type"] == "file"

        assert ds["sub"]["type"] == "directory"
        subds = ds["sub"]["dir_state"]
        assert len(subds) == 1
        assert "file3.txt" in subds
