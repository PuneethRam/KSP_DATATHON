from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
import os
import matplotlib.pyplot as plt
import io
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
import pandas as pd
from django.core.files.storage import FileSystemStorage
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from keras.models import load_model
from .models import AnalysisResult
from .models import TelegramAnalysis
from ultralytics import YOLO
from IPython import display
display.clear_output()
import ultralytics
import folium
from folium.plugins import MarkerCluster


def index(request):
  context = {
    'segment': 'index'
  }
  return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/tables.html", context)

# Components
@login_required(login_url='/accounts/login/')
def bc_button(request):
  context = {
    'parent': 'basic_components',
    'segment': 'button'
  }
  return render(request, "pages/components/bc_button.html", context)

@login_required(login_url='/accounts/login/')
def bc_badges(request):
  context = {
    'parent': 'basic_components',
    'segment': 'badges'
  }
  return render(request, "pages/components/bc_badges.html", context)

@login_required(login_url='/accounts/login/')
def bc_breadcrumb_pagination(request):
  context = {
    'parent': 'basic_components',
    'segment': 'breadcrumbs_&_pagination'
  }
  return render(request, "pages/components/bc_breadcrumb-pagination.html", context)

@login_required(login_url='/accounts/login/')
def bc_collapse(request):
  context = {
    'parent': 'basic_components',
    'segment': 'collapse'
  }
  return render(request, "pages/components/bc_collapse.html", context)

@login_required(login_url='/accounts/login/')
def bc_tabs(request):
  context = {
    'parent': 'basic_components',
    'segment': 'navs_&_tabs'
  }
  return render(request, "pages/components/bc_tabs.html", context)

@login_required(login_url='/accounts/login/')
def bc_typography(request):
  context = {
    'parent': 'basic_components',
    'segment': 'typography'
  }
  return render(request, "pages/components/bc_typography.html", context)

@login_required(login_url='/accounts/login/')
def icon_feather(request):
  context = {
    'parent': 'basic_components',
    'segment': 'feather_icon'
  }
  return render(request, "pages/components/icon-feather.html", context)


# Forms and Tables
@login_required(login_url='/accounts/login/')
def form_elements(request):
  context = {
    'parent': 'form_components',
    'segment': 'form_elements'
  }
  return render(request, 'pages/form_elements.html', context)

@login_required(login_url='/accounts/login/')
def basic_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'basic_tables'
  }
  return render(request, 'pages/tbl_bootstrap.html', context)

# Chart and Maps
@login_required(login_url='/accounts/login/')
def morris_chart(request):
  context = {
    'parent': 'chart',
    'segment': 'morris_chart'
  }
  return render(request, 'pages/chart-morris.html', context)

@login_required(login_url='/accounts/login/')
def google_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'google_maps'
  }
  return render(request, 'pages/map-google.html', context)

# Authentication
class UserRegistrationView(CreateView):
  template_name = 'accounts/auth-signup.html'
  form_class = RegistrationForm
  success_url = '/accounts/login/'

class UserLoginView(LoginView):
  template_name = 'accounts/auth-signin.html'
  form_class = LoginForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/auth-reset-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/auth-password-reset-confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/auth-change-password.html'
  form_class = UserPasswordChangeForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def profile(request):
  context = {
    'segment': 'profile',
  }
  return render(request, 'pages/profile.html', context)

@login_required(login_url='/accounts/login/')
def sample_page(request):
  context = {
    'segment': 'sample_page',
  }
  return render(request, 'pages/sample-page.html', context)



@login_required(login_url='/accounts/login/')
def pedestrian(request):
  context = {
    'segment': 'sample_page',
  }
  return render(request, 'pages/pedestrian.html', context)



@login_required(login_url='/accounts/login/')
def overall(request):
    map_html_path = '' 

    df=pd.read_csv(r'home\datasets\FINAL_KARNATAKA_DATA.csv')

    if request.method == 'POST':
        district = request.POST.get('district')
        districts_to_keep = [district]
        df = df[df['DISTRICTNAME'].isin(districts_to_keep)]
        center_point = [12.9716, 77.5946]  # Example center point for Mysuru City
        m = folium.Map(location=center_point, zoom_start=7)
        marker_cluster = MarkerCluster().add_to(m)
        for index, row in df.iterrows():
            # Create a popup message for the marker
            popup_text = f"Accident Spot: {row['Accident_Spot']}\nAccident SubLocation: {row['Accident_SubLocation']}\nSeverity: {row['Severity']}"

            # Create a marker and add it to the MarkerCluster layer
            folium.Marker([row['Latitude'], row['Longitude']], popup=popup_text).add_to(marker_cluster)
        # Save the map as an HTML file
        map_html_path = r'static\assets\maps\maps.html'
        m.save(map_html_path)


    

    accident_analysis = []
    for year in range(2016, 2024):
        fatal_count = df[(df['Year'].astype(int) == year) & (df['Severity'].astype(str) == 'Fatal')].shape[0]
        non_fatal_count = df[(df['Year'].astype(int) == year) & (df['Severity'].astype(str) != 'Fatal')].shape[0]
        accident_analysis.append({'year': year, 'fatal': fatal_count, 'non_fatal': non_fatal_count})
    main_cause_counts = df['Main_Cause'].value_counts().reset_index().rename(columns={'index': 'Main_Cause', 'Main_Cause': 'count'})


    year_roadcondition_counts = df.groupby(['Year', 'Road_Condition']).size().reset_index(name='count')

    data_by_year = {}
    for _, row in year_roadcondition_counts.iterrows():
        year = row['Year']
        roadcondition = row['Road_Condition']  # Corrected column name
        count = row['count']
        if year not in data_by_year:
            data_by_year[year] = {}
        data_by_year[year][roadcondition] = count
    years = sorted(data_by_year.keys())
    roadconditions = sorted(list(set(rc for rc_counts in data_by_year.values() for rc in rc_counts.keys())))
    series = [{ 'name': rc, 'data': [data_by_year.get(year, {}).get(rc, 0) for year in years] } for rc in roadconditions]


