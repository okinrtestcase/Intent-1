from module import modul, envfile, envwebchat, action, envreport
import time

def main():
    """ Initialize.... """
    modul.initialize("Initialize ...")

    """ Time Starting.. """
    today, time = modul.todays()
    start = modul.start_time()
    id_test = modul.id_test()

    # report name
    report_filename = "Test Intent Bank Jakarta - Part 02"
    # Logging
    modul.setup_logging(report_filename, id_test)

    print("Test ID : ", id_test, "\n")
    print("Day : ", today)
    print("Start Time : ", time, "\n")

    """ URL/s Test Area """
    # url = "https://chat.botika.online/K7xgbwv" #POC BPJS Kes
    # url = "https://chat.botika.online/tOvxkD2" # Central Park
    # url = "https://chat.botika.online/AhTzwr8" #Suzuki
    # url = "https://chat.botika.online/zDticmq" #Suzuki1
    # url = "https://chat.botika.online/Iwel50K" #UPN
    # url = "https://chat.botika.online/umZ3b2x"
    # url = "https://chat.botika.online/umZ3b2x" # Pos Indonesia
    # url = "https://chat.botika.online/zDticmq" # Bank DKI
    # url = "https://chat.botika.online/TF00WgP" # Bank DKI
    # url = "https://chat.botika.online/AhTzwr8" # 3KIOSK DEV
    # url = "https://chat.botika.online/c73kOrB" # BRINS DEV
    # url = "https://chat.botika.online/venKwFV?newMessage=chat%20Started&attachment=false&auth=JiQSg8PEZ%2FLCT964dTazyOuehjLUbzKxJUmXjMk9AJgB2tKyrbEy2IfktoPYa4BpTDryrmQb%2BtVE9sX0NlfpDmcVu48%3D&header=hidden&history=false"
    # url = "https://chat.botika.online/cCTRReh" # Name
    # url = "https://chat.botika.online/MAZl5se" # Phone
    # url = "https://chat.botika.online/ImrptvB" # Email
    # url = "https://chat.botika.online/Zx0gx0t" # All
    # url = "https://chat.botika.online/4J2xVuy" # Asuransi Tugu
    # url = "https://chat.botika.online/L0bBAca" # POC Garuda
    # url = "https://chat.botika.online/qdQgoYH" # SMM
    url = "https://chat.botika.online/TF00WgP" # Bank DKI Dev

    """ Filename Assets """
    csv_file  = "bankjakarta-02"
    json_file = "bankjakarta-02"
    

    """ Detail of test """
    tester_name = modul.tester("Ahmad Nur Brasta")
    greeting = "Hai"
    name = "Tester Props"
    email = "tester.props@gmail.com"
    phone = "08999999999"
    
    """" Choose Browser """
    browser = "chrome"
    # browser = "edge"
    # browser = "firefox"

    """ Convert CSV to JSON """
    envfile.convert(csv_file, json_file)

    """ Read JSON """
    json_data = envfile.read_json(json_file)

    """ Read Browser """
    driver, title_page, browser_name = modul.read_browser(url, browser)

    """ Check Available Pre-chat Form """
    envwebchat.prechat_form(driver, greeting, name, email, phone)

    """ Action Run """
    action.actions(driver, json_data, report_filename, id_test, time, today, tester_name, url, title_page, browser_name, browser, greeting, name, email, phone)
    
    """ Generate Report """
    envreport.report(report_filename, id_test)

    end = modul.end_time(start)
    today, time = modul.todays()
    print("End Time : ", time)
    print("Duration : ", end, "\n")
    
    # Write End Time And Duration Summary
    envfile.write_end_time_summary(time, end, report_filename, id_test)
    
    modul.test_done("Test  Done!")
    print("Thank you, Have a great day!😎 \n")

if __name__ == "__main__": 
    main()