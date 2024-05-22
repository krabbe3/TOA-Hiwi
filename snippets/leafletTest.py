import folium
import webbrowser

# Define coordinates of where we want to center our map (center to mean of the loc result)
map_bounds = [self._pos_base['latitude'], self._pos_base['longitude']]

#Create the map
my_map = folium.Map(location = map_bounds, zoom_start = 16, max_zoom=19, control_scale = True)

# plot all estimated node positions in the map
def plotDot(position, label, color):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=position,
                        radius=2,
                        weight=5,
                        color=color).add_child(folium.Popup(label)).add_to(my_map)

for idx, position in enumerate(pos_upper):
    if (position[0] == np.inf) or (position[1] == np.inf):
        continue
    plotDot(position, label, 'red')

for idx, position in enumerate(pos_lower):
    if (position[0] == np.inf) or (position[1] == np.inf):
        continue
    plotDot(position, label, 'blue')

# Add the positions of the basestations + solver init 
folium.Marker([self._pos_base['latitude'], self._pos_base['longitude']], popup = 'helmholtz', icon=folium.Icon(icon_color='white', color="black", icon="tower-cell", prefix='fa')).add_to(my_map)
folium.Marker([self._pos_sat1['latitude'], self._pos_sat1['longitude']], popup = 'pöhö', icon=folium.Icon(icon_color='white', color="black", icon="tower-cell", prefix='fa')).add_to(my_map)
folium.Marker([self._pos_sat2['latitude'], self._pos_sat2['longitude']], popup = 'iwg', icon=folium.Icon(icon_color='white', color="black", icon="tower-cell", prefix='fa')).add_to(my_map)
folium.Marker([self._pos_dab['latitude'], self._pos_dab['longitude']], popup = 'dab_station', icon=folium.Icon(icon_color='black', color="grey", icon="tower-broadcast", prefix='fa')).add_to(my_map)
folium.Marker([self._pos_solver['latitude'], self._pos_solver['longitude']], popup="solver_init",icon=folium.Icon(color="black", icon="info-sign")).add_to(my_map)


# Do stuff if real node position is known
if self._node_lat is not None:
    
    # calculate the radius of the circles around the basestation
    bs0 = (self._pos_base['latitude'], self._pos_base['longitude'])
    bs1 = (self._pos_sat1['latitude'], self._pos_sat1['longitude'])
    bs2 = (self._pos_sat2['latitude'], self._pos_sat2['longitude'])
    node = (self._node_lat, self._node_long)
    
    node_base = geopy.distance.geodesic((bs0), (node)).m
    node_sat1 = geopy.distance.geodesic((bs1), (node)).m
    node_sat2 = geopy.distance.geodesic((bs2), (node)).m
    
    
    # draw circles around the basestations
    iframe = folium.IFrame("hypothetical node position according to station helmholtz with distance of {dist} m between station helmholtz and node".format(dist=round(node_base, 2)))
    popup = folium.Popup(iframe, min_width=500, max_width=500)
    folium.Circle(location=[self._pos_base['latitude'], self._pos_base['longitude']], popup=popup, fill_color='black', radius=node_base, weight=4, color="black").add_to(my_map)
    iframe = folium.IFrame("hypothetical node position according to station helmholtz with distance of {dist} m between station pöhö and node".format(dist=round(node_sat1, 2)))
    popup = folium.Popup(iframe, min_width=500, max_width=500)
    folium.Circle(location=[self._pos_sat1['latitude'], self._pos_sat1['longitude']], popup=popup, fill_color='black', radius=node_sat1, weight=4, color="black").add_to(my_map)
    iframe = folium.IFrame("hypothetical node position according to station helmholtz with distance of {dist} m between station iwg and node".format(dist=round(node_sat2, 2)))
    popup = folium.Popup(iframe, min_width=500, max_width=500)
    folium.Circle(location=[self._pos_sat2['latitude'], self._pos_sat2['longitude']], popup=popup, fill_color='black', radius=node_sat2, weight=4, color="black").add_to(my_map)
    
    # draw node in map with meta information
    iframe = folium.IFrame(" ID: {node_id} <br> \
                            lat: {lat} <br> \
                            long:{long} <br> \
                            alt: {alt} <br> \
                            interval: {interval} <br> \
                            mode: {mode} <br> \
                            pattern: {pattern} <br>".format(node_id=node_id, lat=self._node_lat, long=self._node_long, alt=self._node_alt, interval=self._node_interval, mode=self._node_mode, pattern=self._node_pattern))
    popup = folium.Popup(iframe, min_width=500, max_width=500)
    folium.Marker([self._node_lat, self._node_long], popup=popup, icon=folium.Icon(icon_color='black', color="green", icon="map-pin", prefix='fa')).add_to(my_map)

#Display the map
save_map = LOC_PATH + str(node_id) + '_calib.html'
my_map.save(save_map)
#webbrowser.open(save_map)