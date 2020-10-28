from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

config_object.read("config.ini")

#Get the key
default = config_object["default"]
print("Blur is {}".format(default["blur"]))