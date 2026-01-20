from jinja2 import Environment, FileSystemLoader
import json
from colorama import Fore, Style
from module import modul, envfolder
import os
from datetime import datetime
import re


def report(report_filename, id_test):
    report_filename = f"{report_filename}-{id_test}"
    result_path = envfolder.report_html(report_filename)

    # Animasi Generate Report Proses
    title = f"Generating report on process.. "
    modul.show_loading(title)
    
    # file name of report
    file_json_report = envfolder.write_json_data_bot(report_filename)
    
    try:
        with open(file_json_report, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Load Jinja2 template
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('report/template/uhuy.html')

        # Render the template with data
        html_output = template.render(summary=data['summary'], chart=data['chart'], test_data=data['data'])

        # Save the rendered HTML to a file
        with open(result_path, 'w', encoding='utf-8') as output_file:
            output_file.write(html_output)
        print("HTML report generated successfully.", "\n")    
    except FileNotFoundError as e:
        print(Fore.RED + "File JSON tidak ditemukan:", str(e) + Style.RESET_ALL, "\n")
        raise
    except Exception as e:
        print(Fore.RED + "Terjadi kesalahan saat membuat report:", str(e) + Style.RESET_ALL, "\n")
        raise
    
def report_action(report_filename, id_test):
    report_filename = f"{report_filename}-{id_test}"
    result_path = envfolder.report_html(report_filename)

    # file name of report
    file_json_report = envfolder.write_json_data_bot(report_filename)
    
    try:
        with open(file_json_report, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Load Jinja2 template
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('report/template/uhuy.html')

        # Render the template with data
        html_output = template.render(summary=data['summary'], chart=data['chart'], test_data=data['data'])

        # Save the rendered HTML to a file
        with open(result_path, 'w', encoding='utf-8') as output_file:
            output_file.write(html_output)
    except FileNotFoundError as e:
        print(Fore.RED + "File JSON tidak ditemukan:", str(e) + Style.RESET_ALL)
        raise
    except Exception as e:
        print(Fore.RED + "Terjadi kesalahan saat membuat report:", str(e) + Style.RESET_ALL)
        raise
    
    
def take_screenshot(driver, id_test, key, sample_text):
    # Hilangkan simbol dan spasi akhir
    # sample_text = sample_text.replace(" ", "")
    sample_text = re.sub(r'[^\w\s]', '', sample_text)
    sample_text = re.sub(r'\s+', ' ', sample_text)
    sample_text = sample_text.strip()

    # folder screenshot
    result_path = envfolder.report_screenshoot(id_test)
    result_filename = f'{result_path}/{sample_text}.png'
    
    # take screenshot
    try:
        modul.wait_time(1.5)
        success = driver.save_screenshot(result_filename)
        modul.wait_time(1)
        if success:
            print(f"{key} hass been captured!")
        else:
            print(Fore.RED + f"{key} failed to captured!", str(e) + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error save capture because: {e}", str(e) + Style.RESET_ALL)
    
    return result_filename