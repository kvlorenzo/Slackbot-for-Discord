from distutils.core import setup

setup(
    name='slackbot-for-discord',
    version='1.0',
    packages=['discord', 'dateparser', 'pytz'],
    url='https://github.com/kvlorenzo/Slackbot-for-Discord',
    license='MIT',
    author='Kyle Lorenzo',
    author_email='kvlorenz@ucsd.edu',
    description='A Discord bot with slackbot functionality',
    requires=['discord', 'dateparser', 'pytz']
)