#---------------------------------------------------------------------------------------------------------------------------
    #weather severity
    # Group by 'Weather' and 'Severity' and count occurrences
    weather_severity_counts = df.groupby(['Weather', 'Severity']).size().reset_index(name='count')

    # Prepare data for Highcharts
    weather_categories = sorted(df['Weather'].unique())
    fatal_data = []
    non_fatal_data = []

    for weather in weather_categories:
        fatal_count = weather_severity_counts[(weather_severity_counts['Weather'] == weather) & (weather_severity_counts['Severity'] == 'Fatal')]['count'].sum()
        non_fatal_count = weather_severity_counts[(weather_severity_counts['Weather'] == weather) & (weather_severity_counts['Severity'] != 'Fatal')]['count'].sum()
        fatal_data.append(fatal_count)
        non_fatal_data.append(non_fatal_count)

    series_data = [
        {
            'name': 'Fatal',
            'data': fatal_data
        },
        {
            'name': 'Non Fatal',
            'data': non_fatal_data
        }
    ]




#--------------------------------------------------------------------------------------------------------------------
#accident spot
    accident_collision_counts = df.groupby(['Accident_Spot', 'Severity']).size().reset_index(name='count')
    
    # Prepare data for Highcharts
    accident_spots = sorted(df['Accident_Spot'].unique())
    collision_types = sorted(df['Severity'].unique())
    series_data2 = []

    for collision_type in collision_types:
        data = []
        for accident_spot in accident_spots:
            count = accident_collision_counts[(accident_collision_counts['Accident_Spot'] == accident_spot) & (accident_collision_counts['Severity'] == collision_type)]['count'].sum()
            data.append(count)
        series_data2.append({
            'name': collision_type,
            'data': data
        })    




     
#---------------------------------------------------------------------------------------------------------------------
    context = {
       'accident_analysis': accident_analysis,
       'main_cause_counts': main_cause_counts.to_dict('records'),
       'years': years,
       'series': series,
       'weather_categories': weather_categories,
       'series_data': series_data,
       'map_html_path': map_html_path,
       'accident_spots': accident_spots,
       'collision_types': collision_types,
       'series_data2': series_data2,
    }

    return render(request, 'pages/overall.html', context)






