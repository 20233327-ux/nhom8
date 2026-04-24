from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='abc-document-management',
    version='1.0.0',
    author='ABC Organization',
    author_email='admin@abc.org',
    description='ABC Document Management System - Quản lý Công văn với AI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/20233327-ux/nhom8',
    project_urls={
        'Documentation': 'https://github.com/20233327-ux/nhom8/wiki',
        'Bug Reports': 'https://github.com/20233327-ux/nhom8/issues',
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 6.0',
        'Intended Audience :: Business',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.12',
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'abc-app=app_launcher:main',
        ],
    },
    keywords='django document management workflow ocr digital-signature',
    zip_safe=False,
)
