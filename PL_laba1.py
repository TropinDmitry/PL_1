import time
import sys
import urllib3
from threading import Thread

crrntSize: int = 0
fileSize: float = 0
tB: str = ""
fileName: str = ""

def sizeType(size: int) -> float:
    if size < 1024 and (tB == "" or tB == "b"):
        return round(size, 2)
    if size < 1024 * 1024 and (tB == "" or tB == "Kb"):
        return round(size / 1024, 2)
    else:
        return round(size / 1024 / 1024, 2)

def typeB(size: float) -> str:
    if size < 1024:
        return "b"
    if size < 1024 * 1024:
        return "Kb"
    else:
        return "Mb"
    
def download(url: str):
    global crrntSize
    global fileSize
    global fileName
    global tB
    http = urllib3.PoolManager()
    resp = http.request("GET", url, preload_content = False)
    fileName = url.split("/")[-1]
    fileSize = int(resp.getheader("Content-Length"))
    tB = typeB(fileSize)
    with open(fileName, 'wb') as file:
        while chunk := resp.read(1024):
            file.write(chunk)
            crrntSize += 1024

def stream():
    while True:
        time.sleep(1)
        if sizeType(crrntSize) < sizeType(fileSize):
            print(f"downloading: [{sizeType(crrntSize)}{tB} / {sizeType(fileSize)}{tB}]")
        if sizeType(crrntSize) >= sizeType(fileSize):
            print("\n", f"{fileName} downloaded: [{sizeType(fileSize)}{tB}]")
            break

def main():
    if len(sys.argv) > 1:
        thread = Thread(target = stream)
        thread.start()
        download(sys.argv[1])

if __name__ == "__main__":
    main()

