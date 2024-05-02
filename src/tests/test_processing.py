""" Test processing module
@Author: Jai Wargacki"""

import os

import processing

def test_move_to_storage_basic():
    file_path = "test.txt"
    with open(file_path, 'w') as f:
        f.write("test")

    storage_path = "storage"
    if not os.path.exists(storage_path):
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
    if not os.path.exists(storage_path):
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

def test_extract_clip():
    video_path = "tests/test_data/demo_mp4_vid.mp4"
    start_frame = 2
    end_frame = 10
    storage_path = "storage"
    clip_path = processing.extract_clip(video_path, start_frame, end_frame, storage_path)
    assert os.path.exists(clip_path)
    # clean up
    os.remove(clip_path)

def test_extract_clip_multiple():
    video_path = "tests/test_data/demo_mp4_vid.mp4"
    start_frame = 2
    end_frame = 10
    storage_path = "storage"
    feature1 = "clip1"
    feature2 = "clip2"
    clip_path1 = processing.extract_clip(video_path, start_frame, end_frame, storage_path, feature1)
    clip_path2 = processing.extract_clip(video_path, start_frame, end_frame, storage_path, feature2)
    assert os.path.exists(clip_path1)
    assert os.path.exists(clip_path2)
    # clean up
    os.remove(clip_path1)
    os.remove(clip_path2)

def test_feature_init():
    name = "Test"
    description = "Test description"
    freq = 30
    verbose = True
    feature = processing.Feature(name, description, freq, verbose)
    assert feature.name == name
    assert feature.description == description
    assert feature.frame_frequency == freq
    assert feature.verbose == verbose

def test_feature_str():
    name = "Test"
    description = "Test description"
    feature = processing.Feature(name, description)
    assert str(feature) == f"{name}: {description}"

def test_feature_clear():
    name = "Test"
    description = "Test description"
    feature = processing.Feature(name, description)
    try:
        feature.clear()
        assert False
    except NotImplementedError:
        assert True

def test_feature_process():
    name = "Test"
    description = "Test description"
    feature = processing.Feature(name, description)
    try:
        feature.process(None, None)
        assert False
    except NotImplementedError:
        assert True

def test_feature_save():
    name = "Test"
    description = "Test description"
    feature = processing.Feature(name, description)
    try:
        feature.save(None, None)
        assert False
    except NotImplementedError:
        assert True