@login_required(login_url='/accounts/login/')
def timeanalysis(request): 
    map_html_path = ''
    import folium
    from folium.plugins import MarkerCluster

    if request.method == 'POST':
        district = request.POST.get('district')
        type = request.POST.get('type')
      
        a=pd.read_csv(r'home\datasets\FINAL_KARNATAKA_DATA.csv')
        districts_to_keep = [district]
        filtered_data = a[a['DISTRICTNAME'].isin(districts_to_keep)]
        filtered_data.to_csv(r'home\datasets\dataset.csv', index=False)


        df=pd.read_csv(r'home\datasets\dataset.csv')
        if type=="Cause":
            # Create a map object
            m = folium.Map(location=[12.2958, 76.6394], zoom_start=10)

            # Create separate MarkerCluster layers for each cause of the accident
            human_error_cluster = MarkerCluster(name='Human Error', control=False).add_to(m)
            vehicle_defect_cluster = MarkerCluster(name='Vehicle Defect', control=False).add_to(m)
            not_applicable_cluster = MarkerCluster(name='Not Applicable', control=False).add_to(m)
            road_defect_cluster = MarkerCluster(name='Road Environment Defect', control=False).add_to(m)

            # Define icon URLs
            orange_url = 'https://images.emojiterra.com/google/android-12l/512px/1f7e0.png'
            yellow_url = 'https://www.pngall.com/wp-content/uploads/15/Yellow-Circle-No-Background.png'
            green_url = 'https://png.pngtree.com/png-vector/20220523/ourmid/pngtree-green-circle-button-on-white-background-push-modern-paper-vector-png-image_13628152.png'
            human_icon_url = 'https://cdn-icons-png.freepik.com/256/10/10522.png'
            vehicle_icon_url = 'https://cdn-icons-png.freepik.com/512/310/310742.png'
            not_applicable_icon_url = 'https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png'

            # road_defect_icon_url = 'https://png.pngtree.com/png-clipart/20221228/original/pngtree-fault-sign-png-image_8817270.png'
            road_defect_icon_url = 'https://static-00.iconduck.com/assets.00/unpaved-road-icon-2046x2048-h5paxc1b.png'


            # Define icons for legend
            legend_icons = {
                'Be Alert (<10)' : 'https://images.emojiterra.com/google/android-12l/512px/1f7e0.png',
                'Accident Prone (10-100)' : 'https://www.pngall.com/wp-content/uploads/15/Yellow-Circle-No-Background.png',
                'Red Zone (>100)' : 'https://png.pngtree.com/png-vector/20220523/ourmid/pngtree-green-circle-button-on-white-background-push-modern-paper-vector-png-image_13628152.png',
                'Human Error': 'https://cdn-icons-png.freepik.com/256/10/10522.png',
                'Vehicle Defect': 'https://cdn-icons-png.freepik.com/512/310/310742.png',
                'Not Applicable': 'https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png',
                'Road Environment Defect': 'https://static-00.iconduck.com/assets.00/unpaved-road-icon-2046x2048-h5paxc1b.png'

            }


            # Create legend HTML
            legend_html = """
            <div style="
                position: fixed;
                bottom: 50px;
                left: 50px;
                width: 300px;
                height: auto;
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                z-index: 1000;
                font-size: 16px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            ">

                <!-- First set of legends -->
                <div style="margin-top: 10px;">
                    <p style="font-weight: bold; margin-bottom: 5px;text-align: center;">Number of Accidents</p>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: green; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Be alert:</span> Less than 10
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: yellow; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Accident Prone:</span> 10 to 100
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: orange; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Danger Zone:</span> Greater than 100
                    </div>
                </div>

              <div style="position: fixed; top: 10px; right: 10px; z-index: 1000; background-color: #fff; border: 2px solid #ccc; border-radius: 5px; padding: 10px;">
                <p style="font-weight: bold;">Main Cause </p>
                <div style="margin-top: 5px;">
                    <img src="https://cdn-icons-png.freepik.com/256/10/10522.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;">Human Error</span>
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://cdn-icons-png.freepik.com/512/310/310742.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;">Vehicle Defect</span>
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://static-00.iconduck.com/assets.00/unpaved-road-icon-2046x2048-h5paxc1b.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;">Road Environment Defect</span>
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;">Other Reasons</span>
                </div>
            </div>
            """

            # for cause, icon_url in legend_icons.items():
            #     legend_html += f"""
            #     <p style="margin: 5px 0;"><img src="{icon_url}" style="width: 20px; height: 20px; margin-right: 5px;">{cause}</p>
            # """



            legend_html += """
            </div>
            """

            # Add legend as a custom control
            m.get_root().html.add_child(folium.Element(legend_html))

            # Iterate through the DataFrame and add markers to the appropriate cluster
            for index, row in df.iterrows():
                # Determine the cause of the accident
                cause = row['Main_Cause']

                # Set the icon and cluster based on the cause
                if cause == 'Human Error':
                    icon = folium.features.CustomIcon(human_icon_url, icon_size=(30, 30))
                    cluster = human_error_cluster
                elif cause == 'Vehicle Defect':
                    icon = folium.features.CustomIcon(vehicle_icon_url, icon_size=(30, 30))
                    cluster = vehicle_defect_cluster
                elif cause == 'Not Applicable':
                    icon = folium.features.CustomIcon(not_applicable_icon_url, icon_size=(30, 30))
                    cluster = not_applicable_cluster
                elif cause == 'Road Environment Defect':
                    icon = folium.features.CustomIcon(road_defect_icon_url, icon_size=(30, 30))
                    cluster = road_defect_cluster
                else:
                    continue  # Skip unknown causes

                # Add marker to the appropriate cluster
                # folium.Marker(location=[row['Latitude'], row['Longitude']], icon=icon).add_to(cluster)
                folium.Marker(location=[row['Latitude'], row['Longitude']], icon=icon, tooltip=cause).add_to(cluster)

            # Add layer control to toggle between clusters
            folium.LayerControl(collapsed=False).add_to(m)

            # Save the map as an HTML file
            map_html_path = r'static\assets\maps\factor_map.html'
            m.save(map_html_path)
        

        elif type=="severity":
          
            # Create a map object
            m = folium.Map(location=[12.2958, 76.6394], zoom_start=10)
            # Create separate MarkerCluster layers for each cause of the accident
            Damage_Only_cluster = MarkerCluster(name='Damage Only', control=False).add_to(m)
            simple_injury_cluster = MarkerCluster(name='Simple Injury', control=False).add_to(m)
            not_applicable_cluster = MarkerCluster(name='Not Applicable', control=False).add_to(m)
            Grievous_Injury_cluster = MarkerCluster(name='Grievous Injury', control=False).add_to(m)
            Fatal_cluster = MarkerCluster(name='Fatal', control=False).add_to(m)

            # Define icon URLs
            orange_url = 'https://images.emojiterra.com/google/android-12l/512px/1f7e0.png'
            yellow_url = 'https://www.pngall.com/wp-content/uploads/15/Yellow-Circle-No-Background.png'
            green_url = 'https://png.pngtree.com/png-vector/20220523/ourmid/pngtree-green-circle-button-on-white-background-push-modern-paper-vector-png-image_13628152.png'
            fatal_url = 'https://static.thenounproject.com/png/53747-200.png'
            grievous_injury_url = 'https://cdn-icons-png.flaticon.com/512/6098/6098835.png'
            damage_url = 'https://icons.veryicon.com/png/o/internet--web/collection-and-payment/damage.png'
            simple_injury_url = 'https://icon-library.com/images/injury-icon/injury-icon-2.jpg'
            not_applicable_icon_url = 'https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png'

            # road_defect_icon_url = 'https://png.pngtree.com/png-clipart/20221228/original/pngtree-fault-sign-png-image_8817270.png'
            road_defect_icon_url = 'https://static-00.iconduck.com/assets.00/unpaved-road-icon-2046x2048-h5paxc1b.png'


            # Define icons for legend
            legend_icons = {
                'Be Alert (<10)' : 'https://images.emojiterra.com/google/android-12l/512px/1f7e0.png',
                'Accident Prone (10-100)' : 'https://www.pngall.com/wp-content/uploads/15/Yellow-Circle-No-Background.png',
                'Red Zone (>100)' : 'https://png.pngtree.com/png-vector/20220523/ourmid/pngtree-green-circle-button-on-white-background-push-modern-paper-vector-png-image_13628152.png',
                'fatal_url' : 'https://static.thenounproject.com/png/53747-200.png',
            'grievous_injury_url' : 'https://cdn-icons-png.flaticon.com/512/6098/6098835.png',
            'damage_url' : 'https://icons.veryicon.com/png/o/internet--web/collection-and-payment/damage.png',
            'simple_injury_url' : 'https://icon-library.com/images/injury-icon/injury-icon-2.jpg',
            'not_applicable_icon_url' : 'https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png'

            }


            # Create legend HTML
            legend_html = """
            <div style="
                position: fixed;
                bottom: 50px;
                left: 50px;
                width: 300px;
                height: auto;
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                z-index: 1000;
                font-size: 16px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            ">

                <!-- First set of legends -->
                <div style="margin-top: 10px;">
                    <p style="font-weight: bold; margin-bottom: 5px;text-align: center;">Number of Accidents</p>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: green; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Be alert:</span> Less than 10
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: yellow; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Accident Prone:</span> 10 to 100
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: orange; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Danger Zone:</span> Greater than 100
                    </div>
                </div>


              <div style="position: fixed; top: 10px; right: 10px; z-index: 1000; background-color: #fff; border: 2px solid #ccc; border-radius: 5px; padding: 10px;">
                <p style="font-weight: bold;">Severity</p>
                <div style="margin-top: 5px;">
                <img src="https://icons.veryicon.com/png/o/internet--web/collection-and-payment/damage.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Damage Only

                </div>
                <div style="margin-top: 5px;">
                      <img src="https://icon-library.com/images/injury-icon/injury-icon-2.jpg" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Simple Injury
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/6098/6098835.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Grievous Injury
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://static.thenounproject.com/png/53747-200.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Fatal Injury
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Other Reasons
                </div>
            </div>
            """

            # for cause, icon_url in legend_icons.items():
            #     legend_html += f"""
            #     <p style="margin: 5px 0;"><img src="{icon_url}" style="width: 20px; height: 20px; margin-right: 5px;">{cause}</p>
            # """



            legend_html += """
            </div>
            """

            # Add legend as a custom control
            m.get_root().html.add_child(folium.Element(legend_html))

            # Iterate through the DataFrame and add markers to the appropriate cluster
            for index, row in df.iterrows():
                # Determine the severity
                cause = row['Severity']


                # Set the icon and cluster based on the cause
                if cause == 'Simple Injury':
                    icon = folium.features.CustomIcon(simple_injury_url, icon_size=(45, 45))
                    cluster = simple_injury_cluster
                elif cause == 'Grievous Injury':
                    icon = folium.features.CustomIcon(grievous_injury_url, icon_size=(45, 45))
                    cluster = Grievous_Injury_cluster
                elif cause == 'Not Applicable':
                    icon = folium.features.CustomIcon(not_applicable_icon_url, icon_size=(30, 30))
                    cluster = not_applicable_cluster
                elif cause == 'Damage Only':
                    icon = folium.features.CustomIcon(damage_url, icon_size=(45, 45))
                    cluster = Damage_Only_cluster
                elif cause == 'Fatal':
                    icon = folium.features.CustomIcon(fatal_url, icon_size=(45, 45))
                    cluster = Fatal_cluster
                else:
                    continue  # Skip unknown causes

                # Add marker to the appropriate cluster
                # folium.Marker(location=[row['Latitude'], row['Longitude']], icon=icon).add_to(cluster)
                folium.Marker(location=[row['Latitude'], row['Longitude']], icon=icon, tooltip=cause).add_to(cluster)

            # Add layer control to toggle between clusters
            folium.LayerControl(collapsed=False).add_to(m)

            # Save the map as an HTML file
            map_html_path = r'static\assets\maps\factor_map.html'
        
            m.save(map_html_path)

        elif type=="weather":
            m = folium.Map(location=[12.2958, 76.6394], zoom_start=10)

            clear_conditions = ['Clear', 'Fine', 'Very Hot']
            cloudy_conditions = ['Cloudy']
            wind_conditions = ['Wind', 'Dust Storm']
            rain_conditions = ['Light Rain', 'Heavy Rain', 'Flooding of Slipways/Rivulets']
            snow_conditions = ['Mist or Fog', 'Hail or Sleet', 'Very Cold']
            other_conditions = ['Not Applicable']

            # Create separate MarkerCluster layers for each condition
            clear_cluster_1 = MarkerCluster(name='Clear', control=False).add_to(m)
            cloudy_cluster_2 = MarkerCluster(name='Cloudy', control=False).add_to(m)
            wind_cluster_6 = MarkerCluster(name='Wind', control=False).add_to(m)
            rain_cluster_3= MarkerCluster(name='Rain', control=False).add_to(m)
            Snow_cluster_4 = MarkerCluster(name='Snow', control=False).add_to(m)
            Others_cluster_5 = MarkerCluster(name='Other', control=False).add_to(m)


            # Define icon URLs
            orange_url = 'https://images.emojiterra.com/google/android-12l/512px/1f7e0.png'
            yellow_url = 'https://www.pngall.com/wp-content/uploads/15/Yellow-Circle-No-Background.png'
            green_url = 'https://png.pngtree.com/png-vector/20220523/ourmid/pngtree-green-circle-button-on-white-background-push-modern-paper-vector-png-image_13628152.png'
            clear_url = 'https://cdn-icons-png.flaticon.com/512/3222/3222807.png'
            cloudy_url = 'https://cdn-icons-png.flaticon.com/512/1163/1163736.png'
            rain_url = 'https://cdn-icons-png.freepik.com/512/4150/4150897.png'
            snow_url = 'https://cdn-icons-png.flaticon.com/512/2834/2834547.png'
            not_applicable_icon_url = 'https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png'
            wind_url = 'https://cdn-icons-png.flaticon.com/512/3104/3104631.png'



            # Define icons for legend
            legend_icons = {
                'Be Alert (<10)' : 'https://images.emojiterra.com/google/android-12l/512px/1f7e0.png',
                'Accident Prone (10-100)' : 'https://www.pngall.com/wp-content/uploads/15/Yellow-Circle-No-Background.png',
                'Red Zone (>100)' : 'https://png.pngtree.com/png-vector/20220523/ourmid/pngtree-green-circle-button-on-white-background-push-modern-paper-vector-png-image_13628152.png',
            'clear_url' : 'https://cdn-icons-png.flaticon.com/512/3222/3222807.png',
            'cloudy_url' : 'https://cdn-icons-png.flaticon.com/512/1163/1163736.png',
            'rain_url' : 'https://cdn-icons-png.freepik.com/512/4150/4150897.png',
            'snow_url' : 'https://cdn-icons-png.flaticon.com/512/2834/2834547.png',
            'not_applicable_icon_url' : 'https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png',
            'wind_url': 'https://cdn-icons-png.flaticon.com/512/3104/3104631.png'
            }


            # Create legend HTML
            legend_html = """
            <div style="
                position: fixed;
                bottom: 50px;
                left: 50px;
                width: 300px;
                height: auto;
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                z-index: 1000;
                font-size: 16px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            ">

                <!-- First set of legends -->
                <div style="margin-top: 10px;">
                    <p style="font-weight: bold; margin-bottom: 5px;text-align: center;">Number of Accidents</p>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: green; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Be alert:</span> Less than 10
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: yellow; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Accident Prone:</span> 10 to 100
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="display: inline-block; width: 20px; height: 20px; background-color: orange; margin-right: 5px;"></span>
                        <span style="font-weight: bold;">Danger Zone:</span> Greater than 100
                    </div>
                </div>



              <div style="position: fixed; top: 10px; right: 10px; z-index: 1000; background-color: #fff; border: 2px solid #ccc; border-radius: 5px; padding: 10px;">
                <p style="font-weight: bold;">Weather Conditions</p>
                <div style="margin-top: 5px;">
                <img src="https://cdn-icons-png.flaticon.com/512/3222/3222807.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Clear Sky

                </div>
                <div style="margin-top: 5px;">
                      <img src="https://cdn-icons-png.flaticon.com/512/1163/1163736.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Cloudy
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://cdn-icons-png.freepik.com/512/4150/4150897.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Rainy
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2834/2834547.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Snow or Fog
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/3104/3104631.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Windy
                </div>
                <div style="margin-top: 5px;">
                    <img src="https://static-00.iconduck.com/assets.00/warning-icon-2048x2048-wfo0sck3.png" style="width: 20px; height: 20px; margin-right: 5px;">
                    <span style="font-weight: bold;"></span> Other Reasons
                </div>
            </div>
            """

            # for cause, icon_url in legend_icons.items():
            #     legend_html += f"""
            #     <p style="margin: 5px 0;"><img src="{icon_url}" style="width: 20px; height: 20px; margin-right: 5px;">{cause}</p>
            # """



            legend_html += """
            </div>
            """

            # Add legend as a custom control
            m.get_root().html.add_child(folium.Element(legend_html))

            # Iterate through the DataFrame and add markers to the appropriate cluster
            for index, row in df.iterrows():
                # Determine the severity
                cause = row['Weather']


                # Set the icon and cluster based on the cause
                if cause == 'Clear' or cause== 'Fine' or cause=='Very Hot':
                    icon = folium.features.CustomIcon(clear_url, icon_size=(45, 45))
                    cluster = clear_cluster_1
                elif cause == 'Cloudy':
                    icon = folium.features.CustomIcon(cloudy_url, icon_size=(45, 45))
                    cluster = cloudy_cluster_2
                elif cause == 'Wind' or cause =='Dust Storm':
                    icon = folium.features.CustomIcon(wind_url, icon_size=(30, 30))
                    cluster = wind_cluster_6
                elif cause == 'Light Rain' or cause == 'Heavy Rain' or cause == 'Flooding of Slipways/Rivulets':
                    icon = folium.features.CustomIcon(rain_url, icon_size=(45, 45))
                    cluster = rain_cluster_3
                elif cause == 'Mist or Fog' or 'Hail or Sleet' or 'Very Cold':
                    icon = folium.features.CustomIcon(snow_url, icon_size=(45, 45))
                    cluster = Snow_cluster_4
                elif cause == 'Not Applicable':
                    icon = folium.features.CustomIcon(not_applicable_icon_url, icon_size=(45, 45))
                    cluster = Others_cluster_5
                else:
                    continue  # Skip unknown causes

                # Add marker to the appropriate cluster
                # folium.Marker(location=[row['Latitude'], row['Longitude']], icon=icon).add_to(cluster)
                folium.Marker(location=[row['Latitude'], row['Longitude']], icon=icon, tooltip=cause).add_to(cluster)

            # Add layer control to toggle between clusters
            folium.LayerControl(collapsed=False).add_to(m)

            # Save the map as an HTML file
            map_html_path = r'static\assets\maps\factor_map.html'       
            m.save(map_html_path)

        elif type=="time":
            starttime = pd.to_datetime(request.POST.get('starttime'))
            endtime = pd.to_datetime(request.POST.get('endtime'))

            karnataka_map = folium.Map(location=[12.9716, 77.5946], zoom_start=7)
            custom_icon_create_function = """
            function(cluster) {
                var markers = cluster.getAllChildMarkers();
                var childCount = markers.length;
                var size = 'small';
                
                // Adjust icon size dynamically based on the label value
                var width = Math.min(40 + childCount * 2, 150);  // Limit maximum size to 100 pixels
                var height = width;  // Make the height the same as the width
                
                if (childCount < 5) {
                    size = 'tiny';
                } else if (childCount < 20) {
                    size = 'small';
                } else if (childCount < 100 ) {
                    size = 'medium-small';
                } else if (childCount < 200) {
                    size = 'medium';
                } else if (childCount < 500) {
                    size = 'medium-large';
                } else if (childCount < 600) {
                    size = 'large';
                } else {
                    size = 'extra-large';
                }
                
                var opacity = 1.0;  // Default opacity
                
                // Adjust opacity based on the cluster size
                if (size === 'large')  {
                    opacity = 0.3;  // Minimum transparency for large and extra-large clusters
                } else if (size === 'extra-large') {
                    opacity = 0.4;
                } else if (size === 'medium')  {
                    opacity = 0.45;  // Medium transparency for medium and medium-large clusters
                } else if(size === 'medium-large') {
                    opacity = 0.5; 
                } else {
                    opacity = 0.6;  // Default transparency for other cluster sizes
                }
                
                var html = '<div style="background-color: rgba(255, 0, 0, ' + opacity + '); color: white; border-radius: 50%; border: 1px solid white; width: ' + width + 'px; height: ' + height + 'px; text-align: center; line-height: ' + height + 'px;">' + childCount + '</div>';

                return L.divIcon({
                    html: html,
                    className: 'marker-cluster',
                    iconSize: [width, height]
                });
            }
            """


            # Create a MarkerCluster layer with the custom icon creation function
            marker_cluster = MarkerCluster(icon_create_function=custom_icon_create_function).add_to(karnataka_map)

            for index, row in df.iterrows():
                lat, lon = row['Latitude'], row['Longitude']
                time = pd.to_datetime(row['Time'])  # Assuming 'Time' column contains datetime objects

                # Check if the time of the data point falls within the specified range
                if starttime <= time <= endtime:
                    # Create a custom icon for the marker
                    icon = folium.Icon(color='red', icon='exclamation-triangle', prefix='fa')

                    # Create a popup message for the marker
                    popup_text = f"Accident Spot: {row['Accident_Spot']}\nAccident SubLocation: {row['Accident_SubLocation']}\nSeverity: {row['Severity']}"

                    # Create a marker with the custom icon and add it to the MarkerCluster layer
                    folium.Marker([lat, lon], popup=popup_text, icon=icon).add_to(marker_cluster)

            map_html_path = r'static\assets\maps\factor_map.html'       
            m.save(map_html_path) 


    return render(request, 'pages/timeanalysis.html', {'map_html_path': map_html_path})



