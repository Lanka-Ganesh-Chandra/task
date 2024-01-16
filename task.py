import ctypes
import psutil
import platform
import socket
import speedtest
import cpuinfo
import GPUtil
import wmi
import screeninfo

def get_installed_software():
    software_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        software_list.append(proc.info['name'])
    return set(software_list)

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    return download_speed, upload_speed

def get_screen_resolution():
    try:
        
        screen = screeninfo.get_monitors()[0]
        return f"{screen.width}x{screen.height}"
    except ImportError:
        return "Screen resolution not available (install screeninfo library)"

def get_cpu_info():
    cpu_info = cpuinfo.get_cpu_info()
    cpu_brand = cpu_info.get('brand', cpu_info.get('brand_raw', 'N/A'))
    # return cpu_info['brand'], psutil.cpu_count(logical=False), psutil.cpu_count()
    return cpu_brand, psutil.cpu_count(logical=False), psutil.cpu_count()

def get_gpu_info():
    try:
        GPUs = GPUtil.getGPUs()
        if GPUs:
            return GPUs[0].name
    except ImportError:
        return "GPU information not available (install gputil library)"

def get_ram_size():
    ram_size = psutil.virtual_memory().total // (1024 ** 3)  # Convert to GB
    return round(ram_size, 2)

def get_dpi():
    hdc = ctypes.windll.user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 corresponds to LOGPIXELSX
    ctypes.windll.user32.ReleaseDC(0, hdc)
    return dpi

def get_screen_size():
    try:
        dpi = get_dpi()
        # Assume standard DPI of 96, adjust as needed
        width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
        diagonal_pixels = (width**2 + height**2)**0.5
        diagonal_inches = diagonal_pixels / dpi
        return f"{diagonal_inches:.2f} inch"
    except Exception as e:
        return f"Screen size not available: {str(e)}"

def get_wifi_mac_address():
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if "Wi-Fi" in interface and addr.family == psutil.AF_LINK:
                    return addr.address
        return "Wi-Fi MAC Address not available"
    except Exception as e:
        return str(e)

def get_public_ip():
    try:
        public_ip = socket.gethostbyname(socket.gethostname())
        return public_ip
    except socket.gaierror:
        return "Public IP not available"

def get_windows_version():
    return platform.win32_ver()

if __name__ == "__main__":
    print("Installed Software:", get_installed_software())
    print()
    download_speed, upload_speed = get_internet_speed()
    print(f"Internet Speed: Download {download_speed:.2f} Mbps, Upload {upload_speed:.2f} Mbps")
    print("Screen Resolution:", get_screen_resolution())
    cpu_model, cpu_cores, cpu_threads = get_cpu_info()
    print(f"CPU Model: {cpu_model}, Cores: {cpu_cores}, Threads: {cpu_threads}")
    print("GPU Model:", get_gpu_info())
    print("RAM Size:", get_ram_size(), "GB")
    print("Screen Size:", get_screen_size())
    print("MAC Address:", get_wifi_mac_address())
    print("Public IP Address:", get_public_ip())
    print("Windows Version:", get_windows_version())
