import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # 使用无头模式启动浏览器
        browser = await p.chromium.launch(headless=True)  # 这里设为True表示无头模式
        context = await browser.new_context()
        page = await context.new_page()

        # 第一步：访问指定URL并获取checkoutUrl
        url = "http://codeium.serv-static.serv00.net/?teamName=2024.06.20-1"
        await page.goto(url)

        # 获取页面内容并解析JSON数据
        response = await page.content()
        data = await page.evaluate('''() => JSON.parse(document.querySelector("body").innerText)''')

        # 检查是否存在checkoutUrl
        if "checkoutUrl" not in data:
            print("checkoutUrl not found, stopping the script.")
            await browser.close()
            print("Script stopped.")
            return
        print("checkoutUrl found:", data["checkoutUrl"])
        checkout_url = data["checkoutUrl"]
        print("Checkout URL:", checkout_url)

        # 第二步：访问checkoutUrl
        print("Navigating to checkout URL...")
        await page.goto(checkout_url)
        print("Checkout URL navigated.")

        # 第三步：找到按钮并点击
        print("Clicking button...")
        await page.wait_for_selector('[data-testid="hosted-payment-submit-button"]')
        print("Button clicked.")
        await page.click('[data-testid="hosted-payment-submit-button"]')
        print("Payment successful.")

        # 保持浏览器打开状态以进行调试
        print("Waiting for 5 minutes...")
        await page.wait_for_selector('[data-testid="hosted-payment-submit-button"]')
        print("5 minutes passed.")
        # 在调试期间保持浏览器打开状态
        await asyncio.sleep(300)  # 等待5分钟，给你足够的时间进行调试
        print("Script finished.")

        # 关闭浏览器
        print("Closing browser...")
        await browser.close()
        print("Browser closed.")

# 运行脚本
asyncio.run(main())
