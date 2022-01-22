import meshfssync
import tempfile
from pathlib import Path




def test_get_dir_state():
    # $ echo 'foo' > foo.txt
    # $ sha256sum foo.txt
    # b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c foo.txt
    foohash = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c'
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        file1 = tmpdir.joinpath('file1.txt')
        file2 = tmpdir.joinpath('file2.txt')
        file1.write_text('foo\n')
        file2.write_text('bar\n')


        ds = meshfssync.get_dir_state(tmpdir);
        assert len(ds) == 2
        assert 'file1.txt' in ds
        assert 'file2.txt' in ds

        assert ds['file1.txt']['sha256'] == foohash
