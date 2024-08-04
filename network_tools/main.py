import socket
import whois
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup


def get_ip(domain):
    ip_address = socket.gethostbyname(domain)
    print(f"IP: {ip_address}")
    return ip_address


def who_is(domain):
    whois_sorgusu = whois.whois(domain)
    print(whois_sorgusu)


def port_tarayıcı(Hedef_ip_adresi):
    for port in range(0, 1000):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((Hedef_ip_adresi, port))
        if result == 0:
            print(f"{port} Açık")
        s.close()


def url_toplayıcı(domain):
    reqs = requests.get(f"http://{domain}")
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            if href.startswith('/'):
                href = f"http://{domain}{href}"
            if domain in href:
                urls.append(href)
    return urls


def xml_urls_toplayıcı(domain):
    urls = url_toplayıcı(domain)
    xml_urls = [url for url in urls if url.endswith('.xml')]
    return xml_urls


def fetch_and_parse_xml(url):
    response = requests.get(url)
    xml_content = response.content
    root = ET.fromstring(xml_content)
    print(f"Root tag: {root.tag}")
    for child in root:
        print(f"Tag: {child.tag}, Text: {child.text}")


def main():
    domain = input("Domain gir: ")
    ip_address = get_ip(domain)
    who_is(domain)
    port_tarayıcı(ip_address)

    urls = url_toplayıcı(domain)
    for url in urls:
        print(url)

    xml_urls = xml_urls_toplayıcı(domain)

    for xml_url in xml_urls:
        print(xml_url)
        fetch_and_parse_xml(xml_url)


main()
