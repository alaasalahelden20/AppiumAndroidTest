from django.shortcuts import render
from .models import App
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import App
from .forms import AppForm
from django.conf import settings

import base64
import os
import subprocess
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

from selenium.webdriver.support.ui import WebDriverWait


# Load environment variables from .env file
load_dotenv()


automation_name = os.getenv('APPIUM_AUTOMATION_NAME')
deviceName=os.getenv('deviceName')
platformName=os.getenv('platformName')
class AppiumTestCase(unittest.TestCase):
    def __init__(self, apk_path,app_instance):
        self.apk_path = apk_path
        self.app_instance = app_instance  # Store the passed app instance
        self.driver = None

    def setUp(self) -> None:
        capabilities = dict(
            platformName='Android',
            automationName=automation_name,
            deviceName=deviceName,
            uiautomator2ServerLaunchTimeout=100000,
            newCommandTimeout=100000,
            app=self.apk_path 
        )
        try:
            appium_server_url = 'http://host.docker.internal:4723'
            time.sleep(30)  # Allow the app to load

            self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
            time.sleep(70)  # Allow the app to load
            print("Driver initialized successfully")
        except Exception as e:
            print(f"Failed to initialize driver: {e}")
            raise



    def tearDown(self) -> None:
        if self.driver:
            try:
                if self.driver:
                    self.driver.quit()
            except Exception as e:
                print(f"Error during tearDown: {e}")

    def test_app(self) -> None:
        self.setUp()
        try:
            time.sleep(30)  # Allow the app to load
            wait = WebDriverWait(self.driver, 40)
            
            initial_hierarchy =self.driver.page_source
            self.driver.start_recording_screen()
            print(initial_hierarchy)
            
            

            # Capture initial screen screenshot
            initial_screenshot_path = os.path.join(settings.MEDIA_ROOT, 'screenshots', f'{self.app_instance.id}_initial.png')
            self.driver.save_screenshot(initial_screenshot_path)
            print("scren1 taken")

            # Simulate a click on the first button
            # Wait for the element to be present
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.Button'))
            )
            first_button = self.driver.find_element(by=AppiumBy.CLASS_NAME, value='android.widget.Button')
            first_button.click()
            time.sleep(20)  # Allow the app to load


            # Wait for the screen to change
            # Capture subsequent screen screenshot
            subsequent_screenshot_path = os.path.join(settings.MEDIA_ROOT, 'screenshots', f'{self.app_instance.id}_subsequent.png')
            self.driver.save_screenshot(subsequent_screenshot_path)
            print("scrn2 taken")

            subsequent_hierarchy = self.driver.page_source
            screen_changed = initial_hierarchy != subsequent_hierarchy
            print(screen_changed, 'screen_changed')
            time.sleep(20)  # Allow the app to load

            # Define the path for the video recording
            video_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{self.app_instance.id}_test_video.mp4')

            # Stop recording and get the raw video data (Base64 encoded string)
            raw_video_data = self.driver.stop_recording_screen()

            # Decode the Base64 string into bytes
            video_data_bytes = base64.b64decode(raw_video_data)

            # Write the decoded bytes to the specified file
            with open(video_path, 'wb') as video_file:
                video_file.write(video_data_bytes)
            print(f"Initial Screenshot Path: {initial_screenshot_path}")
            print(f"Subsequent Screenshot Path: {subsequent_screenshot_path}")
            print(f"Video Path: {video_path}")

            # Store the results in the database
            self.app_instance.ui_hierarchy = initial_hierarchy
            self.app_instance.screen_changed = screen_changed
            self.app_instance.first_screen_screenshot_path = initial_screenshot_path
            self.app_instance.second_screen_screenshot_path = subsequent_screenshot_path
            self.app_instance.video_recording_path = video_path
            self.app_instance.save()
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        finally:
            self.tearDown()
        

# Helper function to run the test case
def run_appium_test(apk_file_path, app_instance):

    apk_path = os.path.join(settings.MEDIA_ROOT, apk_file_path.name)  #path absloute value for the test
    
    # Check if the APK file exists
    if not os.path.exists(apk_path):
        print(f"APK file not found at: {apk_path}")
        return

    # Create an instance of AppiumTestCase
    test_case = AppiumTestCase(apk_path=apk_path, app_instance=app_instance)
    
    # Run the test case
    test_case.test_app()


    


def app_list(request):
    apps = App.objects.all()
    return render(request, 'apps_manager/app_list.html', {'apps': apps})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('app_list')  # Redirect to a success page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def app_list(request):
    apps = App.objects.filter(uploaded_by=request.user)
    return render(request, 'apps_manager/app_list.html', {'apps': apps})

@login_required
def app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id, uploaded_by=request.user)

    context = {
            'app': app,
        }
    return render(request, 'apps_manager/app_detail.html', context)
@login_required
def app_create(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.uploaded_by = request.user
            app.save()
            print('app.apk_file_path',app.apk_file_path)
            run_appium_test(app.apk_file_path, app)
            return redirect('app_list')
    else:
        form = AppForm()
    return render(request, 'apps_manager/app_form.html', {'form': form})


@login_required
def app_update(request, app_id):
    app = get_object_or_404(App, id=app_id, uploaded_by=request.user)
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            run_appium_test(app.apk_file_path,app)
            return redirect('app_list')
    else:
        form = AppForm(instance=app)
    return render(request, 'apps_manager/app_form.html', {'form': form})

@login_required
def app_delete(request, app_id):
    app = get_object_or_404(App, id=app_id, uploaded_by=request.user)
    if request.method == 'POST':
        app.delete()
        return redirect('app_list')
    return render(request, 'apps_manager/app_confirm_delete.html', {'app': app})


