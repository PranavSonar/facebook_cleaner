# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:57:13 2017

@author: pmullapudy
"""
#
import sys
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time as ti
#
class FacebookCleaner(object):
    """
    The main class to clean the facebook contents from activity log.
    """
    def __init__(self, clean_type):
        """
        Set up the FB Cleaner
        """
        self.clean_type = clean_type
        self.webdriver = webdriver
        self.browser = webdriver.Firefox()
#        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5)
        self.profile_name = None
        self.short_sleep_time = 1 # seconds to sleep
        self.medium_sleep_time = 3
        self.long_sleep_time = 10
    #
    def login(self, email, password):
        """
        Log in to Facebook
        """
        self.browser.get('https://www.facebook.com/login/')
        ti.sleep(self.medium_sleep_time)
        email_element = self.browser.find_element_by_id('email')
        email_element.send_keys(email)
        password_element = self.browser.find_element_by_id('pass')
        password_element.send_keys(password)
        password_element.submit()
        ti.sleep(self.medium_sleep_time)
        assert "Facebook" in self.browser.title
    #
    def get_profile_name(self):
        """
        Get the Profile Name
        """
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        profile_link = soup.find('a', {'title': 'Profile'})
        self.profile_name = profile_link.get('href')[25:]    # get from the link http://www.facebook.com/PROFILE
    #
    def get_your_posts_url(self):
        """
        get the URL of the activity log
        """
        your_posts_url = 'https://www.facebook.com/' + self.profile_name + "/allactivity?privacy_source=activity_log&log_filter=cluster_11"
        self.browser.get(your_posts_url)
        ti.sleep(self.medium_sleep_time)
    #
    def get_likes_url(self):
        """
        get the URL of the activity log
        """
        likes_url = 'https://www.facebook.com/' + self.profile_name + "/allactivity?privacy_source=activity_log&log_filter=likes"
        self.browser.get(likes_url)
        ti.sleep(self.medium_sleep_time)
    #
    def get_comments_url(self):
        """
        get the URL of the activity log
        """
        comments_url = 'https://www.facebook.com/' + self.profile_name + "/allactivity?privacy_source=activity_log&log_filter=cluster_116"
        self.browser.get(comments_url)
        ti.sleep(self.medium_sleep_time)
    #
    def check_element_exist(self):
        """
        Execute JS to scroll down until the menu element is present.
        returns True or False
        """
        counter_a = 0
        while counter_a < 100:
            counter_a = counter_a + 1
            self.browser.execute_script("window.scrollBy(0,500)", "")
            ti.sleep(self.medium_sleep_time)
            soup = BeautifulSoup(self.browser.page_source, "lxml")
            edit_menu_buttons = soup.find_all('a', {'aria-label': 'Edit'})
            if len(list(edit_menu_buttons)) > 0: # when it is greater than zero, it has picked up the Edit
                return True
            else:
                continue
        return False

    def scroll_down(self):
        """
        Scroll down such that x pages of Edit can be captured
        """
        counter_b = 0
        while counter_b <= 50: # try to scroll for Edit elements in x pages in one go
            counter_b = counter_b + 1
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            ti.sleep(self.medium_sleep_time)

    def clean_activity_log(self):
        """
        Clean all the post on the facebok activity log .On Click if there is  1) delete option or 2) Unlike/Remove Reaction or 3) Remove Tag . This ensures that friends are Not Unfriended !!!!!. All page likes will also be removed
        """
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        edit_menu_buttons = soup.find_all('a', {'aria-label': 'Edit'})
        #
        unlike_count = 0
        remove_reaction_count = 0
        del_count = 0
        #
        for item in range(0, len(list(edit_menu_buttons)) - 1):

            id_of_menu_element = edit_menu_buttons[item].get('id')
            menu_element = self.browser.find_element_by_id(id_of_menu_element)
            scrollElementIntoMiddle = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"  + "var elementTop = arguments[0].getBoundingClientRect().top;"  + "window.scrollBy(0, elementTop-(viewPortHeight/2));"; # scroll the element to centre of view
            self.browser.execute_script(scrollElementIntoMiddle, menu_element)
            ti.sleep(self.short_sleep_time)
            menu_element.click()
            ti.sleep(self.short_sleep_time)
            #
            if self.clean_type == 3:
                try:
                    tot_del_elements =  self.browser.find_elements_by_link_text('Delete')
                    ti.sleep(self.short_sleep_time)
                    del_element = tot_del_elements[item]
                    del_element.click()
                    ti.sleep(self.short_sleep_time)
                except:
                    pass
            else: #if self.clean_type == 3:
                pass
            #
            if self.clean_type == 2:
                try:
                    tot_unlike_elements = self.browser.find_elements_by_link_text('Unlike') ## shows up only after clicking the "Edit"
                    ti.sleep(self.short_sleep_time)
                    if len(tot_unlike_elements) > 0:
                        unlike_element = tot_unlike_elements[unlike_count]
                        unlike_count = unlike_count + 1
                        unlike_element.click()
                    else:
                        pass
                except:
                    pass
                #
                try:
                    tot_remove_reaction_elements = self.browser.find_elements_by_link_text('Remove Reaction') # shows up only after clicking the "Edit"
                    ti.sleep(self.short_sleep_time)
                    if len(tot_remove_reaction_elements) > 0:
                        reaction_element = tot_remove_reaction_elements[remove_reaction_count]
                        remove_reaction_count = remove_reaction_count + 1
                        reaction_element.click()
                    else:
                        pass
                except:
                    pass
            else: # if self.clean_type != 2:
                pass
            #
            if self.clean_type == 1:
                try:
                   tot_del_elements =  self.browser.find_elements_by_link_text('Delete')
                   ti.sleep(self.short_sleep_time)
                   del_element = tot_del_elements[del_count]
                   if del_element:
                       del_count = del_count + 1
                       del_element.click()
                       ti.sleep(self.short_sleep_time)
                       layer_confirm_element = self.browser.find_element_by_class_name('layerConfirm')
                       ti.sleep(self.short_sleep_time)
                       layer_confirm_element.click()
                       ti.sleep(self.medium_sleep_time)
                   else:
                       pass
                except:
                    pass
            else: #if self.clean_type != 1
                pass
            #
            self.webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform() # handle the popup's


    #
if __name__ == '__main__':
    """
    Main section
    """
    #
    print (" [1]: Clean 'Your Posts' in Activity Log \n [2]: Clean 'Likes' in Activity Log \n [3]: Clean 'Comments' in Activity Log")
    print("..")
    #
    user_input = input("Choose the Facebook Clean Type that u want to perform (1/2/3) : ")
    try:
        clean_type = int(user_input)
    except:
        print ("enter a valid Integer 1, 2 or 3 ")
        quit()
    #
    if (clean_type == 1) | (clean_type == 2) | (clean_type == 3):
        pass
    else:
        print ("sorry bhai !!!")
        quit()
    #

    #get email and password
    email = input("Please enter Facebook login email: ")
    password = getpass.getpass()
    #
    cleaner = FacebookCleaner(clean_type=clean_type)
    #
    cleaner.login(email=email, password=password)
    cleaner.get_profile_name()

    if clean_type == 1:
        cleaner.get_your_posts_url()
    elif clean_type == 2:
        cleaner.get_likes_url()
    elif clean_type == 3:
        cleaner.get_comments_url()

    element_exists = cleaner.check_element_exist()
    if element_exists:
        cleaner.scroll_down()
    else:
        print ("the element Edit does not exist")
        sys.exit()
    #
    cleaner.clean_activity_log()