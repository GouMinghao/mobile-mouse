# Using Your Mobile Phone as the Mouse to Control Your PC  
## Developer  
 - Minghao Gou, School of Mechanical Engineering, Shanghai Jiao Tong University  
 - Panzheng Zhou, School of Chemistry, Shanghai Jiao Tong University  
 - Jiangtong Li, Zhiyuan College, Shanghai Jiao Tong University  
 - Ruihao liu, School of Biomedical Engineering, Shanghai Jiao Tong University  
 - Peihan Zhang, School of Mechanical Engineering, Shanghai Jiao Tong University  
## How It Works  
### Acceleration data  
We use the accelerometer in the mobile phone with Android operating system.
We use API provided by the operating system to read the accelerometer data.

### Problem in Calculating Velocity of the Mouse  
In theory, the integration of acceleration is velocity.
However, this may not make sense in practice.
There is some bias and error with the sensor and the stimulation of small error in acceleration may lead to tremendous error in velocity.
In addition, the sum of discrete sampling of acceleration is different from the integration of continious acceleration.
There is also some error caused by discrete sampling.
As a result, the common way to calculate velocity has great problem and needs to be inproved.
### Solutions  
In order to solve the problem above, we proposed several solutions.
 - Kalman filter is applied on the acceletation data.  
 - Calibration is applied before using the system to decrease caused by the sensor bias.  
 - Attenuation of velocity is exerted to avoid divergency of velocity.  
 - Activation function is used to alleviate the backlash.  
#### Kalman filter  
Kalman filter is usually used in dealing with inertial sensor data to remove noise.
It's based on the prediction of the next state.  
```python
ax, xVar = kalmanFilter(ax,xPreData,xVar,Q,R)
ay, yVar = kalmanFilter(ay,yPreData,yVar,Q,R)
```
#### Calibration  
Before using the system, the user should put the mobile phone in the working surface.
Then the system set the zero of acceleration to the mean value of static sensor data.
After this step, the effect of inclination of the surface and the sensor bias is conpensated.  
```python
ax = x0int / 32.0 * 9.8 - axave
ay = y0int / 32.0 * 9.8 - ayave
```
#### Attenuation of Velocity  
We let the velocity damps with a constant rate so that the velocity will convergent even the integration of acceleration divergent.
```python
# damp the speed
vx = vx * dampRate
vy = vy * dampRate
```
#### Activation function
There will be backlash when stop moving the mouse because of the huge reverse acceleration.
It always causes the cursor to move backward which is not expected.  
Therefore, we desigend an activation function to change the effect of accleration on the change of velocity.
When the velocity is very small, the cursor is static and there is no problem of backlash.
As a result, the acceleration should have great effect on the change of velocity.
On the contrary, when the cursor is moving fast, huge acceleration is usually cause by stopping the mouse.
So the acceleratiou shouldn't have a big enough impact on velocty or there will be backlash.
In our design, the change of velocity is decided by several factors as shown below:
```python
dvx = np.exp(-abs(vx)) * ax * v
dvy = np.exp(-abs(vy)) * ay * v
```
dv is the change of velocity, np.exp is the exponential function provided by numpy package in python, a is the acceleration and v is a constant to magify the relative speed which is specified by the user.  
As we can see, dv decreases with the increase of the absolute value of v. 
## Communcation Protocal  

### Hardware  

### Encoding

## Running Requirement  

### Mobile Phone  
 - Phone with Android OS is required.(tested on EMUI 8.0.0(Huawei))  
 - Phone with bluetooth 4 is required or it cannot communicate with conputer  

### Computer  
 - PC with Windows OS is required.(tested on Windows 10 Pro)  
 - PC with python environment is required.(tested on python 3.5)  
 - Python package numpy, serial, win32api and win32con are required.(tested using Anaconda 5.1.0(Python 3.5))  

## Setup  
### Mobile Phone  
Install the csNetworkNewbeta.apk APP on your Android phone and open the bluetooth on system setting.  
### Computer  
Insert a external bluetooth in your USB port.
In the test, we use HC-05 bluetooth module and a ttl serial port to usb converter.
The connection is shown in the picture below.
![Picture](./pic/connection.jpg)  
HC-05---------TTL to USB converter  
5V ----------------------- 5V  
GND --------------------- GND  
TX ----------------------- RX  
RX ----------------------- TX  
  
Set the path to the root folder that contains driver.py  

## Run  
### Phone  
Open the "Xiao" APP and click the "Connect to BlueTooth" button then choooe the bluetooth device conneted to your PC.  
**We should pay attention that this step must be done before run the python written driver program.**  
![Picture](./pic/xiao.jpg)  

### Computer  
Run the command as follows:
```cmd
python driver.py (serial port number) [(cursor move speed)] [(threshhold for moving)] [(damp rate)] [(Q)] [(R)]
```
We can just give the first few parameters that is included in '[' and ']' and the parameters will be set the default value. 
Some of the few examples are given below:
```cmd
python driver.py COM3 20 
python driver.py COM3 20 0.4
python driver.py COM3 20 0.4 0.8
python driver.py COM3 20 0.4 0.8 0.1
python driver.py COM3 20 0.4 0.8 0.1 0.25
```
These values are also the default value and as a result, these commands have the same effect.  

### Calibration
Make sure that the xiao APP is running without lock the screen when the program begins and put the mobile phone on the surface where you want to use this program.  
The program will print some of the information and after that it's available to use the mouse to control your computer.
