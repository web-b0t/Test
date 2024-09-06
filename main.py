from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
import time
import datetime
import review

def is_element_present(driver, element_id):
    try:
        driver.find_element(By.ID, element_id)
        return True
    except NoSuchElementException:
        return False

def recuperation_value(fichier_txt):
    with open(fichier_txt, 'r') as fichier:
        for ligne in fichier:
            if ligne[0] == "m":
                mail = ligne[5:].strip()
            elif ligne[0] == "p":
                pwd = ligne[4:].strip()
            elif ligne[0] == "n":
                numero = ligne[7:].strip()
    return mail, pwd, numero

def initialisation_navigateur():
    # Chemin relatif vers chromedriver.exe
    driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
    service = Service(driver_path)

    # Chemin vers l'extension VPN .crx (si nécessaire)
    extension_path = os.path.join(os.getcwd(), 'vpn.crx')

    # Configuration des options de Chrome
    options = webdriver.ChromeOptions()
    if os.path.exists(extension_path):
        options.add_extension(extension_path)

    # Initialisation du WebDriver avec les options
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def activation_vpn(driver, mail, pwd):
    # Parcourir toutes les fenêtres ouvertes par Chrome
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        current_url = driver.current_url
        print(f"URL actuelle : {current_url}")
        text_to_check = "setupvpn"
        
        # Vérifier si l'URL contient "setupvpn"
        if text_to_check in current_url:
            # Créer une nouvelle URL en modifiant les 12 premiers caractères
            new_url = current_url[:13] + ".setupvpn.com/ui/login"
            print(f"Navigation vers : {new_url}")
            driver.get(new_url)
            
            time.sleep(0.5)
            
            element = driver.find_element(By.CSS_SELECTOR, "a.ant-typography.css-zl9ks2")
            element.click()
            
            # Remplir un champ de texte
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
            text_field = driver.find_element(By.NAME, 'email')
            text_field.send_keys(mail)

            # Remplir un champ de mot de passe
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
            password_field = driver.find_element(By.NAME, 'password')
            password_field.send_keys(pwd)
            
            
            bouton = driver.find_elements(By.CLASS_NAME, 'ant-btn')
            bouton[1].click()
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-list-item-meta')))
            pays = driver.find_elements(By.CLASS_NAME, 'ant-list-item-meta')
            pays[random.randint(0,3)].click()
            
            
        else:
            # Fermer les fenêtres qui ne sont pas pertinentes
            driver.close()
    return 0

def radio_check_id(driver, id):
    if(is_element_present(driver,id)):
        case_a_cocher = driver.find_element(By.ID, id)
        if not case_a_cocher.is_selected():
            case_a_cocher.click()
    else:
        return 0

def borne(driver):
    value = str(random.randint(1,2))
    choix = "onf_q_feedback_m_where_did_you_eat_" + value
    radio_check_id(driver, choix)
    
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()
    
    if(value == "1"):
        choix = "onf_q_where_was_the_order_delivered_6"
        radio_check_id(driver, choix)
        
        time.sleep(0.5)
        
        bouton = driver.find_element(By.ID, 'buttonNext')
        bouton.click()

def commande_internet(driver):
    choix = "onf_q_where_was_the_order_delivered_" + str(random.choice([1,2,7]))
    print(choix)
    
    radio_check_id(driver, choix)
    
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()

def premiere_page(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'buttonBegin')))
    bouton = driver.find_element(By.ID, 'buttonBegin')
    bouton.click()
    
def deuxieme_page(driver):
    choix = "onf_q_mc_q_age_" + str(random.randint(2,4))
    radio_check_id(driver, choix)
    
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()
    
