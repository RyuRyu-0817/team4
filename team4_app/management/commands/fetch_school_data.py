# import requests
# from django.core.management.base import BaseCommand
# from team4_app.models import School  # モデルをインポート

# class Command(BaseCommand):
#     help = 'Fetch school data from API and save to database'

#     def handle(self, *args, **kwargs):
#         url = "https://api.edu-data.jp/api/v1/school"
#         headers = {
#             'Authorization': 'Bearer 336|pCFc2QKRNIGiKKOjnRG45ehuh1rZzM98GCVh8k50'
#         }
#         params = {'school_type_code': 'D1'}

#         response = requests.get(url, headers=headers, params=params)
#         if response.status_code == 200:
#             school_data = response.json().get('schools', {}).get('data', [])
            
#             for school in school_data:
#                 # データを保存
#                 School.objects.get_or_create(
#                     name=school['school_name']                    
#                 )
#             self.stdout.write(self.style.SUCCESS('School data successfully saved!'))
#         else:
#             self.stdout.write(self.style.ERROR('Failed to fetch data from API'))

import requests
from django.core.management.base import BaseCommand
from team4_app.models import School  # モデルをインポート

class Command(BaseCommand):
    help = 'Fetch all school data from API and save to database'

    def handle(self, *args, **kwargs):
        url = "https://api.edu-data.jp/api/v1/school"
        headers = {
            'Authorization': 'Bearer 336|pCFc2QKRNIGiKKOjnRG45ehuh1rZzM98GCVh8k50'
        }
        params = {'school_type_code': 'D1'}

        while url:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                # APIレスポンスのJSONデータから学校情報を取得
                school_data = response.json().get('schools', {}).get('data', [])
                
                # 各学校データを保存
                for school in school_data:
                    School.objects.get_or_create(
                        name=school['school_name']
                    )
                                
                url = response.json().get('schools', {}).get('next_page_url')
                if url:                
                    self.stdout.write(self.style.SUCCESS(f"Fetched next page: {url}"))
                else:                    
                    self.stdout.write(self.style.SUCCESS('No more pages to fetch.'))
                    break
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch data from API'))
                break
        
        self.stdout.write(self.style.SUCCESS('All school data successfully saved!'))
