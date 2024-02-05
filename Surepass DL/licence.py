import requests
from lxml import html
from PIL import Image
from io import BytesIO

class DrivingLicenseScraper:
    def __init__(self, dl_number, dob):
        self.dl_number = dl_number
        self.dob = dob
        self.base_url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"
        self.session = requests.Session()

    def fetch_captcha(self):
        captcha_url = "https://parivahan.gov.in/rcdlstatus/captcha.png"  
        response = self.session.get(captcha_url, stream=True)

        if response.status_code == 200:
            captcha_image = Image.open(BytesIO(response.content))
            captcha_image.show()
            return captcha_image
        else:
            print(f"Failed to fetch CAPTCHA image. Status code: {response.status_code}")
            return None

    def get_captcha_input(self):
        return input("Enter the CAPTCHA value: ")

    def scrape_data(self):
        captcha_image = self.fetch_captcha()
        captcha_input = self.get_captcha_input()

        payload = {
            'dl_number': self.dl_number,
            'dob': self.dob,
            'txtCaptcha': captcha_input,
        }

        response = self.session.post(self.base_url, data=payload)

        if response.status_code == 200:
            tree = html.fromstring(response.content)

            current_status = tree.xpath("//span[@id='lblRC_Status']/text()")
            holder_name = tree.xpath("//span[@id='lblHolderName']/text()")
            ratings = tree.xpath("//span[@id='lblBadge']/text()")
            

            data_json = {
                'current_status': current_status[0] if current_status else None,
                'holder_name': holder_name[0] if holder_name else None,
                'ratings': ratings[0] if ratings else None,
                
            }

            return data_json
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

if __name__ == "__main__":
    dl_number = input("Enter Driving License Number: ")
    dob = input("Enter Date of Birth (DD-MM-YYYY): ")

    scraper = DrivingLicenseScraper(dl_number, dob)
    scraped_data = scraper.scrape_data()

    print(scraped_data)
