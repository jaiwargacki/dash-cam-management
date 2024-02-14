""" Test processing module
@Author: Jai Wargacki"""

import os

import processing

def test_move_to_storage_basic():
    file_path = "test.txt"
    with open(file_path, 'w') as f:
        f.write("test")

    storage_path = "storage"
    os.mkdir(storage_path)

    try:
        processing.move_to_storage(file_path, storage_path)

        assert os.path.exists(file_path)
        assert os.path.exists(os.path.join(storage_path, "test.txt"))
        with open(os.path.join(storage_path, "test.txt"), 'r') as f:
            assert f.read() == "test"
    except:
        assert False
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(os.path.join(storage_path, "test.txt")):
            os.remove(os.path.join(storage_path, "test.txt"))
        if os.path.exists(storage_path):
            os.rmdir(storage_path)

def test_move_to_storage_no_dir():
    file_path = "test.txt"
    with open(file_path, 'w') as f:
        f.write("test")

    storage_path = "storage"

    try:
        processing.move_to_storage(file_path, storage_path)

        assert os.path.exists(file_path)
        assert os.path.exists(os.path.join(storage_path, "test.txt"))
        with open(os.path.join(storage_path, "test.txt"), 'r') as f:
            assert f.read() == "test"
    except:
        assert False
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(os.path.join(storage_path, "test.txt")):
            os.remove(os.path.join(storage_path, "test.txt"))
        if os.path.exists(storage_path):
            os.rmdir(storage_path)

def test_move_to_storage_delete_file():
    file_path = "test.txt"
    with open(file_path, 'w') as f:
        f.write("test")

    storage_path = "storage"
    os.mkdir(storage_path)

    try:
        processing.move_to_storage(file_path, storage_path, True)

        assert not os.path.exists(file_path)
        assert os.path.exists(os.path.join(storage_path, "test.txt"))
        with open(os.path.join(storage_path, "test.txt"), 'r') as f:
            assert f.read() == "test"
    except:
        assert False
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(os.path.join(storage_path, "test.txt")):
            os.remove(os.path.join(storage_path, "test.txt"))
        if os.path.exists(storage_path):
            os.rmdir(storage_path)

