from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'f1_tenth'

setup(
    name=package_name,
    version='0.0.1',

    packages=find_packages(exclude=['test']),

    data_files=[
        # ament index
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),

        # package.xml
        (
            'share/' + package_name,
            ['package.xml']
        ),

        # ✅ launch 파일
        (
            os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))
        ),

        # ✅ Autonomous_Driving 시나리오 BT XML
        (
            os.path.join(
                'share',
                package_name,
                'scenario',
                'autonomous_driving'
            ),
            glob(
                os.path.join(
                    'f1_tenth',
                    'scenario',
                    'autonomous_driving',
                    '*.xml'
                )
            )
        ),

        # ✅ Autonomous_Driving 시나리오 YAML
        (
            os.path.join(
                'share',
                package_name,
                'scenario',
                'autonomous_driving',
                'config'
            ),
            glob(
                os.path.join(
                    'f1_tenth',
                    'scenario',
                    'autonomous_driving',
                    'config',
                    '*.yaml'
                )
            )
        ),
    ],

    install_requires=[
        'setuptools',
        'py_trees',
        'rclpy',
        'mavros_msgs',
        'geometry_msgs'
    ],

    zip_safe=True,
    maintainer='jaeho',
    maintainer_email='jaeho@todo.todo',
    description='F1TENTH + BehaviorTree package',
    license='TODO',

    entry_points={
        'console_scripts': [
            'auto_drive = f1_tenth.scenario.autonomous_driving.main:main',
        ],
    },
)
