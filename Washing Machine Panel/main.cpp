#include "mbed.h"
#include <cstdio>
#include "Notes.h"

BufferedSerial pc(USBTX, USBRX, 115200);
DigitalIn OnOff(PC_11); // ON and OFF button
DigitalIn DoorLock(PD_2); // Safety feature to make sure the door is locked
DigitalIn Run(PC_10); // The run button and also the override button when held
DigitalOut RedTemperature(PA_4); // Red LED indicating washing at 60 degrees
DigitalOut YellowTemperature(PA_1); // Yellow LED indicating washing at 40 degrees
DigitalOut GreenTemperature(PB_0); // Green LED indicating washing at 20 degrees
DigitalOut StatusGreen(PC_1); // Green LED indicating washing taking place
DigitalOut StatusRed(PC_0); // Red LED indicating standby
AnalogIn FSR1(PA_7); // When pressed sets the cycle to wash at 60 degrees
AnalogIn FSR2(PC_4); // When pressed sets the cycle to wash at 40 degrees
AnalogIn FSR3(PA_5); // When pressed sets the cycle to wash at 20 degrees
AnalogIn TMP(PA_6); // Sensor to wash at the correct temperature
AnalogIn Pot(PA_0); // To set the time of the 7 segment
PwmOut Buzzer(PA_15); // To play a sound at the end of the cycle
//segment       A       B     C      D    E     F      G        
BusOut SegDis(PB_12, PB_11, PB_1, PB_14, PB_15, PA_11, PA_12);
BusOut SegDis2(PB_3, PA_10, PA_9, PA_8, PB_10, PB_5, PB_4);

//               0     1     2     3     4     5     6     7     8     9   
int hexDis[] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};

void Initialise(); // Makes everything OFF
void InitialiseLEDs(); // Turns off the temperature LEDs
void TurnOn(); // Turns on the right LEDs
float ReadPot(); // Reads the value from the pot
void WriteDisplay(short Num1, short Num2); // Writes the value from the pot to the 7 segment
void FlashRed(); // Flashes the StatusRed LED indicating an error
void FlashGreen(); // Flashes the StatusGreen LED indicating cycle complete
void PlayBuzzer(); // When cycle completes or when powered on
void PlayCancel(); // If the cycle is cancelled the buzzer makes some noise
short ReadForce(); // Reads the values from the FSR
void RunCycle(short Timer, short Temp, bool Override); // Begins the cycle


