Comprehensive Auto System Optimizer

Overview
The Comprehensive Auto System Optimizer is a Blender addon designed to intelligently optimize your Blender settings based on your computer's hardware. By analyzing the GPU, RAM, and system configuration, this script automatically adjusts rendering and memory settings to maximize performance and efficiency.

Key Features
Hardware Detection:

Detects the installed GPU and determines its capabilities.
Calculates available RAM for system-level adjustments.
Rendering Optimization:

Sets the optimal rendering resolution based on GPU performance.
Configures the maximum Cycles rendering samples to balance quality and speed.
Memory Management:

Dynamically adjusts Blender's memory cache limit based on the detected system RAM, ensuring efficient use of available resources.
User-Friendly Integration:

Adds a dedicated panel under Preferences -> System for easy access.
Includes a simple "Run Optimizer" button to apply all adjustments with a single click.
Console Logging:

Outputs detailed hardware information and applied settings to the Blender console for transparency and debugging.

How to Use
Save the script as a .py file (e.g., comprehensive_system_optimizer.py).
Install the addon:
Open Blender.
Go to Edit -> Preferences -> Add-ons.
Click Install, select the .py file, and enable it.
Run the optimizer:
Go to Preferences -> System.
Click Run Optimizer to apply the settings.

GPU-Based Adjustments:
Sets rendering resolution (resolution_x and resolution_y) based on GPU.
Sets sampling settings (cycles.samples) for Cycles rendering.
RAM-Based Adjustments:

Dynamically sets Blender’s memory cache limit based on detected RAM.
User-Friendly UI:

Adds a panel under Preferences -> System with a button to run the optimization.
Logs to Console:

Logs detected hardware and applied settings for debugging.
