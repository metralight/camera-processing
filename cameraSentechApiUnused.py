"""
This sample shows how to process received image with filter and converter.
The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Acquire image data
 - Apply image processing with StApi filter and converter.
 - Copy image data for OpenCV
 - Preview image using OpenCV
 Note: opencv-python and numpy packages are required:
    pip install numpy
    pip install opencv-python
"""

import cv2
import numpy as np
import stapipy as st
import time
import logging
import ipaddress



class Camera:

    # Image scale when displaying using OpenCV.
    DISPLAY_RESIZE_FACTOR = 0.5

    # remote device
    st_device = None

    # host datastream
    st_datastream = None

    GEV_DEVICE_FORCE_IP_ADDRESS = "GevDeviceForceIPAddress"
    GEV_DEVICE_FORCE_SUBNET_MASK = "GevDeviceForceSubnetMask"
    GEV_DEVICE_FORCE_IP = "GevDeviceForceIP"

    ACQUISITION_FRAME_RATE = "AcquisitionFrameRate"

    IP = "10.90.103.180"

    def __init__(self):
        # Initialize StApi before using.
        st.initialize()

        # Create a system object for device scan and connection.
        st_system = st.create_system(st.EStSystemVendor.Default, st.EStInterfaceType.GigEVision)
        
        # Connect to first detected device.
        # self.st_device = st_system.create_first_device()
        deviceFound = False
        for index in range(st_system.interface_count):
            st_interface = st_system.get_interface(index)
            if st_interface.device_count > 0:
                deviceFound = True
                break
            
        if not deviceFound:
            logging.error("No device found")
            exit(-1)

        
        self.setIp(self.IP, st_interface.port.nodemap)

        for i in range(30):
            time.sleep(1)
            self.st_device = self.createDeviceOnIp(st_interface, self.IP)
            if self.st_device:
                break
        if self.st_device is None:
            raise Exception(f"A device ip IP address {self.IP} could not be found")
        logging.debug(self.st_device.remote_port.nodemap.get_nodes_name())

        # Display DisplayName of the device.
        logging.info(f'Connected device: {self.st_device.info.display_name}')

        # Create a datastream object for handling image stream data.
        self.st_datastream = self.st_device.create_datastream()

        self.ConfigureCamera(self.st_device)


    def ConfigureCamera(self, st_device):
        acqFps = st_device.remote_port.nodemap.get_node(self.ACQUISITION_FRAME_RATE)
        acqFps.value = 3


    def setIp(self, ip, nodemap):
        # Specify the new ip address of the device.
        force_ip = nodemap.get_node(self.GEV_DEVICE_FORCE_IP_ADDRESS)
        force_ip.value = int(ipaddress.ip_address(ip))

        # Specify the new subnet mask of the device.
        force_mask = nodemap.get_node(self.GEV_DEVICE_FORCE_SUBNET_MASK)
        force_mask.value = int(ipaddress.ip_address("255.255.255.0"))

        # Update the device setting.
        force_ip_cmd = nodemap.get_node(self.GEV_DEVICE_FORCE_IP).get()
        force_ip_cmd.execute()


    def createDeviceOnIp(self, pinterface, ipAddrStr : str) -> st.PyStDevice:
        """
        Function to connect to device based on the given ip address.

        :param pinterface PyStDevice: interface of the device.
        :param ipAddrStr: IP address of the device in string.
        :return: connected device (PyStDevice).
        """
        pinterface.update_device_list()
        iface_nodemap = pinterface.port.nodemap
        device_selector = iface_nodemap.get_node("DeviceSelector").get()
        max_index = device_selector.max
        device_ip = iface_nodemap.get_node("GevDeviceIPAddress")
        for index in range(max_index+1):
            device_selector.value = index
            if device_ip.is_available:
                if device_ip.value == int(ipaddress.ip_address(ipAddrStr)):
                    return pinterface.create_device_by_index(index)
        return None

    def StartGrab(self):
        # Create a converter object for converting pixel format to BGR8.
        st_converter_pixelformat = st.create_converter(st.EStConverterType.PixelFormat)
        st_converter_pixelformat.destination_pixel_format = st.EStPixelFormatNamingConvention.BGR8

        # Start the image acquisition of the host (local machine) side.
        self.st_datastream.start_acquisition()

        # Start the image acquisition of the camera side.
        self.st_device.acquisition_start()

        # A while loop for acquiring data and checking status
        while self.st_datastream.is_grabbing:
            # Create a localized variable st_buffer using 'with'
            # Warning: if st_buffer is in a global scope, st_buffer must be
            #          assign to None to allow Garbage Collector release the buffer
            #          properly.
            with self.st_datastream.retrieve_buffer() as st_buffer:
                # Check if the acquired data contains image data.
                if st_buffer.info.is_image_present:
                    # Filter and convert the acquired image.
                    # st_image = st_filter_edge.apply_filter(st_buffer.get_image())
                    # st_image = st_converter_pixelformat.convert(st_image)
                    
                    st_image = st_converter_pixelformat.convert(st_buffer.get_image())

                    # Display the information of the acquired image data.
                    print("BlockID={0} Size={1} x {2} First Byte={3}".format(
                        st_buffer.info.frame_id,
                        st_image.width, st_image.height,
                        st_image.get_image_data()[0]))

                    # Get raw image data.
                    data = st_image.get_image_data()

                    nparr = np.frombuffer(data, np.uint8)

                    # Process image for displaying the BGR8 image.
                    nparr = nparr.reshape(st_image.height, st_image.width, 3)

                    # Resize image.and display.
                    # nparr = cv2.resize(nparr, None, fx=DISPLAY_RESIZE_FACTOR, fy=DISPLAY_RESIZE_FACTOR)
                    cv2.imshow('image', nparr)
                    cv2.waitKey(1)
                else:
                    # If the acquired data contains no image data.
                    print("Image data does not exist.")

        # Stop the image acquisition of the camera side
        self.st_device.acquisition_stop()

        # Stop the image acquisition of the host side
        self.st_datastream.stop_acquisition()


if __name__ == '__main__':
    from logs import ConfigureLogging
    ConfigureLogging(10, name="cam")

    cam = Camera()
    cam.StartGrab()