int main()
{
    short Time = 0; // 7 Segment time
    short PotValue = 0; // Reading from pot. Limited to values from 0-4 by dividing 20 later
    bool Door = 0; // A 0 or LOW means the Door is open and the cycle cannot run
    short FSRVal = 0; // Takes values from 0-3 tells which force sensors is used and 0 is none
    short Temperature = 20; // The temperature that the cycle will run at
    bool IO = 0; // Machine is On or Off (The IO symbol where I is power on and O is power Off)
    short SleepTime = 0; // Used to turnoff the machine if not used
    short PreviousTime = 0; // To see if time was changed meaning SleepTime has to be reset
    short Counter = 0; // To adjust the TimeOn value
    short TimeOn = 10; // How long the machine can be on without activity

    Initialise();

    printf("The button on the right is the on/off button. The button next to it opens/closes the door. The last button beginss the cycle.\n");
    printf("Move the pot to adjust the cycle time. The 3 force sensors adjusts the temperatures. The 3 LEDs indicate what the temperature is set to: \n");
    printf("    1. Red is for 60 Celsius\n  2. Yellow is for 40 Celsius\n   3. Green is for 20 Celsius\n");
    printf("At the bottom, Green indicates cycle is running or about to start (flashing). Red is standby. A flashing red is an error.\n");
    
    while (true) {

        if(OnOff.read()){

            if(IO){ // Checking if the OnOff button is being held which is only applicable when machine is On
                while(true){ // Keeps counting as long as the button is pressed
                    if(OnOff.read()){
                        Counter += 1;
                        ThisThread::sleep_for(100ms);
                    } else {
                        break;
                    }
                }
            }

            if(Counter >= 25){ // This is equivalent to holding the button for 2.5s
                Counter = 0;
                while(!OnOff.read()){ // Loop runs until the OnOff is clicked again confirming the user choice
                    PotValue = ReadPot() / 34; // Limits value to 0,1,2
                    switch (PotValue) {
                        case 0:
                            WriteDisplay(1, 0);
                            TimeOn = 10; //10s
                            break;
                        case 1:
                            WriteDisplay(1, 5);
                            TimeOn = 15; //15s
                            break;
                        case 2:
                            WriteDisplay(2, 0);
                            TimeOn = 20; //20s
                            break;
                    }
                }
                SleepTime = 0;
                ThisThread::sleep_for(300ms); // Necessary as otherwise may register 1 click to be multiple presses hence turning the machine off then on
            } else {
                IO = !IO; // Toggle when the button is pressed On to Off or Off to On
                if(IO == 1){ // If On then run the On code
                    TurnOn();
                    printf("Washing Machine is on.\n");
                } else { // If Off run the Off code
                    printf("Turning off Washing Machine.\n");
                    Initialise();
                }
                ThisThread::sleep_for(300ms); // So it does not register multiple inputs
            }
            
        }

        if(SleepTime == TimeOn * 20){ // *20 as 50ms*20 = 1s where 50ms is the thread sleep time
            // Turns off if not used
            Initialise();
            SleepTime = 0;
            IO = 0;
            printf("Washing Machine is Off. Idle for too long!\n");
            printf("To adjust how long the machine can stay On, turn it on and hold the on/off button.\n");
            printf("Adjust the time using the pot and press the on/off button to confirm.\n");
        }

        if(IO == 1){
            PotValue = (ReadPot() - 0.01) / 20; // -0.01 to ensure it does not reach 100 and become 5
            switch (PotValue) { // Choosing the cycle time
                case 0:
                    WriteDisplay(1, 0);
                    Time = 10;
                    break;
                case 1:
                    WriteDisplay(1, 5);
                    Time = 15;
                    break;
                case 2:
                    WriteDisplay(3, 0);
                    Time = 30;
                    break;
                case 3:
                    WriteDisplay(4, 5);
                    Time = 45;
                    break;
                case 4:
                    WriteDisplay(6, 0);
                    Time = 60;
                    break;
            }

            if(PreviousTime != Time){
                // Checks if the time is changed meaning machine is in use
                SleepTime = 0;
                PreviousTime = Time;
            }

            if(DoorLock.read()){
                // Toggle Door when button is clicked
                Door = !Door;
                SleepTime = 0;
                if(Door){
                    printf("Door has been locked.\n");
                } else {
                    printf("Door is unlocked.\n");
                }
                ThisThread::sleep_for(500ms); // To avoid having the button register multiple inputs for a single press
            }

            FSRVal = ReadForce();
            switch (FSRVal) {
                case 0:
                    break;
                case 1:
                    if(Temperature != 20){
                        // Check made so that a message is only displayed when temp. changes
                        printf("Temperature is set to 20 degrees Celsius.\n");
                        SleepTime = 0;
                    }
                    Temperature = 20;
                    InitialiseLEDs();
                    GreenTemperature.write(1);
                    break;
                case 2:
                    if(Temperature != 40){
                        printf("Temperature is set to 40 degrees Celsius.\n");
                        SleepTime = 0;
                    }
                    Temperature = 40;
                    InitialiseLEDs();
                    YellowTemperature.write(1);
                    break;
                case 3:
                    if(Temperature != 60){
                        printf("Temperature is set to 60 degrees Celsius.\n");
                        SleepTime = 0;
                    }
                    Temperature = 60;
                    InitialiseLEDs();
                    RedTemperature.write(1);
                    break;
            }

            if(Run.read()){
                SleepTime = 0;
                if(Door){
                    // Checks that the door is locked
                    RunCycle(Time, Temperature, 0);
                } else {
                    // Error signal
                    FlashRed();
                    printf("Door is unlocked! Make sure it is locked.\n");
                }
            }

            // stops SleepTime incrementing instantly
            ThisThread::sleep_for(50ms);
            SleepTime += 1;
        }
    }
}

void Initialise(){
    SegDis.write(0x00);
    SegDis2.write(0x00);

    RedTemperature.write(0);
    GreenTemperature.write(0);
    YellowTemperature.write(0);
    StatusGreen.write(0);
    StatusRed.write(0);

    OnOff.mode(PullNone);
    DoorLock.mode(PullNone);
    Run.mode(PullDown); // Not enough external resistors so PullDown used
}

void InitialiseLEDs(){
    RedTemperature.write(0);
    GreenTemperature.write(0);
    YellowTemperature.write(0);
}

void TurnOn(){
    StatusRed.write(1);
    GreenTemperature.write(1);
    // This part is taken from ELEC1620 PWM-Buzzer-Example
    int Notes[] = {NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4};

    for(int i = 0; i < 4; i++){
        Buzzer.period_us((float) 1000000.0f/ (float) Notes[i]);
        Buzzer.pulsewidth_us(Buzzer.read_period_us()/2);
        ThisThread::sleep_for(500ms);
    }
    Buzzer.pulsewidth_us(0);
}

float ReadPot(){
    return 100 * Pot.read();
}

void WriteDisplay(short Num1, short Num2){
    // hexDis will change the index (e.g. 1) to the hex value required for the output display
    SegDis.write(hexDis[Num1]);
    SegDis2.write(hexDis[Num2]);
}

void FlashRed(){
    for(short i = 0; i < 4; i++){
        // Period is 1s
        StatusRed.write(1);
        ThisThread::sleep_for(500ms);
        StatusRed.write(0);
        ThisThread::sleep_for(500ms);
    }
    StatusRed.write(1);
}

void FlashGreen(){
    for(short i = 0; i < 4; i++){
        // Period is 1s
        StatusGreen.write(1);
        ThisThread::sleep_for(500ms);
        StatusGreen.write(0);
        ThisThread::sleep_for(500ms);
    }
    StatusGreen.write(1);
}

