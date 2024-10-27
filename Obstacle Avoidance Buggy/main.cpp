#include "mbed.h"
#include <cstdio>

// Define pins for Trigger and Echo
DigitalOut triggerPin1(D3);
DigitalIn echoPin1(D4);
DigitalOut triggerPin2(D7);
DigitalIn echoPin2(D8);
DigitalOut triggerPin3(D6);
DigitalIn echoPin3(D5);

// Define variables
Timer timer;


int SensorLeft() {
    // Initialize trigger pin
    triggerPin1 = 0;
    float distance = 0.0;
    // Trigger the sensor
    triggerPin1 = 1;
    wait_us(10);
    triggerPin1 = 0;
    // Wait for echo start
    while(echoPin1.read() == 0);

    // Start the timer
    timer.start();

    // Wait for echo end
    while(echoPin1.read() == 1);

    // Stop the timer
    timer.stop();

    // Calculate distance
    float duration = timer.read_us();
    distance = (duration / 2) / 29.1; // Speed of sound in air is approximately 29.1 microseconds per centimeter
    timer.reset();
    return distance;
}

int SensorRight() {
    // Initialize trigger pin
    triggerPin2 = 0;
    float distance;
    // Trigger the sensor
    triggerPin2 = 1;
    wait_us(10);
    triggerPin2 = 0;
    // Wait for echo start
    while(echoPin2.read() == 0);

    // Start the timer
    timer.start();

    // Wait for echo end
    while(echoPin2.read() == 1);
    // Stop the timer
    timer.stop();

    // Calculate distance
    float duration = timer.read_us();
    distance = (duration / 2) / 29.1; // Speed of sound in air is approximately 29.1 microseconds per centimeter
    timer.reset();
    return distance;
}

int SensorForward() {
    // Initialize trigger pin
    triggerPin3 = 0;
    float distance;
    // Trigger the sensor
    triggerPin3 = 1;
    wait_us(10);
    triggerPin3 = 0;

    // Wait for echo start
    while(echoPin3.read() == 0);

    // Start the timer
    timer.start();

    // Wait for echo end
    while(echoPin3.read() == 1);

    // Stop the timer
    timer.stop();

    // Calculate distance
    float duration = timer.read_us();
    distance = (duration / 2) / 29.1; // Speed of sound in air is approximately 29.1 microseconds per centimeter
    timer.reset();
    return distance;
}

// Sensor Code Ends here

PwmOut Out1(PA_1); //PA_1
DigitalOut Out2(PB_7); //PC_2
PwmOut Out3(PB_0); //PB_0
DigitalOut Out4(PA_4); //PA_4

DigitalIn GPIO1(PC_0); //PC_0
DigitalIn GPIO2(PC_1); //PA_15
DigitalIn GPIO3(PC_3); //PB_7
DigitalIn GPIO4(PC_2); //PC_3
DigitalIn GPIO5(PA_15); // PC_1
DigitalIn GPIO6(PA_14); // PA_14

int PWM_Values[3] = {0, 30, 50};
int Index = 0;

void InitialiseButton(){

    GPIO1.mode(PullDown);
    GPIO2.mode(PullDown);
    GPIO3.mode(PullDown);
    GPIO4.mode(PullDown);
    GPIO5.mode(PullDown);
    GPIO6.mode(PullDown);

}

void Initialise(){

    Out1.write(0);
    Out2.write(0);
    Out3.write(0);
    Out4.write(0);

}

void Left(){

    Out2.write(0);
    Out3.write(1);
    Out4.write(0);
    if (Index == 0){
        Out1.write(0);
        Out2.write(1);
    } else {
        float DutyCycle = PWM_Values[Index] / 100.0;
        Out1.write(DutyCycle);
    }
}

void Right(){

    Out1.write(1);
    Out2.write(0);
    Out4.write(0);
    if (Index == 0){
        Out3.write(0);
        Out4.write(1);
    } else {
        float DutyCycle = PWM_Values[Index] / 100.0;
        Out3.write(DutyCycle);
    }
}

void Forward(){

    Out1.write(1);
    Out2.write(0);
    Out3.write(1);
    Out4.write(0);
}

void Backward(){

    Out1.write(0);
    Out2.write(1);
    Out3.write(0);
    Out4.write(1);

}

int main()
{
    float Frequency = 1000;
    Out1.period(1.0f / Frequency);
    Out3.period(1.0f / Frequency);

    int G5 = 0;

    Initialise();
    InitialiseButton();

    float DistanceLeft = 0.0;
    float DistanceRight = 0.0;
    float DistanceForward = 0.0;

    while (true)
    {
        if(GPIO6 == 1){
            DistanceLeft = SensorLeft();
            DistanceRight = SensorRight();
            DistanceForward = SensorForward();
        }
        if(DistanceForward < 20 && GPIO6 == 1 && GPIO2 != 1 && GPIO4 != 1){
            Index = 0;
            Right();
        } else if(DistanceForward < 40 && GPIO6 == 1 && GPIO2 != 1 && GPIO4 != 1){
            if(DistanceRight > 25){
                Index = 1;
                Right();
                Index = 0;
            } else if (DistanceLeft > 25) {
                Index = 1;
                Left();
                Index = 0;
            } else{
                Initialise();
            }
        } else if(DistanceRight < 15 && GPIO6 == 1){
            Index = 2;
            Left();
        } else if(DistanceLeft < 15 && GPIO6 == 1){
            Index = 2;
            Right();
        } else{
            if (GPIO1 == 1 && GPIO3 == 1){
                Forward();
            } else if (GPIO2 == 1 && GPIO4 == 1){
                Backward();
            } else if (GPIO2 == 1 && GPIO3 == 1){
                Left();
            } else if (GPIO1 == 1 && GPIO4 == 1){
                Right();
            } else {
                Initialise();
            }

            if (GPIO5 != G5){
                G5 = GPIO5;
                Index += 1;
                Index = Index % 3;
            }
        }
    }
}