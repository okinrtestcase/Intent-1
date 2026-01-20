import time
from module import modul, envwebchat, envstatus, envfile, envreport, envfolder
from module.modul import log_function_status
import re



@log_function_status
def actions(driver, json_data, report_filename, id_test, time, today, tester_name, url, title_page, browser_name, browser, greeting, name, email, phone):
    # duration start test
    start = modul.start_time()
    
    
    class_name = "message-content-wrapper"
    content = "content"

    title = "Reading sample_text and send to webchat"
    modul.show_loading(title)

    # calculate total intent
    count_per_element_intent = [sum(1 for key in item.keys() if key.startswith("intent_name")) for item in json_data]
    intent_counter = sum(count_per_element_intent)

    # calculate total sample_text
    count_per_element_sample_text = [sum(1 for key in item.keys() if key.startswith("sample_text")) for item in json_data]
    sample_text_count = sum(count_per_element_sample_text)

    # Initiate Intent Count
    intent_count = 0

    for element in json_data:
        # refresh browser
        modul.refresh(driver)
        modul.wait_time(3)
        
        # calculate duration per intent
        duration_perintent = modul.start_time()
        total_duration_perintent = []

        # animation change intent
        modul.show_loading(element["intent_name"])

        # loop sampletext
        for key, value in element.items():
            # read sample text
            if key.startswith("sample_text") and value is not None and value != "":
                # duration per sample text
                count = int(key.split("sample_text")[1])

                duration_persampletext = modul.start_time()

                sample_text = value
                envwebchat.send_message(driver, sample_text)
                envwebchat.wait_reply(driver, class_name, content, sample_text)
                
                # Refresh browser setiap kelipatan sample text 2
                if count % 2 == 0:
                    modul.wait_time(2)
                    modul.refresh(driver)

                # take screenshot
                image_capture = envreport.take_screenshot(driver, id_test, key, sample_text)
                image_capture = image_capture.replace('report/', '')
                print(image_capture)
                
            
                # get reply bot
                respond_bot = envwebchat.get_reply_chat(driver, class_name, content, sample_text, message_content="message-content")
                respond_bot = "\n".join(respond_bot).strip()
                respond_bot = envstatus.respond_bot_correction(respond_bot)
                

                # get response csv
                respond_csv = str(element["respond"]).strip()
                respond_csv = envstatus.respond_csv_correction(respond_csv)
                

                # end_duration_persampletext
                end_duration_persampletext = modul.end_time(duration_persampletext)

                # checking comparation string
                compare_strings = envstatus.compare_strings(respond_bot, respond_csv)
                
                # checking different word
                diff_strings = envstatus.diff_strings(respond_bot, respond_csv)

                # checking score probability
                probability = envstatus.probability(respond_bot, respond_csv)

                # checking status
                status = envstatus.status(probability)
                
                # animation wait done per sample text
                title = f"{key} : {sample_text}"
                modul.show_loading_sampletext(title)

                data_bot = {
                        "no": key,
                        "id": element["id"],
                        "parent_id": element["parent_id"],
                        "intent_name": element["intent_name"],
                        "sample_text": sample_text,
                        "respond_text": respond_csv,
                        "response_bot": respond_bot,
                        "status": status,
                        "probability": probability,
                        "diff_strings": diff_strings,
                        "compare_result": compare_strings,
                        "duration": end_duration_persampletext,
                        "image_capture": image_capture
                    }
                
                # write json file to save data_text
                envfile.write_json_data_bot(data_bot, report_filename, id_test)

                # calculating status pass/failed
                pass_count, failed_count = envstatus.calculate(report_filename, id_test)

                data_summary = {
                    "id_test" : id_test,
                    "tester_name" : tester_name,
                    "url" : url,
                    "page_name" : title_page,
                    "browser_name" : browser_name,
                    "date_test" : today,
                    "start_time_test" : time,
                    "total_intent" : intent_count,
                    "total_sampletext" : sample_text_count,
                    "success" : pass_count,
                    "failed" : failed_count
                }

                # write json file to save data_summary
                envfile.write_json_data_summary(data_summary, report_filename, id_test)
                
                # Generate Report
                envreport.report_action(report_filename, id_test)
                
            else:
                continue
            
        
        # end_duration_perintent 
        end_duration_perintent = modul.end_time(duration_perintent)

        chart = {
            element["intent_name"] : end_duration_perintent
        }

        # write json file to save data_chart
        envfile.write_json_chart(chart, report_filename, id_test)

        print("\n")
        print("Total duration intent", element["intent_name"], " : ", end_duration_perintent, "\n")
        
        intent_count += 1
        browser = False
        if intent_count % 1 == 0 and intent_count != len(json_data):
            greeting = "Hai"
            name = "Tester Props"
            email = "tester.props@gmail.com"
            phone = "08999999999"
            browser = "chrome"
            
            modul.close_browser(driver)
            
            # Buka browser baru
            driver, title_page, browser_name = modul.read_browser(url, browser)
            envwebchat.prechat_form(driver, greeting, name, email, phone)
            browser = True
        elif intent_count == len(json_data):
            if browser == True:
                print("Continous Intent Test")
                modul.close_browser(driver)
                break
            else:
                print("Last Intent")
                modul.close_browser(driver)
                continue
        else:
            continue

    
    duration_test = modul.end_time(start)

    data_summary = {
                "id_test" : id_test,
                "tester_name" : tester_name,
                "url" : url,
                "page_name" : title_page,
                "date_test" : today,
                "start_time_test" : time,
                "total_intent" : intent_counter,
                "total_sampletext" : sample_text_count,
                "duration": duration_test,
                "success" : pass_count,
                "failed" : failed_count
            }
    
    # write json file to save data_summary
    envfile.write_json_data_summary(data_summary, report_filename, id_test)


    # total_duration_perintent.append(end_duration_perintent)
    # print("Total duration all intent", total_duration_perintent)