short ReadForce(){
    if(FSR1.read() * 100 > 50){
        // Sensor 1 is pressed so return 1 and the same goes for the rest
        return 1;
    } else if (FSR2.read() * 100 > 50) {
        return 2;
    } else if (FSR3.read() * 100 > 50) {
        return 3;
    } else {
        // None of the sensors are being pressed
        return 0;
    }
}

void PlayBuzzer(){
    // Array of the notes being played and their duration
    // Notes and Durations were taken from the internet
    int Durations[] = {
        8, 16, 8, 8, 8, 8, 8, 8,
        8, 8,
        8, 16, 8, 8, 8, 8, 8, 8,
        2, 8, 1

    };
    int Notes[] = {
        NOTE_C4, NOTE_E4, NOTE_G4, NOTE_C5, NOTE_E5, NOTE_D5, NOTE_C5, NOTE_A4,
        NOTE_FS4, NOTE_G4,
        NOTE_C4, NOTE_E4, NOTE_G4, NOTE_C5, NOTE_E5, NOTE_D5, NOTE_C5, NOTE_A4,
        NOTE_G4, NOTE_A4, NOTE_DS4
    };

    for(int i = 0; i < sizeof(Durations) / sizeof(int); i++){
                // Very similar to the TurnOn() Buzzer
                Buzzer.period_us((float) 1000000.0f/ (float) Notes[i]);
                Buzzer.pulsewidth_us(Buzzer.read_period_us()/10);
                thread_sleep_for(1000.0/Durations[i]);
                Buzzer.pulsewidth_us(0);
                // A pause between the notes necessary to distinguish the notes from each other
                int pauseBetweenNotes = 1000.0/ Durations[i] * 1.30;
                thread_sleep_for(pauseBetweenNotes);
            }
}

void PlayCancel(){
    // Identical to the previous implementation in PlayBuzzer()
    int Durations[] = {
        4, 4, 4, 4
    };
    int Notes[] = {
        NOTE_F5, NOTE_F5, NOTE_F5, NOTE_F5
    };

    for(int i = 0; i < sizeof(Durations) / sizeof(int); i++){
                Buzzer.period_us((float) 1000000.0f/ (float) Notes[i]);
                Buzzer.pulsewidth_us(Buzzer.read_period_us()/10);
                thread_sleep_for(1000.0/Durations[i]);
                Buzzer.pulsewidth_us(0);
                // A pause between the notes necessary to distinguish the notes from each other
                int pauseBetweenNotes = 1000.0/ Durations[i] * 1.30;
                thread_sleep_for(pauseBetweenNotes);
            }
}

void RunCycle(short Timer, short Temp, bool Override){
    short Count = 0; // A counter that counts how long the Run button was held while running. Used to cancel a cycle
    short Num1 = Timer / 10; // Operations to extract the 10s from the number
    short Num2 = Timer % 10; // Operation to extract the 1s
    bool Cancel = 0; // Determines if the cycle is cancelled (HIGH for cancelled)

    float TMP_Val = TMP.read() * 3.3 / 0.01; // Calculation for the temperature
    printf("The Temperature = %.3f \n", TMP_Val);

    if(TMP_Val - Temp < 5 && TMP_Val - Temp > -5 || Override){
        // Check made to see that the temperature is within 5 Celsius from the washing temp.
        // Also checks if the user wants to override the temp. check
        StatusRed.write(0);
        printf("Running Cycle!\n");
        FlashGreen();
        // Nested loop from Time to 0s
        for(short i = Num1; i >= 0; i--){
            for(short j = Num2; j >= 0; j--){
                WriteDisplay(i, j);
                if(Count == 4){
                    Cancel = 1;
                    break;
                }
                if(Run.read()) {
                    // If the Run button is held then Count increments
                    Count += 1;
                } else{
                    Count = 0;
                }
                ThisThread::sleep_for(1s);
            }
            Num2 = 9; // So the next cycle counts from 9 as Num2 could be 5 or 0.
            if(Count == 4){
                // The run button is held for 3-4 seconds so cycle is cancelled
                printf("Cycle cancelled!\n");
                Cancel = 1;
                break;
            }
        }

        if(!Cancel){
            // Cycle ended normally
            PlayBuzzer();
        } else {
            // Cycle was cancelled
            PlayCancel();
            printf("Cycle Cancelled!\n");
        }
        StatusGreen.write(0);
        StatusRed.write(1);

    } else {
        printf("Incorrect Temperature of the Washing Machine!\n");
        printf("Press the run button to cancel or hold to override after the flash stops.\n");
        FlashRed();
        while(true){
            // Begin the count when the Run button is first clicked. This is an entry point to the loop
            if(Run.read()){
                while(true){
                // if the button is released then the count stops
                    if(Run.read()){
                        Count += 1;
                    } else {
                        break;
                    }
                    if(Count >= 30){
                        // If the button was held for almost 3 seconds then override the error
                        // If it was held for less i.e. was just clicked then cancel operation
                        RunCycle(Timer, Temp, 1); // 1 indicates that the override flag is raised
                    }
                    ThisThread::sleep_for(100ms);
                }
                break;
            }
        }
    }
    
}
