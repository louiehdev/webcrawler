import sys
from crawl import crawl_page

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {sys.argv[1]}")
    page_data = {}
    crawl_page(sys.argv[1], sys.argv[1], page_data)
    print(f"number of pages crawled: {len(page_data)}")



if __name__ == "__main__":
    main()
