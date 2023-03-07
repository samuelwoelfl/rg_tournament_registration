from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys



##################################################################################
# ---------------------------- Insert data in script ---------------------------- #
##################################################################################

# set to 'TEST' to test the bot without registering in the end (therefore you need to select a tournament and division that is open for registration or waiting list
# set to 'RUN' if the bot should complete the registration
mode = 'TEST'

# sets how many seconds the bot will wait at maximum for a page to load - set higher if your internet is slow
delay = 4

# roundnet germany login data
rg_username = 'maxmustermann'  # 'maxmustermann'
rg_password = 'asdbu823l2'  # 'asdbu823l2'

# tournament and team specific data
link_to_tournament = 'https://playerzone.roundnetgermany.de/tournaments/208-2023-04-01-springclash-2023'  # 'https://playerzone.roundnetgermany.de/tournaments/208-2023-04-01-springclash-2023'
division = 'Intermediate Mixed'  # 'Intermediate Mixed'
teamname = 'Kreativer Teamname'  # 'Kreativer Teamname'
teammate_prename = 'Herbert'  # 'Herbert'
teammate_name = 'Müller'  # 'Müller'
teammate_rg_id = 'ABC1234'  # 'ABC1234'
own_skilllevel = 'Intermediate'  # 'Intermediate'



##################################################################################
# ----------------------------- helper functions ------------------------------- #
##################################################################################

def scroll_down():
    body = bot.find_element(By.CSS_SELECTOR, "body")
    body.send_keys(Keys.END)
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        bot.find_element(By.CSS_SELECTOR, "#content").send_keys(Keys.END)
    except:
        pass



##################################################################################
# ----------------------- load page and accept cookies ------------------------- #
##################################################################################

bot = webdriver.Firefox()
bot.get(link_to_tournament)
try:
    elem = WebDriverWait(bot, delay).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.cc-compliance a.cc-btn.cc-dismiss')))
except TimeoutException:
    print(f'Page loading took to much time - increase delay to give the browser more time. Otherwise there could be an error message from roundnet germany, you will see this as a callout message at the top of the page')
    exit()
cookie_accept_button = bot.find_element(By.CSS_SELECTOR, '.cc-compliance a.cc-btn.cc-dismiss')
cookie_accept_button.click()
#bot.maximize_window()



##################################################################################
# -------------------------- set language to german ---------------------------- #
##################################################################################

language_selector = bot.find_element(By.CSS_SELECTOR, 'a[href="#switchlanguage"]')
language_selector.click()
dropdown_input_lang = bot.find_element(By.CSS_SELECTOR, ".modal#switchlanguage input.select-dropdown")
dropdown_input_lang.click()
dropdown_options_lang = bot.find_elements(By.CSS_SELECTOR, "ul.dropdown-content li")

for o in dropdown_options_lang:
    option_html = o.get_attribute("innerHTML")
    if "Deutsch (de)" in option_html:
        o.click()

submit_button_lang = bot.find_element(By.CSS_SELECTOR, '.modal#switchlanguage input[type="submit"]')
submit_button_lang.click()



##################################################################################
# ----------------- find registration link for wanted division ----------------- #
##################################################################################

register_section = bot.find_element(By.XPATH, "//h4[text()='Anmeldung']/../../../following-sibling::div[@class='row']")
divisions_section = register_section.find_element(By.XPATH, "/descendant::ul[@class='collapsible']")
divisions_list = divisions_section.find_elements(By.CSS_SELECTOR, "li")

# search for wanted division
division_number = -1
for i, d in enumerate(divisions_list):
    name = d.find_element(By.CSS_SELECTOR, "div.col b").get_attribute("innerHTML")
    if name.lower() == division.lower():
        division_number = i


# print if wanted division got found
if division_number >= 0:
    print(f"Division '{division}' found!")
else:
    print(f"Divison '{division}' not fround in this tournament. Please make sure it's spelled correct")
    exit()

# get registration link for wanted division
register_button = divisions_list[division_number].find_element(By.CSS_SELECTOR, "div div.col:last-child a")
register_link = register_button.get_attribute("href")