@login_required(login_url='/accounts/login/')
def telegram(request):
    lat = float(request.GET.get('lat'))
    lon = float(request.GET.get('lon'))
    df=pd.read_csv(r'home\datasets\updated_dataset.csv')
    RegionData = df[(df['Region_Latitude'].astype(float) == lat) & (df['Region_Longitude'].astype(float) == lon)]
    
    

    accident_analysis = []
    for year in range(2016, 2024):
        fatal_count = RegionData[(RegionData['Year'].astype(int) == year) & (RegionData['Severity'].astype(str) == 'Fatal')].shape[0]
        non_fatal_count = RegionData[(RegionData['Year'].astype(int) == year) & (RegionData['Severity'].astype(str) != 'Fatal')].shape[0]
        accident_analysis.append({'year': year, 'fatal': fatal_count, 'non_fatal': non_fatal_count})
    main_cause_counts = RegionData['Main_Cause'].value_counts().reset_index().rename(columns={'index': 'Main_Cause', 'Main_Cause': 'count'})

#----------------------------------------------------------------------------------------------------
    #Road condition
    year_roadcondition_counts = RegionData.groupby(['Year', 'Road_Condition']).size().reset_index(name='count')

    data_by_year = {}
    for _, row in year_roadcondition_counts.iterrows():
        year = row['Year']
        roadcondition = row['Road_Condition']  # Corrected column name
        count = row['count']
        if year not in data_by_year:
            data_by_year[year] = {}
        data_by_year[year][roadcondition] = count
    years = sorted(data_by_year.keys())
    roadconditions = sorted(list(set(rc for rc_counts in data_by_year.values() for rc in rc_counts.keys())))
    series = [{ 'name': rc, 'data': [data_by_year.get(year, {}).get(rc, 0) for year in years] } for rc in roadconditions]


