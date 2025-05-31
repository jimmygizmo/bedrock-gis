from setuptools import setup, find_packages


setup(
    name='magma',
    version='1.0.0',
    description='Magma (GIS) - The FastAPI application module of The Bedrock-GIS Stack for geospatial apps. Copyright 2025 James Mannix. MIT License.',
    author='James Mannix',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

