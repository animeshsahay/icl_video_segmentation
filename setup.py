from distutils.core import setup

setup(
    name='Segmenter',
    version='0.0.1',
#    author=''
#    author_email=''
    packages=['segmenter', 'segmenter.test'],
    scripts=['bin/videoSegmenter'],
    url='https://github.com/cgizmo/icl_video_segmentation',
#    license='LICENSE.txt',
    description='Video segmentation based on clusters of faces.',
    long_description=open('README.txt').read(),
    install_requires=[
        "enzyme >= 0.2",
    ]
)
