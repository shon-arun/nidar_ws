from setuptools import find_packages, setup

package_name = 'opsg_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shon Arun',
    maintainer_email='shonarun3785@gmail.com',
    description='Perception and computer vision nodes, including YOLO human detection, for OpSG drones.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_viewer_node = opsg_perception.camera_viewer_node:main',
            'yolo_detection_node = opsg_perception.yolo_detection_node:main'
        ],
    },
)