##################################################################################
# ------------------------- login to roundnet germany -------------------------- #
##################################################################################

# open register link that will ask for login
bot.get(register_link)
# wait for page to load
try:
    elem = WebDriverWait(bot, delay).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input#id_username')))
except:
    print('Page loading took to much time - increase delay to give the browser more time. Otherwise there could be an error message from roundnet germany, you will see this as a callout message at the top of the page')
    exit()
# find input fields and submit button
username_input = bot.find_element(By.CSS_SELECTOR, "input#id_username")
password_input = bot.find_element(By.CSS_SELECTOR, "input#id_password")
submit_button_login = bot.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
# fill input fields and click submit button
username_input.clear()
username_input.send_keys(rg_username)
password_input.clear()
password_input.send_keys(rg_password)
submit_button_login.click()

# check success
try:
    elem = WebDriverWait(bot, delay).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'a.nav-profile-img')))
except:
    print("Login not possible, please check your login credentials for the Playerzone. Otherwise it could be that the page loading took too long or there's an error message from roundnet germany at the page.")
    exit()

print("Successfully logged in")



##################################################################################
# ---------------------- reload till registration is open ---------------------- #
##################################################################################

registration_open = False
reload_count = 0
while registration_open is False:
    bot.get(register_link)

    try:
        registration_form = bot.find_element(By.CSS_SELECTOR, 'div.reg-form')
        registration_open = True
    except:
        if reload_count == 0:
            print("Registration is closed. Reloading until registration opens...")
        elif reload_count % 10 == 0:
            print("still waiting...")

        try:
            elem = WebDriverWait(bot, delay).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, 'a.nav-profile-img')))
        except TimeoutException:
            print('Page loading took to much time - increase delay to give the browser more time. Otherwise there could be an error message from roundnet germany, you will see this as a callout message at the top of the page')
        bot.refresh()
        reload_count += 1

print('Registration is open! Starting to register.')



##################################################################################
# -------------------------------- register ------------------------------------ #
##################################################################################

# find input fields and submit button
teammate_rg_id_input = bot.find_element(By.CSS_SELECTOR, "input#id_teammate_rg_id")
teammate_name_input = bot.find_element(By.CSS_SELECTOR, "input#id_teammate_secret")
teamname_input = bot.find_element(By.CSS_SELECTOR, "input#id_team_name")
skill_container = bot.find_element(By.CSS_SELECTOR, "#id_skill_container")
skill_input = skill_container.find_element(By.CSS_SELECTOR, "input.select-dropdown.dropdown-trigger")
submit_button_registration = bot.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

# fill input fields
teammate_rg_id_input.clear()
teammate_rg_id_input.send_keys(teammate_rg_id)
teammate_name_input.clear()
teammate_name_input.send_keys(f'{teammate_prename} {teammate_name}')
teamname_input.clear()
teamname_input.send_keys(teamname)

# fill skill select
scroll_down()
skill_input.click()
scroll_down()
dropdown_content = skill_container.find_element(By.CSS_SELECTOR, "ul.dropdown-content")
dropdown_options = dropdown_content.find_elements(By.CSS_SELECTOR, "li")
for o in dropdown_options:
    option_html = o.get_attribute("innerHTML")
    if own_skilllevel in option_html:
        o.click()

scroll_down()

# click submit button
submit_button_registration.click()

# wait for confirm page to load
try:
    elem = WebDriverWait(bot, delay).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'label.switch')))
except:
    print('Page loading took to much time - increase delay to give the browser more time. Otherwise there could be an error message from roundnet germany, you will see this as a callout message at the top of the page')
    exit()

# click image rights toggle
switch_image_rights = bot.find_element(By.CSS_SELECTOR, "label.switch")
switch_image_rights.click()

# click final button if in RUN mode
confirm_button = bot.find_element(By.CSS_SELECTOR, "a#confirm-button")
if mode == 'RUN':
    confirm_button.click()
    print("Registration done")
else:
    print("Test successfully done")

bot.close()
bot.quit()
