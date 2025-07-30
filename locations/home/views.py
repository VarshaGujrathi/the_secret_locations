from django.shortcuts import render
from django.http import JsonResponse

import os
import webbrowser

from exif import Image
from gmplot import gmplot
from geopy.geocoders import Nominatim

def home(request):
    return render(request, "home.html")

def display(request):
    return render(request, "display.html")

def process_image(request):
    # Define the filename and input/output paths
    filename = 'Goa'
    input_path = os.path.join(os.path.dirname(__file__), f'static/img/{filename}.jpg')
    output_path = os.path.join(os.path.dirname(__file__), f'{filename}-location.html')

    def decimal_coords(coords, ref):
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref in ('S', 'W'):
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    with open(input_path, 'rb') as src:
        img = Image(src)

    lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
    lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)

    gmap = gmplot.GoogleMapPlotter(lat, lon, 12)
    gmap.marker(lat, lon, 'red')
    gmap.draw(output_path)

    address = Nominatim(user_agent='GetLoc')
    location = address.reverse(f'{lat}, {lon}')

    google_maps_url = f"https://www.google.com/maps/dir//{location.address[0:30]}/@{lat},{lon},20z"

    return JsonResponse({'url': google_maps_url})

def process_image_CSMT(request):
    filename = 'CSMT'
    input_path = os.path.join(os.path.dirname(__file__), f'static/img/{filename}.jpg')
    output_path = os.path.join(os.path.dirname(__file__), f'{filename}-location.html')

    def decimal_coords(coords, ref):
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref in ('S', 'W'):
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    with open(input_path, 'rb') as src:
        img = Image(src)

    lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
    lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)

    gmap = gmplot.GoogleMapPlotter(lat, lon, 12)
    gmap.marker(lat, lon, 'red')
    gmap.draw(output_path)

    address = Nominatim(user_agent='GetLoc')
    location = address.reverse(f'{lat}, {lon}',timeout=10)

    google_maps_url = f"https://www.google.com/maps/dir//{location.address[0:30]}/@{lat},{lon},20z"

    return JsonResponse({'url': google_maps_url})
def process_image_IndGate(request):
    filename = 'IndGate'
    input_path = os.path.join(os.path.dirname(__file__), f'static/img/{filename}.jpg')
    output_path = os.path.join(os.path.dirname(__file__), f'{filename}-location.html')

    def decimal_coords(coords, ref):
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref in ('S', 'W'):
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    with open(input_path, 'rb') as src:
        img = Image(src)

    lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
    lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)

    gmap = gmplot.GoogleMapPlotter(lat, lon, 12)
    gmap.marker(lat, lon, 'red')
    gmap.draw(output_path)

    address = Nominatim(user_agent='GetLoc')
    location = address.reverse(f'{lat}, {lon}',timeout=10)

    google_maps_url = f"https://www.google.com/maps/dir//{location.address[0:30]}/@{lat},{lon},20z"

    return JsonResponse({'url': google_maps_url})


# def process_image(request, filename):
#     # Define the filename and input/output paths
#     filename = filename
#     # input_path = os.path.join(os.path.dirname(__file__), f'{filename}.jpg')
#     # output_path = os.path.join(os.path.dirname(__file__), f'{filename}-location.html')
#     input_path = os.path.join(os.path.dirname(__file__), f'{filename}.jpg')
#     output_path = os.path.join(os.path.dirname(__file__), f'{filename}-location.html')


#     def decimal_coords(coords, ref):
#         decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
#         if ref in ('S', 'W'):
#             decimal_degrees = -decimal_degrees
#         return decimal_degrees

#     with open(input_path, 'rb') as src:
#         img = Image(src)

#     lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
#     lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)

#     gmap = gmplot.GoogleMapPlotter(lat, lon, 12)
#     gmap.marker(lat, lon, 'red')
#     gmap.draw(output_path)

#     address = Nominatim(user_agent='GetLoc')
#     location = address.reverse(f'{lat}, {lon}')

#     google_maps_url = f"https://www.google.com/maps/dir//{location.address[0:30]}/@{lat},{lon},20z"

#     return JsonResponse({'url': google_maps_url})


# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def process_image(request):
#     filename = request.GET.get('filename')
#     # Define the input/output paths
#     input_path = os.path.join(os.path.dirname(__file__), f'{filename}.jpg')
#     output_path = os.path.join(os.path.dirname(__file__), f'{filename}-location.html')

#     def decimal_coords(coords, ref):
#         decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
#         if ref in ('S', 'W'):
#             decimal_degrees = -decimal_degrees
#         return decimal_degrees

#     with open(input_path, 'rb') as src:
#         img = Image(src)

#     lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
#     lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)

#     gmap = gmplot.GoogleMapPlotter(lat, lon, 12)
#     gmap.marker(lat, lon, 'red')
#     gmap.draw(output_path)

#     address = Nominatim(user_agent='GetLoc')
#     location = address.reverse(f'{lat}, {lon}')

#     google_maps_url = f"https://www.google.com/maps/dir//{location.address[0:30]}/@{lat},{lon},20z"

#     return JsonResponse({'url': google_maps_url})