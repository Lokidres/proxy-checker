import requests
import argparse

def gc(filename):  # get_content
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Dosya bulunamadı.")
        return []

def gp(proxy):  # get_public_ip_with_proxy
    proxies = {
        "http": proxy,
        "https": proxy
    }
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
        r.raise_for_status()
        return r.json().get("origin")
    except requests.exceptions.RequestException:
        return None

def rp(filename):  # rotate_proxies
    plist = gc(filename)
    results = []

    for p in plist:
        print(f"Denenen proxy: {p}")
        ip = gp(p)
        if ip:
            print(f"Başarılı proxy: {p} - IP: {ip}")
            results.append((p, ip))
        else:
            print(f"Başarısız proxy: {p}")
    
    if not results:
        print("Hiçbir proxy çalışmadı.")
    return results

def main():
    parser = argparse.ArgumentParser(description="Proxy rotator ve IP kontrol aracı")
    parser.add_argument("-d", "--directory", required=True, help="Proxy listesinin bulunduğu dosya yolu")
    args = parser.parse_args()

    rp(args.directory)

if __name__ == "__main__":
    main()
