#请在校园网环境使用，适用于研究生课程补退改选捡漏
from typing import Optional
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

student_id = "ididid"
student_password = "password"

select_course_category = 5
select_course_name = "D421061001-微纳米工艺与实践（02）"
select_course_id = "D421061001"

def setup_driver():
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--no-sandbox')  # 禁用沙箱
    chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
    chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小
    
    # 可选：禁用图片加载以提升速度
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    
    return webdriver.Chrome(options=chrome_options)

browser = setup_driver()


try:
    browser.get("https://yjsxk.buaa.edu.cn/")
    # 进入统一认证登录界面
    if browser.title=="统一身份认证":
        browser.switch_to.frame("loginIframe")
        username=browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]/div[2]/div[1]/div[1]/div/input')
        password=browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/input')
        username.send_keys(student_id)
        password.send_keys(student_password)
        confirm=browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]/div[2]/div[1]/div[7]/input')
        confirm.click()
        browser.switch_to.default_content()

    while True:
        # 进入选课首页，点击我的选课按钮
        browser.get("https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/index.html")
        time.sleep(0.5)
        browser.find_element(by=By.XPATH, value='/html/body/div[1]/article[1]/section/div[5]/div[2]/div[4]/a').click()
        time.sleep(0.2)

        # 课程类别选择，改<li>标签的索引以选择不同的课程类别
        browser.find_element(by=By.XPATH, value=f'/html/body/div[1]/article[2]/div[2]/div/ul/li[{select_course_category}]').click()

        # 输入课程号并搜索
        course_id = browser.find_element(By.XPATH, f"/html/body/div[1]/article[2]/div[2]/div/div/div[{select_course_category}]/form/input[1]")
        course_id.send_keys(select_course_id)
        browser.find_element(by=By.XPATH, value=f'/html/body/div[1]/article[2]/div[2]/div/div/div[{select_course_category}]/form/input[2]').click()
        

        # 等待课程信息表格加载
        table = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/article[2]/div[2]/div/div/div[{select_course_category}]/div/table/tbody"))
        )
        time.sleep(0.2)
        

        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            # 获取单元格
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 3:  # 确保行有足够的单元格
                # 获取课程
                course_link = cells[0].find_element(By.TAG_NAME, "a")
                course_name = course_link.text
                
                # 获取容量信息
                capacity_cell = cells[8]  # 根据表格结构，容量信息在第9个单元格
                capacity_text = capacity_cell.text

                time.sleep(0.2)
                
                print(f"课程: {course_name}, 容量: {capacity_text}")

                # 查找选课按钮
                select_button = cells[9].find_element(By.TAG_NAME, "a")

                # 检查是否是目标课程且还有容量
                if (course_name == select_course_name and 
                    capacity_text != "已满"):
                    
                    time.sleep(0.2)
                    select_button.click()
                
                    # 等待确认按钮出现并点击
                    confirm_button = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[zeromodal-btn-ok].zeromodal-btn.zeromodal-btn-primary"))
                    )
                    confirm_button.click()
                    print(f"已选课：{course_name}")
                    browser.quit()
                    exit(0)
            else:
                print("未找到课程信息")
                exit(1)
except BaseException as e:
    print(e)
