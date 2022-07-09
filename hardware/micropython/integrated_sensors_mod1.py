from ds18b20 import ds18b20
from mqtt import MqttConnection
from json import load


class integrated_module1():

    def __init__(self, 
                 ds18b20_pin_number:    int,
                 mqtt_config_file:      str):

        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the MQTT connection
        with open(mqtt_config_file) as f:
            self.mqtt_config = load(f)
 

        # creates de connection object and connects esp32 to the MQTT broker
        self.mqtt_client = MqttConnection(**self.mqtt_config)
        self.mqtt_client.mqtt_connect()

        # creates the ds18b20 object with the given pin_number 
        self.ds18b20 = ds18b20(pin_number = ds18b20_pin_number)


    def configure_send_data(self):

        """
            This function configures the MQTT client to publish the data from the
            selected sensors, using a simple sintaxis:

            self.mqtt_client.pub_topics[alias]["exec"] = function_to_be_executed

            were the function_to_be_executed is a function that returns the data
            from the sensor.
        """

        self.mqtt_client.pub_topics["wtemp"]["exec"] = self.ds18b20.read_temperature 
        self.mqtt_client.pub_topics["ec"]["exec"]    = self.ds18b20.read_temperature 


    def send_data(self):

        """
            This function sends data to all the topics that exist in the 'pub_topics'
            field from the 'mqtt_config.json' file.

            Its mandatory for the dictionary 'self.mqtt_client.pub_topics' to have 
            the following structure:

            {
                "alias": { "exec": function_to_be_executed,
                           "topic": topic_to_be_published, 
                           "qos": qos_to_be_used
                         },
                        
                        ...
 
                "alias": { "exec": function_to_be_executed,
                           "topic": topic_to_be_published, 
                           "qos": qos_to_be_used
                         }
            }

            if no "exec" field is present with correspondig function_to_be_executed,
            no data will be sent tho that topic.

        """

        for alias in self.mqtt_client.pub_topics.keys():

            if "exec" in self.mqtt_client.pub_topics[alias].keys():

                self.mqtt_client.publish( topic = self.mqtt_client.pub_topics[alias]["topic"],
                                          msg   = self.mqtt_client.pub_topics[alias]["exec"](),
                                          qos   = self.mqtt_client.pub_topics[alias]["qos"]     )







