from setuptools import find_packages, setup

package_name = 'roomba_pkg'

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
    maintainer='seiji',
    maintainer_email='seiji@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'joy_controller_node = roomba_pkg.joy_controller_node:main',
            'roomba_controller_node = roomba_pkg.roomba_controller_node:main',
            'roomba_node = roomba_pkg.roomba_node:main',
        ],
    },
)
