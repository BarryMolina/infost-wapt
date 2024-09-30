import requests
import time
import sys


def intrude(infile, outfile): 
    with open(infile) as f, open(outfile, 'w') as out:
        out.write('url|status_code|content_length\n')
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                sent = False
                backoff = 0
                url = f'https://goerkecourses.com/wapt/module3/egg-hunt/{line}/'
                while not sent and backoff <= max_backoff:
                    try:
                        # wait backoff seconds before sending the request
                        if backoff > 0:
                            print(f'waiting {backoff} seconds...')
                            time.sleep(backoff)
                        r = requests.get(url)
                        out.write(f"{url}|{r.status_code}|{r.headers['content-length']}\n")
                        sent = True
                    except requests.exceptions.RequestException as e:
                        print(f'Error: {e}')
                        if backoff == max_backoff:
                            print(f'Failed to send request to {url}')
                            out.write(f"{url}|error|0\n")
                            sent = True
                        backoff += 5

filename = 'all.txt'
outfile = 'out_all.txt'
max_backoff = 60



                    


            
