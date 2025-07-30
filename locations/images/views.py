import tempfile
import os
import imghdr
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from exif import Image as ExifImage
from gmplot import gmplot
from geopy.geocoders import Nominatim
import pyrebase

# Create your views here.
Config = {
    'apiKey': "AIzaSyCEky0Ts6zV55ubIamTc1bRuk44D3CBaPE",
    'authDomain': "secretelocations.firebaseapp.com",
    'databaseURL': "https://secretelocations-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "secretelocations",
    'storageBucket': "secretelocations.appspot.com",
    'messagingSenderId': "548765638919",
    'appId': "1:548765638919:web:1796a95018cbfc72af65a2",
    'measurementId': "G-5Y0B1JTW7S"
}
firebase = pyrebase.initialize_app(Config)
authe = firebase.auth()
storage = firebase.storage()
database = firebase.database()
from django.shortcuts import render, redirect

def home_img(request, user):
    name = database.child('users').child(user['localId']).child('details').child('name').get().val()

    timestamps = database.child('Hidden_places').shallow().get().val()  # Shallow() is used to get keys
    lis_time = list(timestamps)  # Convert Firebase result to a list of keys

    place = []
    Lat = []
    Lon = []
    City = []
    Url = []
    google_maps_url = []

    for i in lis_time:
        details = database.child('Hidden_places').child(i).child('Details').get().val()
        place.append(details.get('Place'))
        Lat.append(details.get('Lat'))
        Lon.append(details.get('Lon'))
        City.append(details.get('City'))
        Url.append(details.get('Url'))
        google_maps_url.append(f"https://www.google.com/maps/dir//{details.get('Location')[0:30]}/@{details.get('Lat')},{details.get('Lon')},20z")

    det = zip(place, City, Url, google_maps_url)

    return render(request, "images.html", {"e": name, "det": det})


# def home_img(request, user=None):
#     if 'uid' not in request.session:
#         return redirect('sign_in')  # Redirect to the sign-in page if session is not active

#     session_id = request.session['uid']
#     account_info = authe.get_account_info(session_id)
    
#     if account_info:
#         user_data = account_info['users']
#         print(user_data)
#         return render(request, "images.html", {"e": request.session.get('user_name')})
#     else:
#         return redirect('sign_in')  # Redirect to the sign-in page if account info is not valid


@csrf_exempt
def upload(request):

    return render(request, "upload.html")

@csrf_exempt
def process_upload(request):
    if request.method == 'POST':
        if 'file[]' in request.FILES:
            uploaded_file = request.FILES['file[]']
            url = request.POST.get('url')
            place =request.POST.get('place')
            city =request.POST.get('city')
            file_type = imghdr.what(uploaded_file)
            if not file_type:

                return render(request, "upload.html", {"alert": "Unsupported file type"})

            filename = uploaded_file.name
            data = {
                'Filename':filename,
                'Place':place,
                'City':city,
                    }
            # Save the uploaded file to a temporary location
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            response = process_image(request,temp_path,url,data)
            
            # Clean up temporary file
            os.remove(temp_path)

            return response
        else:
            return render(request, "upload.html", {"alert": "No file found"})
    else:
        return render(request, "upload.html", {"alert": "Invalid request method"})

def process_image(request,image_path,img_url,data):
    import time
    from datetime import datetime, timezone
    import pytz 

    id = request.session['uid']
    a = authe.get_account_info(id)
    a = a['users']
    a = a[0]
    a = a['localId'] # Getting local id of user

    try:
        # Open image and read EXIF data
        with open(image_path, 'rb') as src:
            img = ExifImage(src)

        # Check if image contains EXIF data and GPS information
        if not img.has_exif or not hasattr(img, 'gps_latitude') or not hasattr(img, 'gps_longitude'):
            return render(request, "upload.html", {"alert": "Image does not contain GPS EXIF data"})

        # Function to convert GPS coordinates to decimal format
        def decimal_coords(coords, ref):
            decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
            if ref in ('S', 'W'):
                decimal_degrees = -decimal_degrees
            return decimal_degrees

        # Get latitude and longitude in decimal format
        lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
        lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)


        # Create a temporary HTML file with the location marked on Google Maps
        output_path = os.path.join(tempfile.gettempdir(), f'{os.path.basename(image_path)}-location.html')
        gmap = gmplot.GoogleMapPlotter(lat, lon, 12)
        gmap.marker(lat, lon, 'red')
        gmap.draw(output_path)

        # Get address using reverse geocoding
        address = Nominatim(user_agent='GetLoc')
        location = address.reverse(f'{lat}, {lon}')

        print("file details:")
        # Update data dictionary with location information
        data.update({
            'Url':img_url,
            'Lat': lat,
            'Lon': lon,
            'Location': location.address,
            'Uploaded by':a,
        })
        # Print various details for debugging
        print(data['Filename'])
        print(img_url)
        print(data['Lat'])
        print(data['Lon'])
        print(data['Place'])
        print(data['City'])
        print(data['Location'])
        print(data['Url'])
        print(data['Uploaded by'])
        print()

        # Get the current time in a specific timezone and convert to milliseconds
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        print(millis)

        # Upload the data to realtime database
        database.child("Hidden_places").child(millis).child("Details").set(data)

        google_maps_url = f"https://www.google.com/maps/dir//{location.address[0:30]}/@{lat},{lon},20z"
        print(google_maps_url)
        return HttpResponseRedirect("/postsign")
        # return render(request, "upload.html", {"alert": "File uploaded successfully", "url": google_maps_url})
        # return render(request, "images.html", {"alert": "Info submitted successfully"})
    except Exception as e:
        return render(request, "upload.html", {"alert": f"An error occurred while submitting info: {str(e)}"})
