from setuptools import setup

setup(name='gym_scarecrow',
      version='0.0.1',
      url='https://github.com/ajberlier/gym-scarecrow',
      author='Adam J. Berlier',
      license='GPLv3',
      packages=['gym_scarecrow', "gym_scarecrow.envs"],
      package_data={
          "gym_scarecrow.envs": ["scarecrow_samples/*.npy"]
      },
      install_requires=["gym", "pygame", "numpy"]
      )
