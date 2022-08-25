
import os
import json
from this import d
import time
import requests
from xlwt import Workbook
from xlrd import open_workbook
from datetime import datetime, timedelta
from xlutils.copy import copy
from os import path
import logging
import logger_setup
logger = logger_setup.setup_logger(__name__,'app.log')
class LiveChatUtils:

    def __init__(self, config):
        self.config = config
    
    def generate_chat_history_excel(self, file_path):
        
        test_wb = Workbook()
        sheet = test_wb.add_sheet("Sheet1")
        
        sheet.write(0, 0, "Date")
        sheet.write(0, 1, "Customer Name")
        sheet.write(0, 2, "Mobile Number")
        sheet.write(0, 3, "Email")
        sheet.write(0, 4, "Web-Chat Feedback")
        sheet.write(0, 5, "Interaction Start Date-Time")
        sheet.write(0, 6, "Interaction End Date-Time")
        sheet.write(0, 7, "Interaction Duration")
        sheet.write(0, 8, "Category")
        sheet.write(0, 9, "Agent Name")
        sheet.write(0, 10, "User ID")
        sheet.write(0, 11, "Channel")
        sheet.write(0, 12, "Session ID")
        sheet.write(0, 13, "Wait Time")
        sheet.write(0, 14, "Chat Termination")  
        
        test_wb.save(file_path)
    
    def add_chat_history_report(self, file_path, data):
        
        rb = open_workbook(file_path,formatting_info=True)
        r_sheet = rb.sheet_by_index(0) 
        r = r_sheet.nrows
        wb = copy(rb) 
        sheet = wb.get_sheet(0)
            
        sheet.write(r, 0, data["joined_date"])
        sheet.write(r, 1, data["customer_name"])
        sheet.write(r, 2, data["phone"])
        sheet.write(r, 3, data["email"])
        sheet.write(r, 4, data["rate_value"])
        sheet.write(r, 5, data["start_time"])
        sheet.write(r, 6, data["end_time"])
        sheet.write(r, 7, data["chat_duration"])
        sheet.write(r, 8, data["closing_category"])
        sheet.write(r, 9, data["agent_name"])
        sheet.write(r, 10, data["agent_username"])
        sheet.write(r, 11, data["channel_name"])
        sheet.write(r, 12, data["session_id"])
        sheet.write(r, 13, data["wait_time"])
        sheet.write(r, 14, data["chat_ended_by"])
        wb.save(file_path)
         
    def generate_chat_history_report(self, data):
        
        logger.info("inside generate_chat_history_report")

        parent_user = data["parent_user"] 
        second_user =data["second_user"] 
        
        today = datetime.now()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_path = os.path.join(BASE_DIR, 'files/')
        
        if not os.path.exists(base_path + 'livechat-chat-history/' + str(parent_user)):
                os.makedirs(base_path + 'livechat-chat-history/' +
                                str(parent_user))
                
        if parent_user!="None":
            file_path = "livechat-chat-history/" + \
                    str(parent_user) + "/chat_history_" + \
                    str(today.date()) + ".xls"
                  
            if not os.path.exists(base_path + file_path):
                try:
                    self.generate_chat_history_excel(base_path + file_path)
                except Exception as e:
                    logger.error(e)
            
            try:
                self.add_chat_history_report(base_path + file_path, data)
                
            except Exception as e:
                logger.error(e)
            
        if second_user!="None":

            file_path = "livechat-chat-history/" + \
                    str(second_user) + "/chat_history_" + \
                    str(today.date()) + ".xls"
            if not os.path.exists(base_path + 'livechat-chat-history/' + str(second_user)):
                os.makedirs(base_path + 'livechat-chat-history/' +
                                str(second_user))
            
            if not os.path.exists(base_path + file_path): 
                try:
                    self.generate_chat_history_excel(base_path + file_path)
                except Exception as e:
                    logger.error(e)
                
            try:
                self.add_chat_history_report(base_path + file_path, data)
            except Exception as e:
                logger.error(e)
            
            
    def generate_chat_history_test_report(self, data):
        
        logger.info("inside generate_chat_history_test_report")

        today = datetime.now()
        current_time = today.strftime("%H:%M:%S")
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_path = os.path.join(BASE_DIR, 'files/')
        
        if not os.path.exists(base_path + 'livechat-chat-history/' + str("testing")):
            os.makedirs(base_path + 'livechat-chat-history/' +
                                str("testing"))
        
        file_path = "livechat-chat-history/" + \
                    str("testing") + "/chat_history_" + \
                    str(today.date()) + ".xls"

        if not os.path.exists(base_path + file_path):

            test_wb = Workbook()

            sheet1 = test_wb.add_sheet("Sheet1")

            sheet1.write(0, 0, "index")
            sheet1.write(0, 1, "username")
            
            test_wb.save(base_path + file_path)
                
        rb = open_workbook(base_path + file_path,formatting_info=True)
        r_sheet = rb.sheet_by_index(0) 
        r = r_sheet.nrows
        wb = copy(rb) 
        sheet = wb.get_sheet(0) 
        try:
            sheet.write(r, 0, data["index"])
            sheet.write(r, 1, data["username"])
        except Exception as e:
            logger.error(e)
        
        wb.save(base_path + file_path)
            
        
    def generate_livechat_report(self, data):
        logger.info("inside generate_livechat_report")
        response = {}
        try:
            if data["type"] == "ChatHistoryReport":
                self.generate_chat_history_report(data)
            if data["type"] == "ChatHistoryReportTesting":
                self.generate_chat_history_test_report(data)
        except Exception as e:
            response = {}
            logger.error(e)

        return response

    def request_to_assign_livechat_customer_to_agent(self, data):
        response_data = {}
        logger.info("inside request_to_assign_livechat_customer_to_agent")
        try:
            request_start_time = time.time()
            url = self.config["LIVECHAT_SERVER_HOST"] + "/livechat/assign-livechat-agent/"
            response = requests.post(url=url, data=json.dumps({}), headers={"Content-Type": "application/json"}, timeout=5)
            response_data = json.loads(response.text)
            request_time_taken = round(time.time() - request_start_time, 3)
        except Exception as e:
            response_data = {}

        return response_data