#---------------------------------------------------------------------------------------------------------------------------
    #weather severity
    # Group by 'Weather' and 'Severity' and count occurrences
    weather_severity_counts = RegionData.groupby(['Weather', 'Severity']).size().reset_index(name='count')

    # Prepare data for Highcharts
    weather_categories = sorted(RegionData['Weather'].unique())
    fatal_data = []
    non_fatal_data = []

    for weather in weather_categories:
        fatal_count = weather_severity_counts[(weather_severity_counts['Weather'] == weather) & (weather_severity_counts['Severity'] == 'Fatal')]['count'].sum()
        non_fatal_count = weather_severity_counts[(weather_severity_counts['Weather'] == weather) & (weather_severity_counts['Severity'] != 'Fatal')]['count'].sum()
        fatal_data.append(fatal_count)
        non_fatal_data.append(non_fatal_count)

    series_data = [
        {
            'name': 'Fatal',
            'data': fatal_data
        },
        {
            'name': 'Non Fatal',
            'data': non_fatal_data
        }
    ]


#--------------------------------------------------------------------------------------------------------------------
#accident spot
    accident_collision_counts = RegionData.groupby(['Accident_Spot', 'Collision_Type']).size().reset_index(name='count')
    
    # Prepare data for Highcharts
    accident_spots = sorted(RegionData['Accident_Spot'].unique())
    collision_types = sorted(RegionData['Collision_Type'].unique())
    series_data2 = []

    for collision_type in collision_types:
        data = []
        for accident_spot in accident_spots:
            count = accident_collision_counts[(accident_collision_counts['Accident_Spot'] == accident_spot) & (accident_collision_counts['Collision_Type'] == collision_type)]['count'].sum()
            data.append(count)
        series_data2.append({
            'name': collision_type,
            'data': data
        })    

