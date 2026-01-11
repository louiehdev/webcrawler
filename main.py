import sys
import asyncio
from async_crawler import crawl_site_async
from csv_report import write_csv_report

async def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 4:
        print("too many arguments provided")
        sys.exit(1)

    if not args[2].isdigit():
        print("max_concurrency must be an integer")
        sys.exit(1)
    if not args[3].isdigit():
        print("max_pages must be an integer")
        sys.exit(1)
    
    base_url = args[1]
    max_concurrency = int(args[2])
    max_pages = int(args[3])

    print(f"starting crawl of: {base_url}")
    results = await crawl_site_async(base_url, max_concurrency, max_pages)
    
    print(f"number of pages crawled: {len(results)}")
    write_csv_report(results)



if __name__ == "__main__":
    asyncio.run(main())
