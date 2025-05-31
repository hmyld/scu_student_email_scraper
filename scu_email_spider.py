from playwright.sync_api import sync_playwright
import time
import random
def open_page():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    ]
    random_ua = random.choice(user_agents)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                f"--user-agent={random_ua}"
            ]
            )
        url = r"https://mail.stu.scu.edu.cn"
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            accept_downloads=True,
            java_script_enabled=True,
            bypass_csp=True,
        )
        context.add_init_script("""
            () => {
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'languages', {
                    value: ['zh-CN', 'zh']
                });
            }
        """)
        page=context.new_page()
        page.goto(url,wait_until='networkidle')
        login(page)
        entry=False
        try:
            element=page.wait_for_selector('div.cnt:has-text("收件箱")', timeout=5000, state='visible')
            element.click()
            print("成功进入邮箱！")
            entry=True
        except:
            handle_verification_code(page)
        if not entry:
            try:
                element=page.wait_for_selector('div.cnt:has-text("收件箱")', timeout=300000, state='visible')
                element.click()
                print("成功进入邮箱！")
            except Exception as e:
                print(f"出现重要错误：{e}，请检查网络连接以及用户信息，或验证码信息！")
        q=input("是否屏蔽来自admin的信息? (y/n)")
        if q=='y':
            scupian_connection_to_emali(page)
        else:
            connection_to_emali(page)
        browser.close()
def login(page):
    username, password=load_credentials()
    if not username and not password:
        username,password=usr_ipt()
    time.sleep(1)
    page.keyboard.type(username)
    page.keyboard.press('Tab')
    page.keyboard.type(password)
    page.keyboard.press('Enter')
def handle_verification_code(page):
    page.screenshot(
        path="vc.jpeg",
        full_page=True,
        type="jpeg",
        quality=60
    )
    print("请在当前目录生成的jpeg图片中扫描二维码。")

def usr_ipt():
    username = input("请输入账号：")
    password = input("请输入密码：")
    save_condition = input("是否保存密码? (y/n)")
    if save_condition.lower() == 'y':
        with open('email.txt', 'w') as f:
            f.write(f"{username}\n{password}")
        print("账号密码已保存，稍后你可以在同一目录中email.txt中修改")
    return username, password
def load_credentials():
    try:
        with open('email.txt', 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
        return username, password
    except FileNotFoundError:
        return None, None
def scupian_connection_to_emali(page):
    try:
        page.wait_for_selector('tr.j-mail', timeout=20000, state='visible') 
        email = page.query_selector_all('tr.j-mail')
        for e in email:
            submitter_elem = e.query_selector('span.fromto.j-fromto')
            if submitter_elem:
                person = submitter_elem.text_content()
                if person=="admin":
                  continue
                print("-----------------------------------------------------------------------------------------------------------------------------")
                print(f"发件人：{person}")
            subject=e.query_selector('span.subject')
            if subject:
                notice=subject.text_content()
                print(f"标题：{notice}\n")
            summary=e.query_selector('span.summary')
            if summary:
                inner=summary.text_content()
                print(f"摘要：{inner}\n")
            time=e.query_selector('td.time')
            if time:
                date_pos=time.query_selector('span')
                date=date_pos.text_content()
                print(f"收件时间：{date}\n")
            print("-----------------------------------------------------------------------------------------------------------------------------")
            print(f"\n")
            print(f"\n")
    except Exception as e:
        print(f"处理页面时出现错误: {e}")
def connection_to_emali(page):
    try:
        page.wait_for_selector('tr.j-mail', timeout=20000, state='visible') 
        email = page.query_selector_all('tr.j-mail')
        for e in email:
            submitter_elem = e.query_selector('span.fromto.j-fromto')
            if submitter_elem:
                person = submitter_elem.text_content()
                print("-----------------------------------------------------------------------------------------------------------------------------")
                print(f"发件人：{person}")
            subject=e.query_selector('span.subject')
            if subject:
                notice=subject.text_content()
                print(f"标题：{notice}\n")
            summary=e.query_selector('span.summary')
            if summary:
                inner=summary.text_content()
                print(f"摘要：{inner}\n")
            time=e.query_selector('td.time')
            if time:
                date_pos=time.query_selector('span')
                date=date_pos.text_content()
                print(f"收件时间：{date}\n")
            print("-----------------------------------------------------------------------------------------------------------------------------")
            print(f"\n")
            print(f"\n")
    except Exception as e:
        print(f"处理页面时出现错误: {e}")
if __name__ == "__main__":
    open_page()
