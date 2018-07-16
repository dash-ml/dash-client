from ml_logger import logger, Color, percent
from shutil import rmtree

# clean up previous tasks
TEST_LOG_DIR = '/tmp/ml_logger/test'
try:
    rmtree(TEST_LOG_DIR)
except FileNotFoundError as e:
    print(e)

logger.configure(TEST_LOG_DIR, prefix='main')

print("logging to {}".format(TEST_LOG_DIR))


def test():
    d = Color(3.1415926, 'red')
    s = "{:.1}".format(d)
    print(s)

    logger.log_params(G=dict(some_config="hey"))
    logger.log(step=0, some=Color(0.1, 'yellow'))
    logger.log(step=1, some=Color(0.28571, 'yellow', lambda v: "{:.5f}%".format(v * 100)))
    logger.log(step=2, some=Color(0.85, 'yellow', percent))
    logger.log({"some_var/smooth": 10}, some=Color(0.85, 'yellow', percent), step=3)
    logger.log(step=4, some=Color(10, 'yellow'))


def test_image():
    import scipy.misc
    import numpy as np

    image_bw = np.zeros((64, 64, 1), dtype=np.uint8)
    image_bw_2 = scipy.misc.face(gray=True)[::4, ::4]
    image_rgb = np.zeros((64, 64, 3), dtype=np.uint8)
    image_rgba = scipy.misc.face()[::4, ::4, :]
    logger.log_image(step=4, black_white=image_bw)
    logger.log_image(step=4, bw_face=image_bw_2)
    logger.log_image(step=4, rgb=image_rgb)
    logger.log_image(step=4, rgba_face=image_rgba)
    logger.log_image(step=5, rgba_face=image_bw)
    logger.log_image(step=6, rgba_face=image_rgba)

    # todo: animation is NOT implemented.
    # now print a stack
    # for i in range(10):
    #     logger.log_image(i, animation=[image_rgba] * 5)


def test_pyplot():
    import os, scipy.misc
    import matplotlib
    matplotlib.use('TKAgg')
    import matplotlib.pyplot as plt
    import numpy as np

    face = scipy.misc.face()
    logger.log_image(step=0, test_image=face)

    fig = plt.figure(figsize=(4, 2))
    xs = np.linspace(0, 5, 1000)
    plt.plot(xs, np.cos(xs))
    logger.savefig(fig=fig)
    plt.close()

    fig = plt.figure(figsize=(4, 2))
    xs = np.linspace(0, 5, 1000)
    plt.plot(xs, np.cos(xs))
    logger.savefig('sine.pdf')
    plt.close()


class FakeTensor:
    def cpu(self):
        return self

    def detach(self):
        return self

    def numpy(self):
        import numpy as np
        return np.ones([100, 2])


class FakeModule:
    @staticmethod
    def state_dict():
        return dict(var_1=FakeTensor())


def test_module():
    logger.log_module(step=0, Test=FakeModule)


def test_load_module():
    result, = logger.load_pkl(f"modules/{0:04d}_Test.pkl")
    import numpy as np
    assert (result['var_1'] == np.ones([100, 2])).all(), "should be the same as test data"


def test_load_params():
    pass


if __name__ == "__main__":
    test()
    test_image()
    test_pyplot()
    test_module()
    test_load_module()
    test_load_params()
    # todo: logger.log_module(6, rgba_face=image_rgba)
    # todo: logger.log_pyplot(6, rgba_face=image_rgba)
    # todo: logger.log_params(6, rgba_face=image_rgba)
    # todo: logger.log_file(6, rgba_face=image_rgba)
