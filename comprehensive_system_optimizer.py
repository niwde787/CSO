bl_info = {
    "name": "Comprehensive Auto System Optimizer",
    "blender": (3, 0, 0),
    "category": "System",
    "author": "Your Name",
    "version": (1, 0, 0),
    "description": "Configures Blender settings based on system hardware, including GPU and RAM optimizations.",
}

import bpy
import platform
import subprocess

# GPU Detection
def get_gpu_info():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("wmic path win32_videocontroller get name", shell=True)
            return output.decode().split("\n")[1].strip()
        elif platform.system() == "Linux":
            output = subprocess.check_output("lspci | grep -i vga", shell=True)
            return output.decode().split(":")[1].strip()
        elif platform.system() == "Darwin":
            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).decode()
            for line in output.split("\n"):
                if "Chipset Model" in line:
                    return line.split(":")[-1].strip()
    except Exception as e:
        return f"Unknown GPU: {e}"

# RAM Detection
def get_ram_info():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("wmic ComputerSystem get TotalPhysicalMemory", shell=True)
            ram_bytes = int(output.decode().split("\n")[1].strip())
        elif platform.system() == "Linux":
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
            mem_total_line = next(line for line in lines if "MemTotal" in line)
            ram_kb = int(mem_total_line.split()[1])
            ram_bytes = ram_kb * 1024
        elif platform.system() == "Darwin":
            output = subprocess.check_output(["sysctl", "hw.memsize"]).decode()
            ram_bytes = int(output.split(":")[1].strip())
        else:
            ram_bytes = 0
        return ram_bytes / (1024 ** 3)  # Convert bytes to GB
    except Exception as e:
        return 0

# Determine GPU-Based Settings
def get_max_resolution_and_samples(gpu):
    if "NVIDIA RTX 3090" in gpu or "AMD RX 6900 XT" in gpu:
        return (3840, 2160, 1024)  # 4K resolution, high samples
    elif "NVIDIA GTX 1660" in gpu or "AMD RX 580" in gpu:
        return (2560, 1440, 512)  # 1440p resolution, medium samples
    else:
        return (1920, 1080, 128)  # 1080p resolution, low samples

# Main Configuration Function
def configure_blender():
    # Get hardware details
    gpu = get_gpu_info()
    ram = get_ram_info()
    print(f"Detected GPU: {gpu}")
    print(f"Detected RAM: {ram:.1f} GB")

    # Determine GPU-based settings
    width, height, max_samples = get_max_resolution_and_samples(gpu)
    print(f"Setting Resolution: {width}x{height}, Max Samples: {max_samples}")

    try:
        # Ensure Cycles engine is active
        if bpy.context.scene.render.engine != 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'

        # Set resolution and samples
        bpy.context.scene.render.resolution_x = width
        bpy.context.scene.render.resolution_y = height
        bpy.context.scene.cycles.samples = max_samples

        # RAM-based settings
        if hasattr(bpy.context.preferences.system, 'memory_cache_limit'):
            if ram < 8:
                bpy.context.preferences.system.memory_cache_limit = 4096  # 4GB
            elif 8 <= ram < 16:
                bpy.context.preferences.system.memory_cache_limit = 8192  # 8GB
            else:
                bpy.context.preferences.system.memory_cache_limit = 16384  # 16GB
            print(f"Memory Cache Limit Set: {bpy.context.preferences.system.memory_cache_limit} MB")

        return f"Settings applied: Resolution {width}x{height}, Samples {max_samples}, RAM Cache {bpy.context.preferences.system.memory_cache_limit} MB"
    except Exception as e:
        return f"Error applying settings: {e}"

# Blender UI Operator
class SystemOptimizerOperator(bpy.types.Operator):
    """Optimize Blender settings based on system hardware"""
    bl_idname = "system.auto_optimizer"
    bl_label = "Auto System Optimizer"

    def execute(self, context):
        message = configure_blender()
        self.report({'INFO'}, message)
        return {'FINISHED'}

# Blender UI Panel
class SystemOptimizerPanel(bpy.types.Panel):
    """Creates a Panel in the Preferences -> System tab"""
    bl_label = "Comprehensive Auto System Optimizer"
    bl_idname = "PREFERENCES_PT_auto_optimizer"
    bl_space_type = 'PREFERENCES'
    bl_region_type = 'WINDOW'
    bl_context = "system"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Optimize Blender Settings:")
        layout.operator(SystemOptimizerOperator.bl_idname, text="Run Optimizer")

# Registration Functions
def register():
    bpy.utils.register_class(SystemOptimizerOperator)
    bpy.utils.register_class(SystemOptimizerPanel)

def unregister():
    bpy.utils.unregister_class(SystemOptimizerOperator)
    bpy.utils.unregister_class(SystemOptimizerPanel)

if __name__ == "__main__":
    register()
