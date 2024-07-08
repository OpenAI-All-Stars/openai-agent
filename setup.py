from setuptools import setup, find_packages


setup(
    name="openai-agent",
    version="0.1.0",
    description="",
    author="Ilya Chistyakov",
    author_email="ilchistyakov@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "openai==0.28.1",
        "click==8.1.7",
        "colorama==0.4.6",
        "python_dotenv==1.0.1",
        "backoff==1.11.1",
        "aiohttp==3.9.5",
        "markdownify==0.12.1"
    ],
    extras_require={
        "dev": [
            "mypy==1.4.0",
            "flake8==6.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "openai-agent=openai_agent.cli:cli"
        ]
    },
    python_requires=">=3.10",
)
