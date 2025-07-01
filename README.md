# Visual-Logistics-Puppy-Pi-Robot

This repository contains ROS packages and scripts for the **Puppy Pi robot** by Hiwonder.

## 📂 Directory Structure

Within the repository, the `src/line_tag_detection` directory contains three main ROS packages:

- `puppy_follower`
- `puppy_navigation`
- `[...]` *(please replace this with the third package when you remember it)*

These packages are responsible for the robot's behavior, including color line following, navigation, and tag-based interaction.

## 🚀 How to Run

To run the system:

1. **Source the environment:**

   ```bash
   source devel/setup.bash
   
2. **Launch the follower script:**

    ```bash
    rosrun puppy_follower <your_script_name>.py
    
3. **Use available ROS services:**

   ```bash
   rosservice call /rosnode/enter
   rosservice call /rosnode/set_running 1
   rosservice call /rosnode/set_target blue or black or red or ...

4. **To view the camera image:**

   ```bash
   rqt_image_view

📌 Notes
Make sure your Puppy Pi is connected and running roscore.

Some services (like /rosnode/enter) may require specific launch or pose conditions to be active.
