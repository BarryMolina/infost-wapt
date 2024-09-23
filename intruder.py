import requests

# filename = 'ZAP-directory-list-1.0.txt'
# filename = 'test_file.txt'
filename = 'ZAP-directory-list-1.0_mbcbbc.txt'
outfile = 'out.txt'

with open(filename) as f:
    with open(outfile, 'w') as out:
        out.write('url|status_code|content_length\n')
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                url = f'https://goerkecourses.com/wapt/module3/egg-hunt/{line}/'
                r = requests.get(url)
                if (r.status_code == 200):
                    print(f'status_code: 200, url: {url}')
                out.write(f"{url}|{r.status_code}|{r.headers['content-length']}\n")
            
