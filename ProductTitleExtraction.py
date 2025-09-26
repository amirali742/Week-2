from playwright.sync_api import sync_playwright, TimeoutError
import csv

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=150)  

    # Create a context with video recording enabled
    context = browser.new_context(
        record_video_dir="videos/"  # videos will be saved in this folder
    )  
    page = context.new_page()

    # Open Daraz homepage
    page.goto("https://www.daraz.pk/#?", wait_until="domcontentloaded", timeout=60000)

    # Close popup if present
    try:
        page.locator("button[aria-label='Close']").click(timeout=5000)#checked for pop-ups when page loads, and removed them.
        print("Closed popup")
    except:
        print("No popup")

    # Search for laptops
    search_input = page.locator("input[type='search']").first
    search_input.fill("laptops")
    search_input.press("Enter")

    # Selectors for product titles and prices
    products_title_selector = "[data-spm-anchor-id]"  
    products_price_selector = "div.aBrP0 span.ooOxS"

    # Wait for product titles to load (max 2 minutes)
    try:
        page.wait_for_selector(products_title_selector, timeout=120000)
        print("Daraz laptops page loaded successfully")
    except TimeoutError:
        print("Products did not load!")
        browser.close()
        exit()

    # Extract first 10 titles and prices
    titles = page.locator(products_title_selector).all_inner_texts()[:10]
    prices = page.locator(products_price_selector).all_inner_texts()[:10]
    extracted_items = list(zip(titles, prices))

    # Print extracted items
    print("\nExtracted Items:")
    for idx, (title, price) in enumerate(extracted_items, start=1):
        print(f"{idx}. {title} --> {price}")

    # Save to CSV
    csv_file = "daraz_laptops.csv"
    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Price"])
            for title, price in extracted_items:
                writer.writerow([title, price])
        print(f"\nCSV file created successfully: {csv_file}")
    except PermissionError:
        print(f"\nPermissionError: Could not write to {csv_file}. Make sure it is not open in another program.")

    print("\nTest Passed")

    # Close page & context to finalize video
    page.close()
    video_path = page.video.path()
    context.close()

    print(f"Video saved at: {video_path}")

    browser.close()