#---------------------------------------------------------------------------------------------------------------------
    context = {
       'accident_analysis': accident_analysis,
       'main_cause_counts': main_cause_counts.to_dict('records'),
       'years': years,
       'series': series,
       'weather_categories': weather_categories,
       'series_data': series_data,
       'accident_spots': accident_spots,
       'collision_types': collision_types,
       'series_data2': series_data2,
    
    }

    return render(request, 'pages/telegram.html', context)
    
    
   


@login_required(login_url='/accounts/login/')
def blackspots(request):
    map_html_path = '' 
    
    if request.method == 'POST':
      district = request.POST.get('district')
      blackspot_type = request.POST.get('blackspot_type')
     

      a=pd.read_csv(r'home\datasets\FINAL_KARNATAKA_DATA.csv')
      districts_to_keep = [district]
      filtered_data = a[a['DISTRICTNAME'].isin(districts_to_keep)]
      filtered_data.to_csv(r'home\datasets\dataset.csv', index=False)


#------------------------------------------------------------------------------------------------------------------------------
#clustering
      from math import radians, sin, cos, sqrt, atan2

      # Load the dataset
      b = pd.read_csv(r'home\datasets\dataset.csv')

      # Define the distance thresholds (in kilometers)
      distance_threshold_1 = 0.3
      distance_threshold_2 = 1

      # Define the Haversine function to calculate the distance between two points
      def haversine(lat1, lon1, lat2, lon2):
          # Convert latitude and longitude from degrees to radians
          lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

          # Haversine formula
          dlon = lon2 - lon1
          dlat = lat2 - lat1
          a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
          c = 2 * atan2(sqrt(a), sqrt(1 - a))
          distance = 6371 * c  # Radius of the Earth in kilometers
          return distance

      # Group coordinates into regions based on distance threshold and 'Accident_Road' column
      region_mapping = {}
      region_data = []

      for i, row in b.iterrows():
          lat, lon, road = row['Latitude'], row['Longitude'], row['Accident_Road']
          matched_region = None
          for region, (region_lat, region_lon, region_road) in region_mapping.items():
              if haversine(lat, lon, region_lat, region_lon) <= distance_threshold_1:
                  matched_region = region
                  break
              elif (distance_threshold_1 < haversine(lat, lon, region_lat, region_lon) <= distance_threshold_2 and
                    road == region_road):
                  matched_region = region
                  break
          if matched_region is None:
              region_mapping[(lat, lon, road)] = (lat, lon, road)
              matched_region = (lat, lon, road)
          region_data.append({'Latitude': lat, 'Longitude': lon, 'Accident_Road': road,
                              'Region_Latitude': matched_region[0], 'Region_Longitude': matched_region[1], 'Region_Road': matched_region[2]})

      # Create a DataFrame with region information
      region_df = pd.DataFrame(region_data)

      # Assign a region name to each unique region based on its latitude, longitude, and road
      region_df['Region_Name'] = region_df.groupby(['Region_Latitude', 'Region_Longitude', 'Region_Road']).ngroup().add(1)

      # Calculate total number of data points in each region
      region_counts = region_df.groupby(['Region_Name']).size().reset_index(name='Total_Data_Points')

      # Merge region counts with region dataframe
      region_df = pd.merge(region_df, region_counts, on='Region_Name')


      final_df = pd.merge(b, region_df, on=['Latitude', 'Longitude'], how='left')
      final_df.sort_values(by='Region_Name', inplace=True)

      final_df.to_csv(r'home\datasets\updated_dataset.csv', index=False)
      print("plotting starting")




  
