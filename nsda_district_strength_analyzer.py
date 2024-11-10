import json
import requests


def main(
    cookies,
):
    base_uri = "https://api.speechanddebate.org/v2/reports/"
    district_num = "96"  # 96 = Virginia  # 11 is West Los Angeles (CA) # "4"  # 4 is Big Valley (CA)
    starting_year = "2003"
    year = starting_year
    school_output_rows = []
    overall_output_rows = []
    school_sum_of_strength_over_time_dict = {}

    # TODO - auto-update end-year
    while year < "2025":
        year_str = 0
        uri = base_uri + "largest-schools?district=" + district_num + "&year=" + year

        response = requests.get(uri, cookies=cookies)
        school_obj_list = json.loads(response.content.decode("utf-8")).get("data")
        for school_obj in school_obj_list:
            school = school_obj.get("School")
            try:
                strength = int(school_obj.get("Strength"))
            except TypeError:
                strength = 0
            year_str = year_str + strength
            school_output_rows.append([school, year, strength])
            if school not in school_sum_of_strength_over_time_dict:
                school_sum_of_strength_over_time_dict[school] = strength
            else:
                school_sum_of_strength_over_time_dict[school] += strength

        overall_output_rows.append([year, year_str])
        year = str(int(year) + 1)

    # Write each to a CSV
    with open(f"district_{district_num}_school_strength_over_time.csv", "w") as f:
        f.write("School, Year, Strength, Sum_of_School_Strengths\n")
        for row in school_output_rows:
            row.append(
                school_sum_of_strength_over_time_dict[row[0]]
            )  # Add strength sum column
            f.write(",".join([str(x) for x in row]) + "\n")
    with open(f"district_{district_num}_overall_strength_over_time.csv", "w") as f:
        f.write("Year, Strength\n")
        for row in overall_output_rows:
            f.write(", ".join([str(x) for x in row]) + "\n")


if __name__ == "__main__":
    # This data is viewable in Developer -> Network -> Headers -> Request Headers -> Cookie
    cookies = {
        "nsda_api_session_token": "", # ADD IT HERE!
        "nsda_person_id": "",
        "nsda_roles": "",
        "nsda_username": "", # should be your email
    }
    main(cookies=cookies)
