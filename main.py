# Importing some Packages
from bs4 import BeautifulSoup
from itertools import zip_longest
import requests
import csv

url = 'https://www.imdb.com/what-to-watch/popular/?ref_=watch_wchgd_tab'
movie_name = []
movie_rate = []
description = []
creators = []
trailer = []
links = []

def get_info():
    for link in links:
        print(link)
        inner_page = requests.get(link)
        inner_soup = BeautifulSoup(inner_page.content, 'lxml')
        description.append(inner_soup.find('div', class_='summary_text').text.replace('\n', '').strip())
        creators.append(inner_soup.find('div', class_='credit_summary_item').text.replace('\n', '').replace('»', ''))

def write_csv():
    file_list = [movie_name, movie_rate, description, creators, trailer, links]
    exported = list(zip_longest(*file_list))
    with open('results/popular_movies.csv', mode='w') as file_object:
        wr = csv.writer(file_object)
        wr.writerow(['Movie name', 'Movie rate', 'Description', 'Creators', 'Trailer link', 'More Info'])
        wr.writerows(exported)
    print('SUCCESS: Check file to see RESULT!')

def main():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    movies = soup.find_all('div', {'class': 'ipc-poster-card ipc-poster-card--baseAlt ipc-poster-card--dynamic-width '
                                            'TitleCard-sc-1e5jqmp-0 fYcurh has-action-icons ipc-sub-grid-item ipc-sub-'
                                            'grid-item--span-2'})
    for movie in movies:
        movie_name.append(movie.find('span', {'data-testid': 'title'}).text)
        movie_rate.append(movie.find('span',
                                     {'class': 'ipc-rating-star ipc-rating-star--baseAlt ipc-rating-star--imdb'}).text)
        links.append('https://www.imdb.com' + movie.find('a', {'class': 'ipc-poster-card__title ipc-poster-card__title'
                    '--clamp-2 ipc-poster-card__title--clickable'}).attrs['href'])
        trailer.append('https://www.imdb.com' + movie.find('a', {'class': 'ipc-button ipc-button--single-padding ipc-button--default-height ipc-button--'
                                        'core-baseAlt ipc-button--theme-baseAlt ipc-button--on-textPrimary '
                                        'ipc-text-button card-action-button'}).attrs['href'])
    get_info()
    write_csv()

if __name__ == '__main__':
    main()
