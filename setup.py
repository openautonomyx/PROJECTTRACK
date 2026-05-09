from setuptools import setup, find_packages

setup(
    name="projecttrack",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "projecttrack=projecttrack.driver:main"
        ]
    },
    description="Project tracking workspace with reusable Project Driver Agent automation",
    author="OpenAutonomyX",
    license="MIT",
    python_requires=">=3.9"
)