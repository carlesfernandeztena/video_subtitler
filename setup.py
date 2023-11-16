from setuptools import find_packages, setup

setup(
    version="1.0",
    name="video_subtitler",
    packages=find_packages(),
    py_modules=["video_subtitler"],
    author="Carles Fernández",
    install_requires=[
        'openai-whisper',
        'ffmpeg'
    ],
    description="Automatically generate a subtitle file for an input video",
    entry_points={
        'console_scripts': ['video_subtitler=video_subtitler.video_subtitler:main'],
    },
    include_package_data=True,
)
