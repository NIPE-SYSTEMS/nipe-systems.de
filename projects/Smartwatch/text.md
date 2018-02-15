# Smartwatch

> Semester project at the university: The project features rethinking of a smartwatch with limited components to achieve energy-efficiency.

## Reinventing the wheel?

Current smartwatches mostly provide fitness metrics and multimedia features. This makes them expensive. Furthermore batteries last some days with light usage. The goal of this smartwatch is to display notifications from the smartphone and a simple clock. One of the design goals is that the battery should last at least a week. The watch works 'offline' which means that all informations are kept on the smartphone.

The smartwatch should address the following challenges: It needs to be energy-efficient and comfortable. This means that the device needs to be small. Every component is carefully choosen to fulfill the requirements which leads to limited ressources e.g. limited memory and/or limited bandwidth between the components. Furthermore the software must be carefully designed to work under these conditions.

## Energy-efficient parts

A display of a smartwatch is in general the most energy drawing component. A conventional LCD/LED screen is out of scope since it needs constant power to display e.g. the clock. Therefore the smartwatch uses an e-paper display which does not need any power to display a still image and is furthermore readable in the sunlight.

For the controller, the mainboard of the watch has a low-power microcontroller (Atmel ATMEGA8L) built-in. The chip has 1 KB RAM and a clock speed of 8 MHz which limits the possibilities for a complex software. To enable the watch to work autonomously without the smartphone (which also decreases energy usage) the watch must be capable of storing everything that is needed to drive the display and other components.

## Smartphone communication

The communication to the smartphone is based on Bluetooth Low Energy (BLE). The smartphone helds the high-level informations of the smartwatch (notifications, media, etc.). When the watch screen should display new informations the smartphone sends low-level rendering informations to the watch over BLE. The watch stores these in dedicated SRAM modules located on the mainboard.

Since the memory of the microcontroller is small compared to the sent informations the software is capable of moving the data in parts to the desired locations. That includes displaying images on the display (a whole copy of the framebuffer requires 5 KB but the controller has only 1 KB RAM).

## Completed milestones

* **NOV//17**: Design of circuit board
* **JAN//18**: Assembly of circuit board
* **FEB//18**: First working test program (testing microcontroller)
