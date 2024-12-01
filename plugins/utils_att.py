from bs4 import BeautifulSoup
import requests
import random
import string
import pytz
from datetime import datetime
from plugins import db_connection as conn
from plugins.tools_att import DataStore, AttendeceTools

# Initialize global data stores and tools
att_tools = AttendeceTools()
sections = DataStore().sections
branches = DataStore().branches
imp_info = {}


def get_resp(date_obj, student: tuple) -> requests.Response:
    """
    Fetches attendance data from the college server.

    Args:
        date_obj: Current date object
        student: Tuple containing student information

    Returns:
        Response object containing attendance data
    """
    url = "http://103.203.175.90:94/attendance/attendanceTillTodayReport.php"
    imp_info["indian_time"] = date_obj

    # Headers required for the attendance server
    headers = {
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "http://103.203.175.90:94",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "http://103.203.175.90:94/attendance/attendanceTillADate.php",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": f'PHPSESSID={att_tools.token}',
        "Connection": "close",
    }

    # Format date for the request
    indian_time = imp_info["indian_time"]
    data = {
        "acadYear": "2024-25",
        "yearSem": "21",
        "branch": f"{student[2]}",
        "section": f"{student[1]}",
        "dateOfAttendance": f'{indian_time.day if len(str(indian_time.day)) == 2 else "0" + str(indian_time.day)}-{indian_time.month if len(str(indian_time.month)) == 2 else "0" + str(indian_time.month)}-{indian_time.year}',
    }

    return requests.post(url, headers=headers, data=data)


def get_data(rollno: str, realtime: bool = True) -> dict:
    """
    Retrieves and parses attendance data for a student.

    Args:
        rollno: Student's roll number
        realtime: If True, fetches fresh data; if False, uses cached data if available

    Returns:
        Dictionary containing parsed attendance information
    """
    student = conn.student_info_by_rollno(rollno)
    branch = branches[student[2].lower()].lower()
    section = student[1].lower()

    try:
        # Use cached data if available and realtime is False
        if not realtime and sections[branch][section] != "":
            html = sections[branch][section]
            print("Using cached data")
        else:
            date_obj = datetime.now(pytz.timezone("Asia/Kolkata"))
            resp_req = get_resp(date_obj, student)
            html = resp_req.text
            sections[branch][section] = html
            # print("Fetched fresh data")

        # Check if session expired and needs re-authentication
        if "<tr><td>User Name</td><td>:</td><td><input type=textbox name='username' id='username'" in html:
            att_tools.update_tok()
            return get_data(rollno, realtime)

        # Parse attendance data from HTML
        sections[section] = html
        soup = BeautifulSoup(html, "html.parser")
        tr_tag = soup.find("tr", {"id": f"{rollno}"})

        data = {}
        data["roll_number"] = tr_tag.find(
            "td", {"class": "tdRollNo"}).text.strip().replace(" ", "")
        td_percent_tag = tr_tag.find("td", {"class": "tdPercent"})
        data["attendance_percentage"] = td_percent_tag.contents[0].strip()
        data["total_classes"] = td_percent_tag.find("font").text.strip()

        # Extract subject-wise attendance
        subject_data = {
            td["title"]: td.text.strip()
            for td in tr_tag.find_all("td")
            if "title" in td.attrs
        }
        data.update(subject_data)

        trs = soup.find_all("tr")[2].find_all("td")[1:]
        l_st = [td.text.strip()[:5] for td in trs]

        data["date_up"] = l_st
        data["from"] = [branches[student[2]], student[1]]
        return data
    except Exception as e:
        print(f"Error fetching attendance data: {str(e)}")
        return {"error": "invalid roll number", "date_up": [], "from": []}
