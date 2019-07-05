
import base64
import vehicle_flagrant_msg
import status_radar_msg

with open("teste.jpg", "rb") as img_file:
    img1 = base64.b64encode(img_file.read())

with open("teste.jpg", "rb") as img_file:
    img2 = base64.b64encode(img_file.read())
print '1'
veiculo = {
            "id_radar": 1,
            "image1": img1,
            "image2": img2,
            "infraction": 2,
            "vehicle_speed": 30,
            "considered_speed": 40,
            "max_allowed_speed": 10
}
print '2'
vehicle_flagrant_msg.send_vehicle_flagrant(veiculo)
 