#-----------------------------------------------------------------------------------------------------------------
#plotting      

      # Load the dataset
      data = pd.read_csv(r'home\datasets\updated_dataset.csv')

      # Create a map centered around Karnataka
      from django.urls import reverse

      # Assuming you have a view named 'analysis' in your Django app
      analysis_url = reverse('telegram')  # Adjust this URL name to match your actual URL pattern

      karnataka_map = folium.Map(location=[12.9716, 77.5946], zoom_start=7)

      # Add data points to the map if Total_Data_Points is greater than 3
      for index, row in data.iterrows():
          lat, lon = row['Region_Latitude'], row['Region_Longitude']
          total_data_points = row['Total_Data_Points']
          if total_data_points > 15:
              # Create a unique class name for each marker
              marker_class = f'marker-{index}'  # Assuming 'index' is unique for each row

              # Create a custom popup for each marker with a link to analysis.html
              popup_content = f'<a href="{analysis_url}?lat={lat}&lon={lon}" target="_blank">Click for analysis</a>'

              folium.CircleMarker(
                  location=[lat, lon],
                  popup=popup_content,  # Assigning the popup content to the marker
                  radius=15,
                  color='red',
                  fill=True,
                  fill_color='red'
              ).add_to(karnataka_map)

      map_html_path = r'static\assets\maps\mysore_map.html'
      karnataka_map.save(map_html_path)


    return render(request, 'pages/blackspots.html', {'map_html_path': map_html_path})




