import ctypes
from pyueye import ueye
from idsControlUtils import (uEyeException, Rect, get_bits_per_pixel,
                                  ImageBuffer, check)

class Camera:
    """
    Camera class allows to derive a camera object wich holds an
    handle to the physical camera. Also it contains all functions
    needed to configure and communicate with the hardware.
    """
    def __init__(self, device_id=0):
        """
        Initializing function.
        """
        self.h_cam = ueye.HIDS(device_id)
        self.img_buffers = []
        self.img_buffer = ImageBuffer()
        self.image_file_params = ueye.IMAGE_FILE_PARAMS()

    def __enter__(self):
        """
        Enable usage of "with"-Statement.
        """
        self.init()
        return self

    def __exit__(self, _type, value, traceback):
        """
        Enable usage of "with"-Statement.
        """
        self.exit()

    def handle(self):
        """
        Returns Camera Handle
        """
        return self.h_cam

    def alloc(self, buffer_count=3):
        """
        Allocates a series of image buffers. Image buffers are appended
        to the img_buffers variable of the camera class.
        """
        rect = self.get_aoi()
        bpp = get_bits_per_pixel(self.get_colormode())

        for buff in self.img_buffers:
            check(ueye.is_FreeImageMem(self.h_cam, buff.mem_ptr, buff.mem_id))

        for _ in range(buffer_count):
            buff = ImageBuffer()
            ueye.is_AllocImageMem(self.h_cam,
                                  rect.width, rect.height, bpp,
                                  buff.mem_ptr, buff.mem_id)

            check(ueye.is_AddToSequence(self.h_cam, buff.mem_ptr, buff.mem_id))

            self.img_buffers.append(buff)

        ueye.is_InitImageQueue(self.h_cam, 0)

    def alloc_mem(self):
        """
        Allocates a single image buffer. Allocated memory is handed over
        to the img_buffer variable of the camera class.
        """
        rect = self.get_aoi()
        bpp = get_bits_per_pixel(self.get_colormode())

        ueye.is_AllocImageMem(self.h_cam,
                              rect.width, rect.height, bpp,
                              self.img_buffer.mem_ptr, self.img_buffer.mem_id)

        check(ueye.is_SetImageMem(self.h_cam, self.img_buffer.mem_ptr, self.img_buffer.mem_id))

    def free_mem(self):
        """
        Frees allocated image buffer.
        """
        check(ueye.is_FreeImageMem(self.h_cam, self.img_buffer.mem_ptr, self.img_buffer.mem_id))

    def init(self):
        """
        Starts the driver and establishes the connection to the camera.
        """
        ret = ueye.is_InitCamera(self.h_cam, None)
        if ret != ueye.IS_SUCCESS:
            self.h_cam = None
            raise uEyeException(ret)

        return ret

    def exit(self):
        """
        Disables the camera handle and releases the data structures and memory areas.
        """
        ret = None
        if self.h_cam is not None:
            ret = ueye.is_ExitCamera(self.h_cam)
        if ret == ueye.IS_SUCCESS:
            self.h_cam = None

    def get_aoi(self):
        """
        Get current configured AOI.
        Returns:
            Rect object that contains position and size of AOI on sensor.
        """
        rect_aoi = ueye.IS_RECT()
        ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_GET_AOI, rect_aoi, ueye.sizeof(rect_aoi))

        return Rect(rect_aoi.s32X.value,
                    rect_aoi.s32Y.value,
                    rect_aoi.s32Width.value,
                    rect_aoi.s32Height.value)

    def set_aoi(self, x, y, width, height):
        """
        Sets the area of interrest on the sensor.
        Args:
            x, y            :   Pixelpositions to define upper left edge of AOI.
            width, height   :   Width and Height of AOI in pixel.
        """
        rect_aoi = ueye.IS_RECT()
        rect_aoi.s32X = ueye.int(x)
        rect_aoi.s32Y = ueye.int(y)
        rect_aoi.s32Width = ueye.int(width)
        rect_aoi.s32Height = ueye.int(height)

        return ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_SET_AOI, rect_aoi, ueye.sizeof(rect_aoi))

    def capture_video(self, wait=False):
        """
        Start Livevideo mode.
        """
        wait_param = ueye.IS_WAIT if wait else ueye.IS_DONT_WAIT
        return ueye.is_CaptureVideo(self.h_cam, wait_param)

    def stop_video(self):
        return ueye.is_StopLiveVideo(self.h_cam, ueye.IS_FORCE_VIDEO_STOP)

    def freeze_video(self, wait=False):
        """
        Softwaretrigger for taking images.
        """
        wait_param = ueye.IS_WAIT if wait else ueye.IS_DONT_WAIT
        return ueye.is_FreezeVideo(self.h_cam, wait_param)

    def set_colormode(self, colormode):
        """
        Set the colormode for the camera.
        Args:
            colormode: Int  : Integer constant of colormode (see Manual)
        """
        check(ueye.is_SetColorMode(self.h_cam, colormode))

    def get_colormode(self):
        """
        Get current configured colormode.
        Returns:
            Integer constant of colormode (see Manual)
        """
        ret = ueye.is_SetColorMode(self.h_cam, ueye.IS_GET_COLOR_MODE)
        return ret
    
    def get_format_list(self):
        count = ueye.UINT()
        check(ueye.is_ImageFormat(self.h_cam,
                                  ueye.IMGFRMT_CMD_GET_NUM_ENTRIES,
                                  count,
                                  ueye.sizeof(count)))
        format_list = ueye.IMAGE_FORMAT_LIST(ueye.IMAGE_FORMAT_INFO * count.value)
        format_list.nSizeOfListEntry = ueye.sizeof(ueye.IMAGE_FORMAT_INFO)
        format_list.nNumListElements = count.value
        check(ueye.is_ImageFormat(self.h_cam, ueye.IMGFRMT_CMD_GET_LIST,
                                  format_list, ueye.sizeof(format_list)))
        return format_list
    
    def to_file(self, path, dtype, quality=100):
        """
        Save an image directly to a file.
        Args:
            part: String    :   Path to destination (with Filename)
            dtype: filetype :   Type of Imagefile (defined in pyueye)
            quality: int    :   Quality of Image (100 equals lossless)
        Returns:
            error code (see API Documentation)
        """
        self.image_file_params.pwchFileName = path
        self.image_file_params.nFileType = dtype
        self.image_file_params.nQuality = quality
        self.image_file_params.ppcImageMem = None
        self.image_file_params.pnImageID = None
        ret = ueye.is_ImageFile(self.h_cam,
                                ueye.IS_IMAGE_FILE_CMD_SAVE,
                                self.image_file_params,
                                ueye.sizeof(self.image_file_params))
        return ret

    def set_exposure(self, exposure_time):
        """
        Sets the exposure time.
        Args:
            exposure_time: Double   : exposure time in milliseconds
        Returns:
            error code (see API Documentation)
        """
        ret = ueye.is_Exposure(self.h_cam,
                               ueye.IS_EXPOSURE_CMD_SET_EXPOSURE,
                               ueye.DOUBLE(exposure_time),
                               8)
        return ret

    def get_exposure(self):
        """
        Read out exposure time.
        Args:
            None
        Returns:
            exposure time in milliseconds.
        """
        exposure_time = ueye.DOUBLE()
        ueye.is_Exposure(self.h_cam,
                         ueye.IS_EXPOSURE_CMD_GET_EXPOSURE,
                         exposure_time,
                         ueye.sizeof(exposure_time))
        return exposure_time

    def get_exposure_range(self):
        """
        Read out range of possible exposure times.
        Args:
            None
        Returns:
            Array that contains range information [min, max, increment]
        """
        exposure_range = (ctypes.c_double*3)()
        ueye.is_Exposure(self.h_cam,
                         ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE,
                         exposure_range,
                         24)
        return exposure_range

    def get_long_exposure_range(self):
        """
        Get range of long exposure mode.
        Returns:
            Array that contains range information [min, max, increment]
        """
        long_exposure_range = (ctypes.c_double*3)()
        ueye.is_Exposure(self.h_cam,
                         ueye.IS_EXPOSURE_CMD_GET_LONG_EXPOSURE_RANGE,
                         long_exposure_range,
                         24)
        return long_exposure_range

    def enable_long_exposure(self):
        """
        Enable long exposure mode.
        """
        ueye.is_Exposure(self.h_cam,
                         ueye.IS_EXPOSURE_CMD_SET_LONG_EXPOSURE_ENABLE,
                         ueye.UINT(1),
                         ueye.sizeof(ueye.UINT()))

    def disable_long_exposure(self):
        """
        Disable long exposure mode.
        """
        ueye.is_Exposure(self.h_cam,
                         ueye.IS_EXPOSURE_CMD_SET_LONG_EXPOSURE_ENABLE,
                         ueye.UINT(0),
                         ueye.sizeof(ueye.UINT()))

    def get_supported_pixelclocks(self):
        """
        Read out range of supported pixel clocks.
        Args:
            None
        Returns:
            Tuple of int and array (number_of_supported_clocks, [int * number_of_supported_clocks])
        """
        number_of_supported_clocks = ctypes.c_uint()
        ueye.is_PixelClock(self.h_cam,
                           ueye.IS_PIXELCLOCK_CMD_GET_NUMBER,
                           number_of_supported_clocks,
                           ueye.sizeof(ctypes.c_uint))

        clock_list = (ctypes.c_uint*number_of_supported_clocks.value)()
        ueye.is_PixelClock(self.h_cam,
                           ueye.IS_PIXELCLOCK_CMD_GET_LIST,
                           clock_list,
                           ueye.sizeof(clock_list))

        return (number_of_supported_clocks, clock_list)

    def get_pixelclock(self):
        """
        Get current pixelclock
        Returns:
            Int value of current pixelclock in Megahertz
        """
        pixelclock = ueye.UINT()
        ueye.is_PixelClock(self.h_cam,
                           ueye.IS_PIXELCLOCK_CMD_GET,
                           pixelclock,
                           ueye.sizeof(pixelclock))
        return pixelclock

    def set_pixelclock(self, pixelclock):
        """
        Set pixelclock. CAUTION: Pixelclock must be a supported value!!!
        Args:
            pixelclock: int     : Pixelclock in Megahertz
        Returns:
            error code (see API Documentation)
        """
        ret = ueye.is_PixelClock(self.h_cam,
                                 ueye.IS_PIXELCLOCK_CMD_SET,
                                 ueye.UINT(pixelclock),
                                 ueye.sizeof(ueye.UINT(pixelclock)))
        return ret

    def get_frame_time_range(self):
        """
        Get range of possible frame times.
        Returns:
            Array that contains range information [min, max, increment]
        """
        frame_time_min = ueye.DOUBLE()
        frame_time_max = ueye.DOUBLE()
        frame_time_interval = ueye.DOUBLE()
        check(ueye.is_GetFrameTimeRange(self.h_cam,
                                        frame_time_min,
                                        frame_time_max,
                                        frame_time_interval))
        return (frame_time_min, frame_time_max, frame_time_interval)

    def get_frame_rate_range(self):
        """
        Get range of minimal and maximal framerates.
        Returns:
            Array that contains range information [min, max]
        """
        tmin, tmax, _ = self.get_frame_time_range()
        return(1/tmax, 1/tmin)

    def set_frame_rate(self, frame_rate):
        """
        Sets the frame rate
        Args:
            frame_rate: double     : value of framerate
        Returns:
            Value of new framerate (may differ from input parameter)
        """
        new_frame_rate = ueye.DOUBLE()
        ueye.is_SetFrameRate(self.h_cam,
                             ueye.double(frame_rate),
                             new_frame_rate)
        return new_frame_rate

    def set_trigger_mode(self, mode):
        """
        Sets the cameras trigger mode
        Args:
            mode:   predefined trigger mode (see ueye manual)
        """
        check(ueye.is_SetExternalTrigger(self.handle(), mode))