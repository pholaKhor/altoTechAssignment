call .\env\Scripts\activate.bat
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install pymongo
pip install openai
cd hotels
python manage.py migrate
python manage.py loaddata users/fixtures/user_permission_1.json
cmd /k