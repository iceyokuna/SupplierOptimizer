class MapController:
    def __init__(self):
        self.customer_lat = ""
        self.customer_lon = ""
        self.supplier_lat = ""
        self.supplier_lon = ""
        self.html = ""

    def setCustomerMarker(self, lat, lon):
        self.customer_lat = lat
        self.customer_lon = lon

    def setSupplierMarker(self, lat, lon):
        self.supplier_lat = lat
        self.supplier_lon = lon
        
    def setHTML(self, html):
        self.html = html
        
    def getHTML(self):
        return '''<!DOCTYPE html>
<html>
  <head>
    <title>Place ID Finder</title>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      #map {
        height: 100%;
      }

      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      .controls {
        background-color: #fff;
        border-radius: 2px;
        border: 1px solid transparent;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        box-sizing: border-box;
        font-family: Roboto;
        font-size: 15px;
        font-weight: 300;
        height: 29px;
        margin-left: 17px;
        margin-top: 10px;
        outline: none;
        padding: 0 11px 0 13px;
        text-overflow: ellipsis;
        width: 400px;
      }

      .controls:focus {
        border-color: #4d90fe;
      }
      .title {
        font-weight: bold;
      }
      #infowindow-content {
        display: none;
      }
      #map #infowindow-content {
        display: inline;
      }

    </style>
  </head>
  <body>
    <input id="pac-input" class="controls" type="text"
        placeholder="Enter a location">
    <div id="map"></div>
    <div id="infowindow-content">
      <span id="place-name"  class="title"></span><br>
      Place ID <span id="place-id"></span><br>
      <span id="place-address"></span>
    </div>

    <script>
    var supply_label = 'S'
    var customer_label = 'C'
    var glo_pid = 0;
    var glo_plo = 0;
    glo_pn = 0;
    
      function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: '''+self.customer_lat+''', lng: '''+self.customer_lon+'''},
          zoom: 13
        });
        var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
          var marker = new google.maps.Marker({
            position: {lat: '''+self.customer_lat+''', lng: '''+self.customer_lon+'''},
            map: map,
            icon: image
        });
        marker.setAnimation(google.maps.Animation.BOUNCE);

          var marker2 = new google.maps.Marker({
            position: {lat: '''+self.supplier_lat+''', lng: '''+self.supplier_lon+'''},
            map: map,
        });
        marker2.setAnimation(google.maps.Animation.BOUNCE);

        var input = document.getElementById('pac-input');

        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.bindTo('bounds', map);

        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        var infowindow = new google.maps.InfoWindow();
        var infowindowContent = document.getElementById('infowindow-content');
        infowindow.setContent(infowindowContent);
        var marker = new google.maps.Marker({
          map: map
        });
        
        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });

        autocomplete.addListener('place_changed', function() {
          infowindow.close();
          var place = autocomplete.getPlace();
          if (!place.geometry) {
            return;
          }
          if (!place.id) {
            return;
          }
          
    
          if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
          } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
          }

          // Set the position of the marker using the place ID and location.
          marker.setPlace({
            placeId: place.place_id,
            location: place.geometry.location
          });
          glo_pid = place.place_id;
          glo_pn = place.name;
          glo_plo = place.formatted_address;
          marker.setVisible(true);

          infowindowContent.children['place-name'].textContent = place.name;
          infowindowContent.children['place-id'].textContent = place.place_id;
          infowindowContent.children['place-address'].textContent =
              place.formatted_address;
          infowindow.open(map, marker);
        });
      }
      function get_placeid(){
      if(glo_pid == 0)
    alert('nothing selected');
      return glo_pid;
      };
      
      function get_name(){
      if(glo_pn == "")
    alert('nothing selected');
      return glo_pn;
      };

      function get_location(){
      if(glo_plo == "")
    alert('nothing selected');
      return glo_plo;
      };
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBmt-IXSmfgH8AsEYAalEUgXuF23GCuNVQ&libraries=places&callback=initMap"
        async defer></script>
  </body>
</html>'''

    
    