def troisieme_page(driver, numero):
    # Récupérer la date et l'heure actuelles
    now = datetime.datetime.now()

    current_day = str(now.day)
    if(len(current_day) == 1):
        current_day = "0"+current_day
        
    current_month = str(now.month)
    if(len(current_month) == 1):
        current_month = "0"+current_month
        
    current_year = str(now.year)

    jour = f"{current_day}/{current_month}/{current_year}"
    
    
    if(now.hour > 21):
        heure = str(random.choice(list(range(11, 14)) + list(range(19, 21))))
        
    elif(now.hour > 19):
        heure = str(random.choice(list(range(19, now.hour-1))))
            
    elif(now.hour > 14):
        heure = str(random.choice(list(range(11, 14))))
        
    elif(now.hour > 11):
        heure = str(random.choice(list(range(11, now.hour-1))))
    
    else:
        exit()
            
    minute = str(random.randint(0,59))
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'cal_q_mc_q_date')))
    jour_web = driver.find_element(By.NAME, 'cal_q_mc_q_date')
    jour_web.send_keys(jour)
    
    heure_web = driver.find_element(By.NAME, 'spl_rng_q_mc_q_hour')
    heure_web.send_keys(heure)
    
    minute_web = driver.find_element(By.NAME, 'spl_rng_q_mc_q_minute')
    minute_web.send_keys(minute)
    
    n_restaurant = driver.find_element(By.NAME, 'spl_rng_q_mc_q_idrestaurant')
    n_restaurant.send_keys(numero)
    
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()

def quatrieme_page(driver):
    value = str(random.choice([1,3,6]))
    choix = "onf_q_where_did_you_place_your_order_" + value
    radio_check_id(driver, choix)
    
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()
    
    if(value == "1"):
        time.sleep(random.randint(1,3))
        borne(driver)
        
    elif(value == "6"):
        time.sleep(random.randint(1,3))
        commande_internet(driver)

def cinquieme_page(driver,value):
    choix = "onf_q_feedback_m_based_upon_this_visit_to_this_6_1"
    radio_check_id(driver, choix)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'textarea_textarea')))
    jour_web = driver.find_element(By.CLASS_NAME, 'textarea_textarea')
    jour_web.send_keys(review.avis_page_5[value])
    
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()

def sixieme_page(driver):
    choix = "onf_q_mc_q_speed_service_1"
    radio_check_id(driver, choix)
    
    choix = "onf_q_mc_q_quality_of_food_and_drink_1"
    radio_check_id(driver, choix)
        
    choix = "onf_q_mc_q_friendliness_crew_1"
    radio_check_id(driver, choix)
        
    choix = "onf_q_mc_q_cleanliness_exterior_aspect_restaurant_1"
    radio_check_id(driver, choix)
    
    choix = "onf_q_feedback_m_the_exterior_aspect_of_the_res_1"
    radio_check_id(driver, choix)
        
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()

def septieme_page(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'onf_q_feedback_m_was_your_order_accurate_1')))
    
    choix = "onf_q_feedback_m_was_your_order_accurate_1"
    radio_check_id(driver, choix)
        
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()
    
def huitieme_page(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'onf_q_feedback_m_did_you_experience_a_problem_d_2')))
    
    choix = "onf_q_feedback_m_did_you_experience_a_problem_d_2"
    radio_check_id(driver, choix)
        
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonNext')
    bouton.click()
    
def neuvieme_page(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'onf_q_participation_loterie_2')))
    
    choix = "onf_q_participation_loterie_2"
    radio_check_id(driver, choix)
        
    time.sleep(0.5)
    
    bouton = driver.find_element(By.ID, 'buttonFinish')
    bouton.click()

def reponse_questionnaire(driver, value, numero):
    url = 'https://survey2.medallia.eu/?hellomcdo'
    driver.get(url)

    premiere_page(driver)
    time.sleep(random.randint(1,3))

    deuxieme_page(driver)
    time.sleep(random.randint(1,3))
    
    troisieme_page(driver, numero)
    time.sleep(random.randint(1,3))
    
    quatrieme_page(driver)
    time.sleep(random.randint(1,3))
    
    cinquieme_page(driver,value)
    time.sleep(random.randint(1,3))
    
    sixieme_page(driver)
    time.sleep(random.randint(1,3))
    
    septieme_page(driver)
    time.sleep(random.randint(1,3))
    
    huitieme_page(driver)
    time.sleep(random.randint(1,3))
    
    neuvieme_page(driver)
    time.sleep(random.randint(1,3))   

def main(nbr_review):
    mail, pwd, numero = recuperation_value("ID.txt")
    driver = initialisation_navigateur()
    while(len(driver.window_handles) != 2):
        time.sleep(0.05)
    time.sleep(5)
    activation_vpn(driver, mail, pwd)
    time.sleep(1)
    
    for i in range(nbr_review):
        avis = random.randint(0,len(review.avis_page_5)-1)
        
        reponse_questionnaire(driver, avis, numero)
        print(str(1+i) + ") " + str(avis))
        time.sleep(60)
    
    driver.quit()

main(15)