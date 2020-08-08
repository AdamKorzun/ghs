import os
import re
import argparse
import requests
from shutil import which

parser = argparse.ArgumentParser(description='')
parser.add_argument('--f', '--find',help='Repository you want to find', required=True)
parser.add_argument('--o', '--output',help='Output directory')
parser.add_argument('--z', '--zip',help='Download as zip',action='store_true')
args = parser.parse_args()

def clone_from_github(url):
    if (args.o is not None):
        try:
            if (':' in args.o):
                if (args.z):
                    re = requests.get(url+ '/zipball/master', allow_redirects=True)
                    open(args.o + '/repo.zip','wb').write(re.content)
                    return
                os.system('cd / & {} & cd {} & git clone {}'.format(args.o[0] + args.o[1], args.o, url))
            else:
                if (args.z):
                    re = requests.get(url+ '/zipball/master', allow_redirects=True)
                    open(os.getcwd() + '/'+ args.o + '/repo.zip','wb').write(re.content)
                    return
                os.system('cd {} & git clone {}'.format(args.o, url))
        except Exception as e:
            print(e)
        return
    if (args.z):
        re = requests.get(url+ '/zipball/master', allow_redirects=True)
        open('repo.zip','wb').write(re.content)
        return
    os.system('git clone ' + url)

def find_on_github(name):
    pattern = re.compile('((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*')
    if (pattern.match(name)):
        if (requests.get(name).ok):
            return name
        else:
            raise Exception('ERROR: Can\'t find \'{}\''.format(name))

    elif ('/' in name):
        url = 'https://github.com/' + name.lower()
        if (requests.get(url).ok):
            return url
        else:
            raise Exception('ERROR: Can\'t find \'{}\''.format(url))
    else:
        try:
            repo = str(requests.get('https://api.github.com/search/repositories?q='+name.lower()).json()['items'][0]['html_url'])
            return repo
        except IndexError:
            raise Exception('ERRROR: Can\'t find \'{}\' on github'.format(name))
        except Exception as e:
            raise e


if __name__ == '__main__':
    if (not which('git')):
        args.z = True
        print('Can\'t find git, downloading as an archive')
    url = find_on_github(args.f)
    while True:
        res=input('Clone \'{}\'  [Y/N]\n'.format(url))
        if (res=='Y' or res=='y'):
            clone_from_github(url)
            break
        elif (res=='N' or res=='n'):
            print('Leaving...')
            break
        else:
            print("Wrong input")
